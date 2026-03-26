from datetime import timedelta

from django.db.models import Avg, Count, Q, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from wallet.models import Transaction


def _filtered_user_transactions(user, *, date_from=None, date_to=None, flow_filter=None, tx_type=None):
    """
    User-involved transactions with optional date range, flow (income/expense), and type filters.
    flow_filter matches wallet history: income = to_user only, expense = from_user only.

    Returns a queryset ready for aggregate() and annotate().
    """
    qs = Transaction.objects.filter(Q(from_user=user) | Q(to_user=user))
    if date_from is not None:
        qs = qs.filter(created_at__date__gte=date_from)
    if date_to is not None:
        qs = qs.filter(created_at__date__lte=date_to)
    if tx_type:
        qs = qs.filter(type=tx_type)
    if flow_filter == "income":
        qs = qs.filter(to_user=user)
    elif flow_filter == "expense":
        qs = qs.filter(from_user=user)
    return qs


def get_filtered_transactions_queryset(user, *, date_from=None, date_to=None, flow_filter=None, tx_type=None):
    """
    Ordered transactions for CSV export and list views; same filters as dashboard aggregates.
    """
    return (
        _filtered_user_transactions(user, date_from=date_from, date_to=date_to, flow_filter=flow_filter, tx_type=tx_type)
        .select_related("from_user", "to_user")
        .order_by("-created_at")
    )


def get_user_financial_summary(user, *, date_from=None, date_to=None, flow_filter=None, tx_type=None):
    """
    Calculates key metrics based on the user's money flow.
    Considers deposits and transfers received as inflows,
    and withdrawals and transfers sent as outflows.
    """
    base = _filtered_user_transactions(user, date_from=date_from, date_to=date_to, flow_filter=flow_filter, tx_type=tx_type)
    sent_metrics = base.filter(from_user=user).aggregate(total_sent=Sum("amount"), count_sent=Count("id"))
    received_metrics = base.filter(to_user=user).aggregate(total_received=Sum("amount"), count_received=Count("id"))

    total_sent = sent_metrics["total_sent"] or 0
    total_received = received_metrics["total_received"] or 0

    return {
        "total_outflow": total_sent,
        "total_inflow": total_received,
        "net_flow": total_received - total_sent,
        "transaction_count": (sent_metrics["count_sent"] or 0) + (received_metrics["count_received"] or 0),
    }


def get_monthly_volume_report(user, *, date_from=None, date_to=None, flow_filter=None, tx_type=None):
    """
    Returns the volume of transactions per month for the user.
    Useful for monthly activity bar charts.
    """
    user_transactions = _filtered_user_transactions(
        user, date_from=date_from, date_to=date_to, flow_filter=flow_filter, tx_type=tx_type
    )

    return (
        user_transactions.annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total_amount=Sum("amount"), count=Count("id"))
        .order_by("-month")
    )


def get_monthly_report_rows(user, *, date_from=None, date_to=None, flow_filter=None, tx_type=None):
    """
    Standardized monthly rows for tables and charts: month, inflow, outflow, count.
    When flow_filter is None, splits inflow (to_user) vs outflow (from_user) per month
    using date/type filters only (not flow), so the chart shows both series.
    When flow_filter is income or expense, amounts appear on the matching side only.
    """
    if flow_filter == "income":
        qs = get_monthly_volume_report(user, date_from=date_from, date_to=date_to, flow_filter="income", tx_type=tx_type)
        rows_inc = []
        for r in qs:
            inf = r["total_amount"] or 0
            rows_inc.append(
                {
                    "month": r["month"],
                    "inflow": inf,
                    "outflow": 0,
                    "net": inf,
                    "count": r["count"],
                }
            )
        return rows_inc
    if flow_filter == "expense":
        qs = get_monthly_volume_report(user, date_from=date_from, date_to=date_to, flow_filter="expense", tx_type=tx_type)
        rows_exp = []
        for r in qs:
            ouf = r["total_amount"] or 0
            rows_exp.append(
                {
                    "month": r["month"],
                    "inflow": 0,
                    "outflow": ouf,
                    "net": -ouf,
                    "count": r["count"],
                }
            )
        return rows_exp

    base = _filtered_user_transactions(user, date_from=date_from, date_to=date_to, flow_filter=None, tx_type=tx_type)
    in_map = {}
    for r in (
        base.filter(to_user=user)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("amount"), cnt=Count("id"))
    ):
        if r["month"] is not None:
            in_map[r["month"]] = {"inflow": r["total"] or 0, "in_cnt": r["cnt"]}
    out_map = {}
    for r in (
        base.filter(from_user=user)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("amount"), cnt=Count("id"))
    ):
        if r["month"] is not None:
            out_map[r["month"]] = {"outflow": r["total"] or 0, "out_cnt": r["cnt"]}

    all_months = sorted(set(in_map.keys()) | set(out_map.keys()), reverse=True)
    rows = []
    for m in all_months:
        i = in_map.get(m, {})
        o = out_map.get(m, {})
        inf = i.get("inflow", 0)
        ouf = o.get("outflow", 0)
        rows.append(
            {
                "month": m,
                "inflow": inf,
                "outflow": ouf,
                "net": inf - ouf,
                "count": i.get("in_cnt", 0) + o.get("out_cnt", 0),
            }
        )
    return rows


def get_transaction_type_breakdown(user, *, date_from=None, date_to=None, flow_filter=None, tx_type=None):
    """
    Break down activity by transaction type (deposit, transfer, withdrawal).
    """
    user_transactions = _filtered_user_transactions(
        user, date_from=date_from, date_to=date_to, flow_filter=flow_filter, tx_type=tx_type
    )

    return user_transactions.values("type").annotate(total=Sum("amount"), count=Count("id")).order_by("-total")


def get_balance_history(user, days=30):
    """
    Returns the final balance points of the transactions in a period.
    Useful for line charts of 'Balance Evolution'.
    """
    return (
        Transaction.objects.filter(Q(from_user=user) | Q(to_user=user))
        .order_by("created_at")
        .values("created_at", "balance_after")[:days]
    )


def get_top_transfer_partners(user):
    """
    Identifies the users with whom the user interacts most in transfers.
    """
    sent_to = (
        Transaction.objects.filter(from_user=user, type="transfer")
        .values("to_user__username")
        .annotate(total=Sum("amount"), count=Count("id"))
        .order_by("-total")
    )

    return sent_to


def get_unusual_transactions(user, threshold_multiplier=3):
    """
    Finds transactions that exceed N times the average of the user.
    """
    avg_amount = Transaction.objects.filter(from_user=user).aggregate(Avg("amount"))["amount__avg"] or 0
    if avg_amount == 0:
        return []

    return Transaction.objects.filter(from_user=user, amount__gt=avg_amount * threshold_multiplier).order_by("-amount")


def get_weekly_comparison(user):
    """
    Compares the volume of outflows this week vs the previous week.
    """
    today = timezone.now()
    this_week_start = today - timedelta(days=7)
    last_week_start = today - timedelta(days=14)

    this_week = (
        Transaction.objects.filter(from_user=user, created_at__gte=this_week_start).aggregate(Sum("amount"))["amount__sum"] or 0
    )
    last_week = (
        Transaction.objects.filter(from_user=user, created_at__range=[last_week_start, this_week_start]).aggregate(Sum("amount"))[
            "amount__sum"
        ]
        or 0
    )

    diff = this_week - last_week
    percent = (diff / last_week * 100) if last_week > 0 else 0

    return {"this_week": this_week, "last_week": last_week, "difference": diff, "percent_change": percent}
