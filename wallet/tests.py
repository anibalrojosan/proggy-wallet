from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from wallet.models import Account, Transaction


class WalletIntegrityTest(TestCase):
    def setUp(self):
        """Set up a test user and account."""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.account = Account.objects.create(user=self.user, balance=Decimal('100.00'))

    def test_layer_5_model_validation_negative_balance(self):
        """Layer 5: Test that MinValueValidator prevents negative balance in Python."""
        self.account.balance = Decimal('-10.00')
        with self.assertRaises(ValidationError):
            # full_clean() triggers the validators (Layer 5)
            self.account.full_clean()

    def test_layer_6_db_constraint_negative_balance(self):
        """Layer 6: Test that CheckConstraint prevents negative balance in the DB."""
        # Bypass full_clean() and try to save directly to trigger the DB error
        with self.assertRaises(IntegrityError):
            Account.objects.filter(id=self.account.id).update(balance=Decimal('-50.00'))

    def test_layer_5_transaction_positive_amount(self):
        """Layer 5: Test that Transaction amount must be at least 0.01."""
        invalid_tx = Transaction(
            from_user=self.user,
            amount=Decimal('0.00'),
            type='withdrawal'
        )
        with self.assertRaises(ValidationError):
            invalid_tx.full_clean()

    def test_layer_6_db_constraint_transaction_amount(self):
        """Layer 6: Test that DB rejects zero or negative transaction amounts."""
        with self.assertRaises(IntegrityError):
            Transaction.objects.create(
                from_user=self.user,
                amount=Decimal('-5.00'),
                type='deposit'
            )

    def test_valid_transaction_flow(self):
        """Test that a valid transaction works correctly."""
        tx = Transaction.objects.create(
            to_user=self.user,
            amount=Decimal('50.00'),
            type='deposit'
        )
        self.assertEqual(tx.amount, Decimal('50.00'))
        self.assertEqual(Transaction.objects.count(), 1)
