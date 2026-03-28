from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management import call_command
from django.db.models import Q
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from wallet.demo_sandbox import sandbox_ledger_q
from wallet.models import Account, Transaction


@override_settings(
    DEMO_GUEST_USERNAME="guest",
    DEMO_PEER_USERNAMES=["demo_peer_1", "demo_peer_2", "demo_peer_3"],
    DEMO_GUEST_PASSWORD="test-guest-password",
)
class DemoGuestSandboxTests(TestCase):
    def setUp(self) -> None:
        call_command("ensure_demo_users")

    def _guest(self) -> User:
        return User.objects.get(username="guest")

    def _peers(self) -> list[User]:
        return list(
            User.objects.filter(username__in=["demo_peer_1", "demo_peer_2", "demo_peer_3"]).order_by("username")
        )

    def test_seed_balance_and_transaction_count(self) -> None:
        guest = self._guest()
        peers = self._peers()
        self.assertEqual(len(peers), 3)
        acc = Account.objects.get(user=guest)
        self.assertEqual(acc.balance, Decimal("50000.00"))
        qs = Transaction.objects.filter(sandbox_ledger_q(guest, peers))
        self.assertEqual(qs.count(), 10)

    def test_guest_transfer_form_only_lists_peers(self) -> None:
        User.objects.create_user(username="regular_user", password="pw12345")
        guest = self._guest()
        from wallet.forms import TransferForm

        form = TransferForm(user=guest)
        qs = form.fields["to_user"].queryset
        self.assertEqual(qs.count(), 3)
        self.assertFalse(qs.filter(username="regular_user").exists())

    def test_guest_transfer_post_rejects_non_peer_recipient(self) -> None:
        regular = User.objects.create_user(username="regular_user", password="pw12345")
        guest = self._guest()
        client = Client()
        client.force_login(guest)
        before_count = Transaction.objects.filter(from_user=guest).count()
        client.post(
            reverse("transfer"),
            {"to_user": str(regular.pk), "amount": "1.00"},
        )
        self.assertEqual(Transaction.objects.filter(from_user=guest).count(), before_count)
        self.assertFalse(Transaction.objects.filter(from_user=guest, to_user=regular).exists())

    def test_regular_user_transfer_form_excludes_demo_accounts(self) -> None:
        User.objects.create_user(username="regular_user", password="pw12345")
        regular = User.objects.get(username="regular_user")
        from wallet.forms import TransferForm

        form = TransferForm(user=regular)
        usernames = set(form.fields["to_user"].queryset.values_list("username", flat=True))
        self.assertNotIn("guest", usernames)
        for name in ("demo_peer_1", "demo_peer_2", "demo_peer_3"):
            self.assertNotIn(name, usernames)

    def test_logout_removes_demo_users_from_database(self) -> None:
        guest = self._guest()
        peers = self._peers()
        guest_pk = guest.pk
        peer_pks = [p.pk for p in peers]
        client = Client()
        self.assertEqual(client.post(reverse("guest_login")).status_code, 302)
        client.post(reverse("deposit"), {"amount": "25.00"}, follow=True)
        self.assertTrue(User.objects.filter(username="guest").exists())

        client.logout()

        self.assertFalse(User.objects.filter(username="guest").exists())
        self.assertEqual(
            User.objects.filter(username__in=["demo_peer_1", "demo_peer_2", "demo_peer_3"]).count(),
            0,
        )
        self.assertFalse(
            Transaction.objects.filter(Q(from_user_id=guest_pk) | Q(to_user_id=guest_pk)).exists()
        )
        for pk in peer_pks:
            self.assertFalse(
                Transaction.objects.filter(Q(from_user_id=pk) | Q(to_user_id=pk)).exists()
            )
