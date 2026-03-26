"""
Build Chart.js-friendly payloads (JSON-serializable) from ORM aggregate rows.
"""

from decimal import Decimal

from wallet.models import Transaction

_TYPE_LABEL = dict(Transaction.TRANSACTION_TYPES)

_INFLOW_BG = "rgba(25, 135, 84, 0.55)"
_INFLOW_BORDER = "rgba(25, 135, 84, 1)"
_OUTFLOW_BG = "rgba(220, 53, 69, 0.55)"
_OUTFLOW_BORDER = "rgba(220, 53, 69, 1)"
_SINGLE_BG = "rgba(13, 110, 253, 0.5)"
_SINGLE_BORDER = "rgba(13, 110, 253, 1)"


def _to_float(value):
    if value is None:
        return 0.0
    if isinstance(value, Decimal):
        return float(value)
    return float(value)


def monthly_bars_chart_payload(rows, *, flow_filter=None):
    """
    rows: list of dicts with month, inflow, outflow, count (from get_monthly_report_rows).
    Returns labels + datasets for grouped bars (inflow + outflow) or a single series when flow is filtered.
    """
    if not rows:
        return {"labels": [], "datasets": []}
    asc = sorted(rows, key=lambda r: r.get("month") or 0)
    labels = []
    for row in asc:
        month = row.get("month")
        if month is not None and hasattr(month, "strftime"):
            labels.append(month.strftime("%Y-%m"))
        else:
            labels.append("")
    datasets = []
    if flow_filter == "income":
        datasets.append(
            {
                "label": "Inflow ($)",
                "data": [_to_float(r.get("inflow")) for r in asc],
                "backgroundColor": _INFLOW_BG,
                "borderColor": _INFLOW_BORDER,
            }
        )
    elif flow_filter == "expense":
        datasets.append(
            {
                "label": "Outflow ($)",
                "data": [_to_float(r.get("outflow")) for r in asc],
                "backgroundColor": _OUTFLOW_BG,
                "borderColor": _OUTFLOW_BORDER,
            }
        )
    else:
        datasets.append(
            {
                "label": "Inflow ($)",
                "data": [_to_float(r.get("inflow")) for r in asc],
                "backgroundColor": _INFLOW_BG,
                "borderColor": _INFLOW_BORDER,
            }
        )
        datasets.append(
            {
                "label": "Outflow ($)",
                "data": [_to_float(r.get("outflow")) for r in asc],
                "backgroundColor": _OUTFLOW_BG,
                "borderColor": _OUTFLOW_BORDER,
            }
        )
    return {"labels": labels, "datasets": datasets}


def transaction_type_chart_payload(rows):
    """rows: iterable of dicts with keys type, total, count."""
    labels = []
    data = []
    for row in rows:
        key = row.get("type") or ""
        labels.append(_TYPE_LABEL.get(key, key.replace("_", " ").title() or "Unknown"))
        data.append(_to_float(row.get("total")))
    return {"labels": labels, "data": data}
