from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from . import services


@login_required
def dashboard_view(request):
    # Consume the service layer
    summary = services.get_user_financial_summary(request.user)
    monthly_volume = services.get_monthly_volume_report(request.user)
    type_breakdown = services.get_transaction_type_breakdown(request.user)

    context = {
        "summary": summary,
        "monthly_volume": monthly_volume,
        "type_breakdown": type_breakdown,
    }
    return render(request, "reports/dashboard.html", context)
