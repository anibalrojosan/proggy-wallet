import csv
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseBadRequest, StreamingHttpResponse
from django.views import View
from django.views.generic import TemplateView

from wallet.models import Transaction

from . import chart_payloads, services
from .forms import ReportsFilterForm


class _CsvEcho:
    """Write-only pseudo-file for csv.writer streaming."""

    def write(self, value: str) -> str:
        return value


def _flow_label_for_user(tx: Transaction, user) -> str:
    if tx.from_user_id == user.id and tx.type != "deposit":
        return "expense"
    return "income"


def _export_filename(*, date_from, date_to) -> str:
    today = datetime.now().strftime("%Y%m%d")
    if date_from and date_to:
        return f"transactions_{date_from}_{date_to}_{today}.csv"
    if date_from:
        return f"transactions_from_{date_from}_{today}.csv"
    if date_to:
        return f"transactions_until_{date_to}_{today}.csv"
    return f"transactions_{today}.csv"


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "reports/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = ReportsFilterForm(self.request.GET or None)
        user = self.request.user

        context["user_has_transactions"] = Transaction.objects.filter(Q(from_user=user) | Q(to_user=user)).exists()

        if form.is_valid():
            data = form.cleaned_data
            date_from = data.get("date_from")
            date_to = data.get("date_to")
            flow_filter = data.get("filter") or None
            tx_type = data.get("tx_type") or None
            kw = {
                "date_from": date_from,
                "date_to": date_to,
                "flow_filter": flow_filter,
                "tx_type": tx_type,
            }
            context["summary"] = services.get_user_financial_summary(user, **kw)
            monthly_rows = list(services.get_monthly_report_rows(user, **kw))
            types_qs = services.get_transaction_type_breakdown(user, **kw)
        else:
            flow_filter = None
            tx_type = None
            context["summary"] = services.get_user_financial_summary(user)
            monthly_rows = list(services.get_monthly_report_rows(user))
            types_qs = services.get_transaction_type_breakdown(user)

        type_rows = list(types_qs)
        context["monthly_volume_rows"] = monthly_rows
        context["type_breakdown_rows"] = type_rows
        context["flow_filter"] = flow_filter
        context["show_net_flow"] = not flow_filter
        context["show_type_chart"] = len(type_rows) > 1
        context["chart_monthly"] = chart_payloads.monthly_bars_chart_payload(monthly_rows, flow_filter=flow_filter)
        context["chart_types"] = chart_payloads.transaction_type_chart_payload(type_rows)

        if form.is_valid():
            context["filter_applied"] = bool(
                data.get("date_from") or data.get("date_to") or data.get("filter") or data.get("tx_type")
            )
        else:
            context["filter_applied"] = False

        context["filter_form"] = form
        return context


class TransactionCsvExportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Bind to request.GET even when empty (unlike `GET or None`, which leaves the form unbound).
        form = ReportsFilterForm(request.GET)
        if not form.is_valid():
            errors = []
            if form.non_field_errors():
                errors.extend(str(e) for e in form.non_field_errors())
            for field in form:
                for err in field.errors:
                    errors.append(f"{field.label}: {err}")
            return HttpResponseBadRequest("\n".join(errors) or "Invalid filter parameters.", content_type="text/plain")

        data = form.cleaned_data
        date_from = data.get("date_from")
        date_to = data.get("date_to")
        flow_filter = data.get("filter") or None
        tx_type = data.get("tx_type") or None
        kw = {
            "date_from": date_from,
            "date_to": date_to,
            "flow_filter": flow_filter,
            "tx_type": tx_type,
        }
        user = request.user
        qs = services.get_filtered_transactions_queryset(user, **kw)

        header = [
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

        def rows():
            writer = csv.writer(_CsvEcho())
            yield writer.writerow(header)
            for tx in qs.iterator(chunk_size=500):
                viewer_bal = tx.balance_after_for_viewer(user)
                yield writer.writerow(
                    [
                        tx.id,
                        tx.created_at.isoformat() if tx.created_at else "",
                        tx.type,
                        str(tx.amount),
                        _flow_label_for_user(tx, user),
                        tx.from_user.username if tx.from_user_id else "",
                        tx.to_user.username if tx.to_user_id else "",
                        (tx.description or "").replace("\n", " ").replace("\r", " "),
                        str(viewer_bal) if viewer_bal is not None else "",
                    ]
                )

        response = StreamingHttpResponse(rows(), content_type="text/csv; charset=utf-8")
        filename = _export_filename(date_from=date_from, date_to=date_to)
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response
