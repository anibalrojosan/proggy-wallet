from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.db.models.signals import post_save
from django.dispatch import receiver


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [CheckConstraint(condition=Q(balance__gte=0), name="balance_non_negative")]

    def __str__(self):
        return f"{self.user.username} - Balance: ${self.balance}"


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.get_or_create(user=instance)


class Transaction(models.Model):
    TRANSACTION_TYPES = [("deposit", "Deposit"), ("transfer", "Transfer"), ("withdrawal", "Withdrawal")]

    from_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sent_transactions")
    to_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="received_transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2, null=True)

    class Meta:
        constraints = [CheckConstraint(condition=Q(amount__gt=0), name="amount_positive")]

    def __str__(self):
        return f"{self.type.capitalize()} - ${self.amount} ({self.created_at.strftime('%Y-%m-%d')})"
