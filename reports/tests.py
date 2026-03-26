import csv
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from io import StringIO

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from reports import chart_payloads, services
from wallet.models import Account, Transaction


class ChartPayloadTests(TestCase):
    def test_monthly_bars_empty(self):
        payload = chart_payloads.monthly_bars_chart_payload([], flow_filter=None)
        self.assertEqual(payload, {"labels": [], "datasets": []})

    def test_monthly_bars_split_two_datasets_chronological(self):
        may = datetime(2024, 5, 1, 12, 0, 0, tzinfo=UTC)
        june = datetime(2024, 6, 1, 12, 0, 0, tzinfo=UTC)
        rows = [
            {"month": june, "inflow": Decimal("100"), "outflow": Decimal("40"), "net": Decimal("60"), "count": 2},
            {"month": may, "inflow": Decimal("50"), "outflow": Decimal("20"), "net": Decimal("30"), "count": 1},
        ]
        payload = chart_payloads.monthly_bars_chart_payload(rows, flow_filter=None)
        self.assertEqual(payload["labels"], ["2024-05", "2024-06"])
        self.assertEqual(len(payload["datasets"]), 2)
        self.assertEqual(payload["datasets"][0]["label"], "Inflow ($)")
        self.assertEqual(payload["datasets"][0]["data"], [50.0, 100.0])
        self.assertEqual(payload["datasets"][1]["data"], [20.0, 40.0])

    def test_monthly_bars_income_single_series(self):
        june = datetime(2024, 6, 1, 12, 0, 0, tzinfo=UTC)
        rows = [{"month": june, "inflow": Decimal("80"), "outflow": 0, "net": Decimal("80"), "count": 1}]
        payload = chart_payloads.monthly_bars_chart_payload(rows, flow_filter="income")
        self.assertEqual(len(payload["datasets"]), 1)
        self.assertEqual(payload["datasets"][0]["data"], [80.0])

    def test_transaction_type_payload_labels_and_floats(self):
        rows = [
            {"type": "deposit", "total": Decimal("100.00"), "count": 2},
            {"type": "transfer", "total": Decimal("25.50"), "count": 1},
        ]
        payload = chart_payloads.transaction_type_chart_payload(rows)
        self.assertEqual(payload["labels"], ["Deposit", "Transfer"])
        self.assertEqual(payload["data"], [100.0, 25.5])

    def test_transaction_type_empty(self):
        self.assertEqual(
            chart_payloads.transaction_type_chart_payload([]),
            {"labels": [], "data": []},
        )


class GetMonthlyReportRowsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="muser", password="x")
        Account.objects.filter(user=self.user).update(balance=Decimal("2000.00"))
        self.other = User.objects.create_user(username="mother", password="x")
        Account.objects.filter(user=self.other).update(balance=Decimal("100.00"))

    def test_split_rows_inflow_outflow_same_month(self):
        Transaction.objects.create(to_user=self.user, amount=Decimal("100.00"), type="deposit", balance_after=Decimal("100"))
        Transaction.objects.create(
            from_user=self.user,
            to_user=self.other,
            amount=Decimal("30.00"),
            type="transfer",
            balance_after=Decimal("70"),
        )
        rows = services.get_monthly_report_rows(self.user)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["inflow"], Decimal("100.00"))
        self.assertEqual(rows[0]["outflow"], Decimal("30.00"))
        self.assertEqual(rows[0]["net"], Decimal("70.00"))


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


class DashboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="dashuser", password="secret123")
        Account.objects.filter(user=self.user).update(balance=Decimal("500.00"))

    def test_dashboard_redirects_when_anonymous(self):
        url = reverse("reports:dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)

    def test_dashboard_200_empty_account_omits_chart_payload_scripts(self):
        self.client.login(username="dashuser", password="secret123")
        response = self.client.get(reverse("reports:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'id="reports-monthly-data"')
        self.assertNotContains(response, 'id="chart-monthly"')

    def test_dashboard_200_with_data_includes_chart_payload_scripts(self):
        Transaction.objects.create(
            to_user=self.user,
            amount=Decimal("1.00"),
            type="deposit",
            balance_after=Decimal("1.00"),
        )
        self.client.login(username="dashuser", password="secret123")
        response = self.client.get(reverse("reports:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="reports-monthly-data"')
        self.assertContains(response, 'id="reports-types-data"')
        self.assertContains(response, "chart.js")

    def test_dashboard_filtered_no_results_hides_kpi_and_charts(self):
        Transaction.objects.create(
            to_user=self.user,
            amount=Decimal("50.00"),
            type="deposit",
            balance_after=Decimal("50.00"),
        )
        self.client.login(username="dashuser", password="secret123")
        response = self.client.get(reverse("reports:dashboard"), {"filter": "expense", "tx_type": "withdrawal"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No results for these filters")
        self.assertNotContains(response, 'id="chart-monthly"')
        self.assertNotContains(response, ">Inflow</h2>")

    def test_dashboard_single_type_hides_doughnut_canvas(self):
        Transaction.objects.create(
            to_user=self.user,
            amount=Decimal("50.00"),
            type="deposit",
            balance_after=Decimal("50.00"),
        )
        self.client.login(username="dashuser", password="secret123")
        response = self.client.get(reverse("reports:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="chart-monthly"')
        self.assertNotContains(response, 'id="chart-types"')

    def test_dashboard_two_types_shows_doughnut_canvas(self):
        other = User.objects.create_user(username="dashother", password="x")
        Account.objects.filter(user=other).update(balance=Decimal("100.00"))
        Transaction.objects.create(
            to_user=self.user,
            amount=Decimal("50.00"),
            type="deposit",
            balance_after=Decimal("50.00"),
        )
        Transaction.objects.create(
            from_user=self.user,
            to_user=other,
            amount=Decimal("10.00"),
            type="transfer",
            balance_after=Decimal("40.00"),
        )
        self.client.login(username="dashuser", password="secret123")
        response = self.client.get(reverse("reports:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="chart-types"')


def _csv_response_body(response) -> str:
    return b"".join(response.streaming_content).decode()


class TransactionCsvExportViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="csvuser", password="secret123")
        Account.objects.filter(user=self.user).update(balance=Decimal("1000.00"))
        self.other = User.objects.create_user(username="csvother", password="x")
        Account.objects.filter(user=self.other).update(balance=Decimal("500.00"))

    def test_csv_export_redirects_when_anonymous(self):
        response = self.client.get(reverse("reports:export_transactions_csv"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)

    def test_csv_export_invalid_date_range_returns_400(self):
        self.client.login(username="csvuser", password="secret123")
        response = self.client.get(
            reverse("reports:export_transactions_csv"),
            {"date_from": "2025-06-10", "date_to": "2025-06-01"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Start date", response.content)

    def test_csv_export_empty_only_header(self):
        self.client.login(username="csvuser", password="secret123")
        response = self.client.get(reverse("reports:export_transactions_csv"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv; charset=utf-8")
        self.assertIn("attachment", response["Content-Disposition"])
        lines = _csv_response_body(response).strip().splitlines()
        self.assertEqual(len(lines), 1)
        row = next(csv.reader(StringIO(lines[0])))
        self.assertEqual(row[0], "id")

    def test_csv_export_other_user_cannot_see_transactions(self):
        tx = Transaction.objects.create(
            to_user=self.user,
            amount=Decimal("99.00"),
            type="deposit",
            balance_after=Decimal("99.00"),
        )
        self.client.login(username="csvother", password="x")
        response = self.client.get(reverse("reports:export_transactions_csv"))
        self.assertEqual(response.status_code, 200)
        body = _csv_response_body(response)
        self.assertNotIn(str(tx.id), body)

    def test_csv_export_respects_tx_type_filter(self):
        Transaction.objects.create(
            to_user=self.user,
            amount=Decimal("10.00"),
            type="deposit",
            balance_after=Decimal("10.00"),
        )
        Transaction.objects.create(
            from_user=self.user,
            to_user=self.other,
            amount=Decimal("5.00"),
            type="transfer",
            balance_after=Decimal("5.00"),
        )
        self.client.login(username="csvuser", password="secret123")
        response = self.client.get(reverse("reports:export_transactions_csv"), {"tx_type": "deposit"})
        self.assertEqual(response.status_code, 200)
        reader = csv.reader(StringIO(_csv_response_body(response)))
        rows = list(reader)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1][2], "deposit")
        self.assertEqual(rows[1][4], "income")

    def test_csv_export_respects_date_range(self):
        now = timezone.now()
        old = Transaction.objects.create(
            to_user=self.user,
            amount=Decimal("1.00"),
            type="deposit",
            balance_after=Decimal("1.00"),
        )
        Transaction.objects.filter(pk=old.pk).update(created_at=now - timedelta(days=60))
        new = Transaction.objects.create(
            to_user=self.user,
            amount=Decimal("2.00"),
            type="deposit",
            balance_after=Decimal("3.00"),
        )
        Transaction.objects.filter(pk=new.pk).update(created_at=now - timedelta(days=2))
        date_from = (now - timedelta(days=7)).date().isoformat()
        date_to = now.date().isoformat()
        self.client.login(username="csvuser", password="secret123")
        response = self.client.get(
            reverse("reports:export_transactions_csv"),
            {"date_from": date_from, "date_to": date_to},
        )
        self.assertEqual(response.status_code, 200)
        reader = csv.reader(StringIO(_csv_response_body(response)))
        rows = list(reader)
        self.assertEqual(len(rows), 2)
        self.assertIn(str(new.id), rows[1][0])
