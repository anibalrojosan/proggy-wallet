from django import forms

from wallet.models import Transaction


class ReportsFilterForm(forms.Form):
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    filter = forms.ChoiceField(
        label="Flow",
        choices=[("", "All"), ("income", "Income"), ("expense", "Expense")],
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    tx_type = forms.ChoiceField(
        label="Transaction type",
        choices=[("", "All types"), *Transaction.TRANSACTION_TYPES],
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def clean(self):
        cleaned = super().clean()
        date_from = cleaned.get("date_from")
        date_to = cleaned.get("date_to")
        if date_from and date_to and date_from > date_to:
            raise forms.ValidationError("Start date must be on or before end date.")
        return cleaned
