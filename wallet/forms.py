from decimal import Decimal

from django import forms
from django.conf import settings
from django.contrib.auth.models import User

from wallet.demo_sandbox import get_demo_peer_usernames, is_demo_guest_user


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
            if is_demo_guest_user(self.user):
                names = get_demo_peer_usernames()
                # Only show the demo peer users to the demo guest user
                self.fields["to_user"].queryset = User.objects.filter(username__in=names).order_by(
                    "username"
                )
            else:
                demo_names = [settings.DEMO_GUEST_USERNAME, *get_demo_peer_usernames()]
                # Exclude the demo users from the recipient selection
                self.fields["to_user"].queryset = (
                    User.objects.exclude(id=self.user.id).exclude(username__in=demo_names).order_by("username")
                )

    def clean_amount(self):
        "Custom validation for the transfer amount"
        amount = self.cleaned_data.get("amount")

        # Check if the user has enough balance
        if self.user and self.user.account.balance < amount:
            raise forms.ValidationError(f" balance: Your current balance is ${self.user.account.balance:.2f}.")
        return amount
