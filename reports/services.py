from datetime import timedelta

from django.db.models import Avg, Count, Q, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from wallet.models import Transaction


def get_user_financial_summary(user):
    """
    Calculates key metrics based on the user's money flow.
    Considers deposits and transfers received as inflows,
    and withdrawals and transfers sent as outflows.
    """
    # Transactions where the user is the sender (Outflows/Transfers sent)
    sent_metrics = Transaction.objects.filter(from_user=user).aggregate(total_sent=Sum("amount"), count_sent=Count("id"))

    # Transactions where the user is the receiver (Inflows/Transfers received)
    received_metrics = Transaction.objects.filter(to_user=user).aggregate(
        total_received=Sum("amount"), count_received=Count("id")
    )

    total_sent = sent_metrics["total_sent"] or 0
    total_received = received_metrics["total_received"] or 0

    return {
        "total_outflow": total_sent,
        "total_inflow": total_received,
        "net_flow": total_received - total_sent,
        "transaction_count": (sent_metrics["count_sent"] or 0) + (received_metrics["count_received"] or 0),
    }


def get_monthly_volume_report(user):
    """
    Returns the volume of transactions per month for the user.
    Useful for monthly activity bar charts.
    """
    # Combine sent and received transactions
    user_transactions = Transaction.objects.filter(Q(from_user=user) | Q(to_user=user))

    return (
        user_transactions.annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total_amount=Sum("amount"), count=Count("id"))
        .order_by("-month")
    )


def get_transaction_type_breakdown(user):
    """
    Break down activity by transaction type (deposit, transfer, withdrawal).
    """
    user_transactions = Transaction.objects.filter(Q(from_user=user) | Q(to_user=user))

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
    # Sent transfers grouped by the receiver
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
