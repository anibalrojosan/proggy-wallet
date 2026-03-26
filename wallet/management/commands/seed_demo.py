from __future__ import annotations

import random
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction as db_transaction
from django.db.models import Max, Q
from django.utils import timezone

from wallet.models import Account, Transaction

User = get_user_model()

PEER_COUNT = 3
PEER_PREFIX = "seed_peer_"
DEFAULT_RESET_BALANCE = Decimal("500000.00")


class Command(BaseCommand):
    help = (
        "Create demo transactions for an existing user. "
        "First run: use --reset-balances (and optional --initial-balance). "
        "Later runs: omit --reset-balances so timestamps and balances continue from the DB."
    )

    def add_arguments(self, parser) -> None:
        parser.add_argument("--username", required=True, type=str)
        parser.add_argument("--count", type=int, default=300)
        parser.add_argument(
            "--seed",
            type=int,
            default=None,
            help="Optional RNG seed for reproducible data.",
        )
        parser.add_argument(
            "--reset-balances",
            action="store_true",
            help=(
                "Set target user and seed_peer_* accounts to --initial-balance before seeding. "
                "Omit on repeat runs so balances and balance_after stay consistent with existing rows."
            ),
        )
        parser.add_argument(
            "--initial-balance",
            type=Decimal,
            default=DEFAULT_RESET_BALANCE,
            help=f"With --reset-balances, balance assigned to target and peers (default: {DEFAULT_RESET_BALANCE}).",
        )

    def handle(self, *args, **options) -> None:
        if options["seed"] is not None:
            random.seed(options["seed"])

        username = options["username"]
        count = max(1, options["count"])

        try:
            target = User.objects.get(username=username)
        except User.DoesNotExist as e:
            raise CommandError(f"No user with username {username!r}.") from e

        peers = self._ensure_peers()
        if options["reset_balances"]:
            self._top_up_balances([target, *peers], options["initial_balance"])

        created = 0
        attempts = 0
        max_attempts = max(count * 25, 100)
        # New rows must sort after existing ones so balance_after matches chronological order.
        tx_ts = self._next_batch_start_timestamp(target, peers)

        while created < count and attempts < max_attempts:
            attempts += 1
            amount = Decimal(str(round(random.uniform(5.0, 350.0), 2)))
            kind = random.choices(
                ["deposit", "transfer_out", "transfer_in", "withdrawal"],
                weights=[0.28, 0.32, 0.32, 0.08],
                k=1,
            )[0]
            peer = random.choice(peers)
            try:
                with db_transaction.atomic():
                    if kind == "deposit":
                        self._do_deposit(target, amount, tx_ts)
                    elif kind == "transfer_out":
                        self._do_transfer(target, peer, amount, tx_ts)
                    elif kind == "transfer_in":
                        self._do_transfer(peer, target, amount, tx_ts)
                    else:
                        self._do_withdrawal(target, amount, tx_ts)
                tx_ts += timedelta(seconds=random.randint(15, 240))
                created += 1
            except ValueError:
                continue

        if created < count:
            raise CommandError(f"Stopped after {attempts} attempts with only {created} transaction(s); try a smaller --count.")

        self.stdout.write(self.style.SUCCESS(f"Created {created} transaction(s) for {username!r}."))

    def _ensure_peers(self):
        peers = []
        for i in range(PEER_COUNT):
            u, created = User.objects.get_or_create(
                username=f"{PEER_PREFIX}{i}",
                defaults={"email": f"{PEER_PREFIX}{i}@seed.local"},
            )
            if created:
                u.set_unusable_password()
                u.save()
            peers.append(u)
        return peers

    def _top_up_balances(self, users: list, amount: Decimal) -> None:
        ids = [u.id for u in users]
        Account.objects.filter(user_id__in=ids).update(balance=amount)

    @staticmethod
    def _next_batch_start_timestamp(target, peers):
        ids = [target.id] + [p.id for p in peers]
        latest = Transaction.objects.filter(Q(from_user_id__in=ids) | Q(to_user_id__in=ids)).aggregate(m=Max("created_at"))["m"]
        if latest is None:
            return timezone.now() - timedelta(days=365)
        return latest + timedelta(microseconds=1)

    @staticmethod
    def _set_created_at(tx_id: int, when) -> None:
        Transaction.objects.filter(pk=tx_id).update(created_at=when)

    def _do_deposit(self, target: User, amount: Decimal, when) -> None:
        acc = Account.objects.get(user=target)
        acc.balance += amount
        acc.save(update_fields=["balance"])
        tx = Transaction.objects.create(
            to_user=target,
            amount=amount,
            type="deposit",
            balance_after=acc.balance,
            description="Seed demo deposit",
        )
        self._set_created_at(tx.pk, when)

    def _do_transfer(self, sender: User, receiver: User, amount: Decimal, when) -> None:
        if sender.id == receiver.id:
            raise ValueError("same user")
        from_acc = Account.objects.select_for_update().get(user=sender)
        if from_acc.balance < amount:
            raise ValueError("insufficient")
        to_acc = Account.objects.select_for_update().get(user=receiver)
        from_acc.balance -= amount
        to_acc.balance += amount
        from_acc.save(update_fields=["balance"])
        to_acc.save(update_fields=["balance"])
        tx = Transaction.objects.create(
            from_user=sender,
            to_user=receiver,
            amount=amount,
            type="transfer",
            balance_after=from_acc.balance,
            balance_after_to_user=to_acc.balance,
            description=f"Seed transfer {sender.username}->{receiver.username}",
        )
        self._set_created_at(tx.pk, when)

    def _do_withdrawal(self, target: User, amount: Decimal, when) -> None:
        acc = Account.objects.select_for_update().get(user=target)
        if acc.balance < amount:
            raise ValueError("insufficient")
        acc.balance -= amount
        acc.save(update_fields=["balance"])
        tx = Transaction.objects.create(
            from_user=target,
            to_user=None,
            amount=amount,
            type="withdrawal",
            balance_after=acc.balance,
            description="Seed demo withdrawal",
        )
        self._set_created_at(tx.pk, when)
