from decimal import Decimal

from django import forms
from django.contrib.auth.models import User


class DepositForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.01"),  # Django will validate this using is_valid()
        label="Amount to deposit",
    )


class TransferForm(forms.Form):
    to_user = forms.ModelChoiceField(
        # .none() because we dont know the recipient yet
        queryset=User.objects.none(),
        label="Recipient",
        empty_label="Select a contact",
    )

    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal("0.01"), label="Amount to transfer")

    def __init__(self, *args, **kwargs):
        # Pop the current user from the kwargs list and validate its balance
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user:
            # Filter out the current user from the queryset
            self.fields["to_user"].queryset = User.objects.exclude(id=self.user.id)

    def clean_amount(self):
        "Custom validation for the transfer amount"
        amount = self.cleaned_data.get("amount")

        # Check if the user has enough balance
        if self.user and self.user.account.balance < amount:
            raise forms.ValidationError(f" balance: Your current balance is ${self.user.account.balance:.2f}.")
        return amount
