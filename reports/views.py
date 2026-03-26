from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from . import services
from .forms import ReportsFilterForm


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "reports/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = ReportsFilterForm(self.request.GET or None)
        user = self.request.user

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
            context["monthly_volume"] = services.get_monthly_volume_report(user, **kw)
            context["type_breakdown"] = services.get_transaction_type_breakdown(user, **kw)
        else:
            context["summary"] = services.get_user_financial_summary(user)
            context["monthly_volume"] = services.get_monthly_volume_report(user)
            context["type_breakdown"] = services.get_transaction_type_breakdown(user)

        context["filter_form"] = form
        return context
