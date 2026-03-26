from decimal import Decimal
from io import StringIO

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.management import CommandError, call_command
from django.db import IntegrityError
from django.db.models import Max, Q
from django.test import TestCase

from wallet.models import Account, Transaction


class WalletIntegrityTest(TestCase):
    def setUp(self):
        """Set up a test user and account."""
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.account = self.user.account
        self.account.balance = Decimal("100.00")
        self.account.save(update_fields=["balance"])

    def test_layer_5_model_validation_negative_balance(self):
        """Layer 5: Test that MinValueValidator prevents negative balance in Python."""
        self.account.balance = Decimal("-10.00")
        with self.assertRaises(ValidationError):
            # full_clean() triggers the validators (Layer 5)
            self.account.full_clean()

    def test_layer_6_db_constraint_negative_balance(self):
        """Layer 6: Test that CheckConstraint prevents negative balance in the DB."""
        # Bypass full_clean() and try to save directly to trigger the DB error
        with self.assertRaises(IntegrityError):
            Account.objects.filter(id=self.account.id).update(balance=Decimal("-50.00"))

    def test_layer_5_transaction_positive_amount(self):
        """Layer 5: Test that Transaction amount must be at least 0.01."""
        invalid_tx = Transaction(from_user=self.user, amount=Decimal("0.00"), type="withdrawal")
        with self.assertRaises(ValidationError):
            invalid_tx.full_clean()

    def test_layer_6_db_constraint_transaction_amount(self):
        """Layer 6: Test that DB rejects zero or negative transaction amounts."""
        with self.assertRaises(IntegrityError):
            Transaction.objects.create(from_user=self.user, amount=Decimal("-5.00"), type="deposit")

    def test_valid_transaction_flow(self):
        """Test that a valid transaction works correctly."""
        tx = Transaction.objects.create(to_user=self.user, amount=Decimal("50.00"), type="deposit")
        self.assertEqual(tx.amount, Decimal("50.00"))
        self.assertEqual(Transaction.objects.count(), 1)


class SeedDemoCommandTests(TestCase):
    def test_seed_demo_creates_expected_transactions(self):
        user = User.objects.create_user(username="seedtarget", password="x")
        out = StringIO()
        call_command(
            "seed_demo",
            username="seedtarget",
            count=10,
            seed=1,
            reset_balances=True,
            initial_balance=Decimal("10000.00"),
            stdout=out,
        )
        n = Transaction.objects.filter(Q(from_user=user) | Q(to_user=user)).count()
        self.assertEqual(n, 10)
        self.assertIn("Created 10", out.getvalue())

    def test_seed_demo_second_run_appends_after_latest_timestamp(self):
        User.objects.create_user(username="seedappend", password="x")
        call_command(
            "seed_demo",
            username="seedappend",
            count=2,
            seed=1,
            reset_balances=True,
            initial_balance=Decimal("5000.00"),
        )
        first_max = Transaction.objects.aggregate(m=Max("created_at"))["m"]
        call_command("seed_demo", username="seedappend", count=1, seed=2)
        latest = Transaction.objects.latest("created_at").created_at
        self.assertGreater(latest, first_max)

    def test_seed_demo_requires_existing_user(self):
        out = StringIO()
        with self.assertRaises(CommandError):
            call_command("seed_demo", username="nonexistent_seed_user", count=1, stdout=out)
