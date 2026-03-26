from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView

from wallet.models import Transaction

from . import chart_payloads, services
from .forms import ReportsFilterForm


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
