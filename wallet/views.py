from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import DepositForm, TransferForm
from .models import Transaction


@login_required
def menu(request):
    return render(request, 'menu.html')

@login_required
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
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
                        type='deposit',
                        description='Deposit via web'
                    )
                messages.success(request, f'Successfully deposited ${amount}!')
                return redirect('menu')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = DepositForm()

    return render(request, 'deposit.html', {'form': form})

@login_required
def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST, user=request.user)
        if form.is_valid():
            to_user = form.cleaned_data['to_user']
            amount = form.cleaned_data['amount']

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
                        type='transfer',
                        description=f'Transfer to {to_user.username}'
                    )
                messages.success(request, f'Successfully sent ${amount} to {to_user.username}!')
                return redirect('menu')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            # If form is invalid, errors will be shown in the template
            pass
    else:
        form = TransferForm(user=request.user)

    return render(request, 'sendmoney.html', {'form': form})

@login_required
def history(request):
    # Fetch transactions where user is sender or receiver
    transactions = Transaction.objects.filter(
        from_user=request.user
    ) | Transaction.objects.filter(
        to_user=request.user
    )
    transactions = transactions.order_by('-created_at')
    return render(request, 'transactions.html', {'transactions': transactions})
