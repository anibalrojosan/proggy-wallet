"""Reset demo guest + peer users to a fixed ledger snapshot (see management command)."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction as db_transaction
from django.db.models import Q

from wallet.models import Account, Transaction

if TYPE_CHECKING:
    from django.contrib.auth.models import User

User = get_user_model()

EXPECTED_PEER_COUNT = 3


def all_demo_usernames() -> frozenset[str]:
    return frozenset([settings.DEMO_GUEST_USERNAME, *get_demo_peer_usernames()])


def is_demo_sandbox_username(username: str) -> bool:
    return username in all_demo_usernames()


def get_demo_peer_usernames() -> list[str]:
    peers = list(settings.DEMO_PEER_USERNAMES)
    if len(peers) != EXPECTED_PEER_COUNT:
        msg = (
            f"DEMO_PEER_USERNAMES must expand to exactly {EXPECTED_PEER_COUNT} usernames; "
            f"got {len(peers)}: {peers!r}"
        )
        raise ValueError(msg)
    return peers


def ensure_demo_users_exist() -> None:
    """Create guest + peer users and set passwords (no ledger seed). Idempotent."""
    guest_name = settings.DEMO_GUEST_USERNAME
    peer_names = get_demo_peer_usernames()
    guest, _created_g = User.objects.get_or_create(
        username=guest_name,
        defaults={"email": f"{guest_name}@demo.local"},
    )
    guest.set_password(settings.DEMO_GUEST_PASSWORD)
    guest.save()
    for name in peer_names:
        peer, _created = User.objects.get_or_create(
            username=name,
            defaults={"email": f"{name}@demo.local"},
        )
        peer.set_unusable_password()
        peer.save()


def tear_down_demo_sandbox() -> None:
    """Remove all demo users and any transactions involving them (after guest logout)."""
    users = list(User.objects.filter(username__in=all_demo_usernames()))
    if not users:
        return
    ids = [u.id for u in users]
    with db_transaction.atomic():
        Transaction.objects.filter(
            Q(from_user_id__in=ids) | Q(to_user_id__in=ids)
        ).delete()
        User.objects.filter(id__in=ids).delete()


def sandbox_ledger_q(guest: User, peers: list[User]) -> Q:
    ids = [guest.id] + [p.id for p in peers]
    return Q(from_user_id__in=ids) | Q(to_user_id__in=ids)


def reset_demo_sandbox() -> None:
    """
    Delete all transactions touching the guest or any demo peer, then re-seed
    accounts and exactly 10 transactions. Idempotent.
    """
    guest_username = settings.DEMO_GUEST_USERNAME
    peer_names = get_demo_peer_usernames()

    guest = User.objects.filter(username=guest_username).first()
    peers = list(User.objects.filter(username__in=peer_names).order_by("username"))
    if guest is None or len(peers) != EXPECTED_PEER_COUNT:
        missing = [guest_username] if guest is None else []
        found_peer_names = {u.username for u in peers}
        for name in peer_names:
            if name not in found_peer_names:
                missing.append(name)
        raise ValueError(
            "Demo sandbox users are missing; use Log in as a guest or run `python manage.py ensure_demo_users`. "
            f"Missing: {missing}"
        )

    peer_by_name = {u.username: u for u in peers}
    ordered_peers = [peer_by_name[name] for name in peer_names]

    with db_transaction.atomic():
        Transaction.objects.filter(sandbox_ledger_q(guest, peers)).delete()

        balances: dict[int, Decimal] = {
            guest.id: Decimal("0"),
            ordered_peers[0].id: Decimal("0"),
            ordered_peers[1].id: Decimal("0"),
            ordered_peers[2].id: Decimal("0"),
        }

        p1, p2, p3 = ordered_peers

        def refresh_accounts() -> None:
            for uid, bal in balances.items():
                Account.objects.filter(user_id=uid).update(balance=bal)

        def create_tx(
            *,
            tx_type: str,
            amount: Decimal,
            from_u: User | None,
            to_u: User | None,
            description: str,
            balance_after: Decimal | None,
        ) -> None:
            Transaction.objects.create(
                from_user=from_u,
                to_user=to_u,
                amount=amount,
                type=tx_type,
                description=description,
                balance_after=balance_after,
            )

        # 10 operations — end state: guest 50000, p1 1000, p2 1000, p3 3500
        ops: list[tuple[str, dict[str, object]]] = [
            ("deposit", {"to": guest, "amount": Decimal("10000"), "desc": "Opening deposit"}),
            ("deposit", {"to": guest, "amount": Decimal("5000"), "desc": "Payroll top-up"}),
            ("transfer", {"from": guest, "to": p1, "amount": Decimal("2000"), "desc": "Transfer to peer 1"}),
            ("transfer", {"from": guest, "to": p2, "amount": Decimal("1500"), "desc": "Transfer to peer 2"}),
            ("deposit", {"to": guest, "amount": Decimal("20000"), "desc": "Savings deposit"}),
            ("transfer", {"from": guest, "to": p3, "amount": Decimal("3500"), "desc": "Transfer to peer 3"}),
            ("transfer", {"from": p1, "to": guest, "amount": Decimal("1000"), "desc": "Refund from peer 1"}),
            ("transfer", {"from": p2, "to": guest, "amount": Decimal("500"), "desc": "Refund from peer 2"}),
            (
                "withdrawal",
                {"from": guest, "amount": Decimal("500"), "desc": "ATM withdrawal"},
            ),
            ("deposit", {"to": guest, "amount": Decimal("21000"), "desc": "Final demo deposit"}),
        ]

        for op_name, payload in ops:
            if op_name == "deposit":
                to_u = payload["to"]  # type: ignore[assignment]
                amount = payload["amount"]  # type: ignore[assignment]
                desc = payload["desc"]  # type: ignore[assignment]
                assert isinstance(to_u, User)
                balances[to_u.id] += amount
                refresh_accounts()
                create_tx(
                    tx_type="deposit",
                    amount=amount,
                    from_u=None,
                    to_u=to_u,
                    description=str(desc),
                    balance_after=balances[guest.id] if to_u.id == guest.id else None,
                )
            elif op_name == "transfer":
                from_u = payload["from"]  # type: ignore[assignment]
                to_u = payload["to"]  # type: ignore[assignment]
                amount = payload["amount"]  # type: ignore[assignment]
                desc = payload["desc"]  # type: ignore[assignment]
                assert isinstance(from_u, User) and isinstance(to_u, User)
                balances[from_u.id] -= amount
                balances[to_u.id] += amount
                refresh_accounts()
                create_tx(
                    tx_type="transfer",
                    amount=amount,
                    from_u=from_u,
                    to_u=to_u,
                    description=str(desc),
                    balance_after=balances[guest.id]
                    if guest.id in (from_u.id, to_u.id)
                    else None,
                )
            elif op_name == "withdrawal":
                from_u = payload["from"]  # type: ignore[assignment]
                amount = payload["amount"]  # type: ignore[assignment]
                desc = payload["desc"]  # type: ignore[assignment]
                assert isinstance(from_u, User)
                balances[from_u.id] -= amount
                refresh_accounts()
                create_tx(
                    tx_type="withdrawal",
                    amount=amount,
                    from_u=from_u,
                    to_u=None,
                    description=str(desc),
                    balance_after=balances[guest.id],
                )

        refresh_accounts()

    seeded = Transaction.objects.filter(sandbox_ledger_q(guest, peers)).count()
    if seeded != 10:
        msg = f"Expected 10 sandbox transactions after seed, got {seeded}"
        raise RuntimeError(msg)


def is_demo_guest_user(user: User) -> bool:
    return user.get_username() == settings.DEMO_GUEST_USERNAME


def demo_peer_id_set() -> frozenset[int]:
    names = get_demo_peer_usernames()
    return frozenset(User.objects.filter(username__in=names).values_list("id", flat=True))
