import csv
import io
from datetime import UTC, datetime, timedelta
from decimal import Decimal

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


EXPECTED_CSV_HEADER = [
    "id",
    "created_at",
    "type",
    "amount",
    "flow",
    "from_username",
    "to_username",
    "description",
    "balance_after",
]


def _parse_csv_response(response):
    text = response.content.decode("utf-8")
    rows = list(csv.reader(io.StringIO(text)))
    return rows[0], rows[1:]


class TransactionCsvExportViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="csvuser", password="secret123")
        Account.objects.filter(user=self.user).update(balance=Decimal("1000.00"))

    def test_export_redirects_when_anonymous(self):
        response = self.client.get(reverse("reports:export"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)

    def test_export_invalid_date_range_returns_400(self):
        self.client.login(username="csvuser", password="secret123")
        response = self.client.get(
            reverse("reports:export"),
            {"date_from": "2025-06-10", "date_to": "2025-06-01"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"date", response.content.lower())

    def test_export_empty_transactions_header_only(self):
        self.client.login(username="csvuser", password="secret123")
        response = self.client.get(reverse("reports:export"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/csv", response["Content-Type"])
        self.assertIn("attachment", response["Content-Disposition"])
        self.assertIn("transactions_export.csv", response["Content-Disposition"])
        header, data_rows = _parse_csv_response(response)
        self.assertEqual(header, EXPECTED_CSV_HEADER)
        self.assertEqual(len(data_rows), 0)

    def test_export_user_isolation_excludes_other_users_transactions(self):
        user_b = User.objects.create_user(username="csvuser_b", password="x")
        user_c = User.objects.create_user(username="csvuser_c", password="x")
        Account.objects.filter(user=user_b).update(balance=Decimal("500.00"))
        Account.objects.filter(user=user_c).update(balance=Decimal("500.00"))

        tx_a = Transaction.objects.create(
            to_user=self.user,
            amount=Decimal("25.00"),
            type="deposit",
            balance_after=Decimal("25.00"),
        )
        tx_bc = Transaction.objects.create(
            from_user=user_b,
            to_user=user_c,
            amount=Decimal("99.00"),
            type="transfer",
            balance_after=Decimal("1.00"),
        )

        self.client.login(username="csvuser", password="secret123")
        response = self.client.get(reverse("reports:export"))
        self.assertEqual(response.status_code, 200)
        _, data_rows = _parse_csv_response(response)
        ids_exported = {int(row[0]) for row in data_rows}
        self.assertIn(tx_a.id, ids_exported)
        self.assertNotIn(tx_bc.id, ids_exported)

    def test_export_expense_filter_matches_service_queryset(self):
        other = User.objects.create_user(username="csvpeer", password="x")
        Account.objects.filter(user=other).update(balance=Decimal("100.00"))
        Transaction.objects.create(
            to_user=self.user,
            amount=Decimal("100.00"),
            type="deposit",
            balance_after=Decimal("100.00"),
        )
        Transaction.objects.create(
            from_user=self.user,
            to_user=other,
            amount=Decimal("40.00"),
            type="transfer",
            balance_after=Decimal("60.00"),
        )

        kw = {"flow_filter": "expense"}
        expected_count = services.get_filtered_transactions_for_user(self.user, **kw).count()
        self.assertEqual(expected_count, 1)

        self.client.login(username="csvuser", password="secret123")
        response = self.client.get(reverse("reports:export"), {"filter": "expense"})
        self.assertEqual(response.status_code, 200)
        _, data_rows = _parse_csv_response(response)
        self.assertEqual(len(data_rows), expected_count)
        self.assertEqual(data_rows[0][2], "transfer")
        self.assertEqual(data_rows[0][4], "expense")

    def test_export_tx_type_deposit_only(self):
        other = User.objects.create_user(username="csvpeer2", password="x")
        Account.objects.filter(user=other).update(balance=Decimal("100.00"))
        Transaction.objects.create(
            to_user=self.user,
            amount=Decimal("10.00"),
            type="deposit",
            balance_after=Decimal("10.00"),
        )
        Transaction.objects.create(
            from_user=self.user,
            to_user=other,
            amount=Decimal("5.00"),
            type="transfer",
            balance_after=Decimal("5.00"),
        )

        kw = {"tx_type": "deposit"}
        expected_count = services.get_filtered_transactions_for_user(self.user, **kw).count()

        self.client.login(username="csvuser", password="secret123")
        response = self.client.get(reverse("reports:export"), {"tx_type": "deposit"})
        self.assertEqual(response.status_code, 200)
        _, data_rows = _parse_csv_response(response)
        self.assertEqual(len(data_rows), expected_count)
        self.assertEqual(len(data_rows), 1)
        self.assertEqual(data_rows[0][2], "deposit")

    def test_export_row_count_matches_queryset_with_multiple_transactions(self):
        other = User.objects.create_user(username="csvpeer3", password="x")
        Account.objects.filter(user=other).update(balance=Decimal("200.00"))
        Transaction.objects.create(
            to_user=self.user,
            amount=Decimal("1.00"),
            type="deposit",
            balance_after=Decimal("1.00"),
        )
        Transaction.objects.create(
            to_user=self.user,
            amount=Decimal("2.00"),
            type="deposit",
            balance_after=Decimal("3.00"),
        )
        Transaction.objects.create(
            from_user=self.user,
            to_user=other,
            amount=Decimal("0.50"),
            type="transfer",
            balance_after=Decimal("2.50"),
        )

        expected_count = services.get_filtered_transactions_for_user(self.user).count()
        self.assertEqual(expected_count, 3)

        self.client.login(username="csvuser", password="secret123")
        response = self.client.get(reverse("reports:export"))
        self.assertEqual(response.status_code, 200)
        _, data_rows = _parse_csv_response(response)
        self.assertEqual(len(data_rows), expected_count)


class TransactionFlowForUserTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="flowuser", password="x")
        Account.objects.filter(user=self.user).update(balance=Decimal("1000.00"))
        self.other = User.objects.create_user(username="flowother", password="x")
        Account.objects.filter(user=self.other).update(balance=Decimal("100.00"))

    def test_deposit_to_user_is_income(self):
        tx = Transaction.objects.create(
            to_user=self.user,
            amount=Decimal("50.00"),
            type="deposit",
            balance_after=Decimal("50.00"),
        )
        self.assertEqual(services.transaction_flow_for_user(tx, self.user), "income")

    def test_transfer_sent_is_expense(self):
        tx = Transaction.objects.create(
            from_user=self.user,
            to_user=self.other,
            amount=Decimal("10.00"),
            type="transfer",
            balance_after=Decimal("90.00"),
        )
        self.assertEqual(services.transaction_flow_for_user(tx, self.user), "expense")

    def test_self_transfer_reports_expense(self):
        tx = Transaction.objects.create(
            from_user=self.user,
            to_user=self.user,
            amount=Decimal("1.00"),
            type="transfer",
            balance_after=Decimal("99.00"),
        )
        self.assertEqual(services.transaction_flow_for_user(tx, self.user), "expense")
