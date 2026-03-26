from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import ListView

from .forms import DepositForm, TransferForm
from .models import Transaction


@login_required
def menu(request):
    return render(request, "wallet/menu.html")


@login_required
def deposit(request):
    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            try:
                with transaction.atomic():
                    # Update account balance
                    account = request.user.account
                    account.balance += amount
                    account.save()

                    # Create transaction record
                    Transaction.objects.create(
                        to_user=request.user,
                        amount=amount,
                        type="deposit",
                        balance_after=account.balance,
                        description="Deposit via web",
                    )
                messages.success(request, f"Successfully deposited ${amount}!")
                return redirect("menu")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = DepositForm()

    return render(request, "wallet/deposit.html", {"form": form})


@login_required
def transfer(request):
    if request.method == "POST":
        form = TransferForm(request.POST, user=request.user)
        if form.is_valid():
            to_user = form.cleaned_data["to_user"]
            amount = form.cleaned_data["amount"]

            try:
                with transaction.atomic():
                    # 1. Deduct from sender
                    from_account = request.user.account
                    from_account.balance -= amount
                    from_account.save()

                    # 2. Add to receiver
                    to_account = to_user.account
                    to_account.balance += amount
                    to_account.save()

                    # 3. Create transaction record
                    Transaction.objects.create(
                        from_user=request.user,
                        to_user=to_user,
                        amount=amount,
                        type="transfer",
                        balance_after=from_account.balance,
                        balance_after_to_user=to_account.balance,
                        description=f"Transfer to {to_user.username}",
                    )
                messages.success(request, f"Successfully sent ${amount} to {to_user.username}!")
                return redirect("menu")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            # If form is invalid, errors will be shown in the template
            pass
    else:
        form = TransferForm(user=request.user)

    return render(request, "wallet/sendmoney.html", {"form": form})


class TransactionHistoryView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "wallet/transactions.html"
    # Must not be "page_obj" — that name is reserved for Django's pagination Page object.
    context_object_name = "movements"
    paginate_by = 10

    def get_queryset(self):
        # Get the base queryset (all transactions of the user)
        queryset = Transaction.objects.filter(Q(from_user=self.request.user) | Q(to_user=self.request.user)).order_by(
            "-created_at"
        )

        # Apply the filter if it exists in the URL
        filter_type = self.request.GET.get("filter")
        if filter_type == "income":
            queryset = queryset.filter(to_user=self.request.user)
        elif filter_type == "expense":
            queryset = queryset.filter(from_user=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        # Pass 'current_filter' to the template for the buttons
        context = super().get_context_data(**kwargs)
        context["current_filter"] = self.request.GET.get("filter")
        return context
