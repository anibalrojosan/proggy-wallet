from django import template

register = template.Library()


@register.filter
def viewer_balance_after(tx, user):
    """Return the stored balance snapshot for `user` on this transaction row."""
    if tx is None or user is None:
        return None
    return tx.balance_after_for_viewer(user)
