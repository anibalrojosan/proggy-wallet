from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from reports import services
from wallet.models import Account, Transaction


class ReportServicesFilterTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="repuser", password="x")
        Account.objects.filter(user=self.user).update(balance=Decimal("1000.00"))
        self.other = User.objects.create_user(username="other", password="x")
        Account.objects.filter(user=self.other).update(balance=Decimal("100.00"))

    def test_financial_summary_respects_date_range(self):
        now = timezone.now()
        tx_old = Transaction.objects.create(
            to_user=self.user, amount=Decimal("10.00"), type="deposit", balance_after=Decimal("10")
        )
        Transaction.objects.filter(pk=tx_old.pk).update(created_at=now - timedelta(days=30))
        tx_new = Transaction.objects.create(
            to_user=self.user, amount=Decimal("20.00"), type="deposit", balance_after=Decimal("30")
        )
        Transaction.objects.filter(pk=tx_new.pk).update(created_at=now - timedelta(days=1))

        date_from = (now - timedelta(days=7)).date()
        date_to = now.date()
        summary = services.get_user_financial_summary(self.user, date_from=date_from, date_to=date_to)
        self.assertEqual(summary["total_inflow"], Decimal("20.00"))
        self.assertEqual(summary["transaction_count"], 1)

    def test_financial_summary_expense_filter_excludes_incoming(self):
        Transaction.objects.create(
            to_user=self.user,
            amount=Decimal("100.00"),
            type="deposit",
            balance_after=Decimal("100"),
        )
        Transaction.objects.create(
            from_user=self.user,
            to_user=self.other,
            amount=Decimal("40.00"),
            type="transfer",
            balance_after=Decimal("60"),
        )

        summary = services.get_user_financial_summary(self.user, flow_filter="expense")
        self.assertEqual(summary["total_inflow"], Decimal("0"))
        self.assertEqual(summary["total_outflow"], Decimal("40.00"))

    def test_transaction_type_filter_limits_breakdown(self):
        Transaction.objects.create(to_user=self.user, amount=Decimal("10.00"), type="deposit", balance_after=Decimal("10"))
        Transaction.objects.create(
            from_user=self.user,
            to_user=self.other,
            amount=Decimal("5.00"),
            type="transfer",
            balance_after=Decimal("5"),
        )

        rows = list(services.get_transaction_type_breakdown(self.user, tx_type="deposit"))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["type"], "deposit")
