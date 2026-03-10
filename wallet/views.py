from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.db.models import Q

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
                        balance_after=account.balance,
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
                        balance_after=from_account.balance,
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
    '''
    View to display the user's transaction history. 
    It uses the Django Paginator to divide the queryset into groups of 10 transactions.
    '''
    # Capture the filter type from the URL (e.g: ?filter=income)
    filter_type = request.GET.get('filter')

    # Filter the transactions where the user is the sender or receiver.
    queryset = Transaction.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user)
    ).order_by('-created_at')

    # Filter logic for the "My Movements" buttons
    if filter_type == 'income':
        queryset = queryset.filter(to_user=request.user)
    elif filter_type == 'expense':
        queryset = queryset.filter(from_user=request.user)

    # Pagination: Divide the queryset into groups of 10 transactions.
    paginator = Paginator(queryset, 10) 
    
    # Get the current page number from the URL (e.g: ?page=2)
    page_number = request.GET.get('page')
    
    # Get the page object
    page_obj = paginator.get_page(page_number)

    # Return the 'page_obj' instead of 'transactions'
    return render(request, 'transactions.html', {
        'page_obj': page_obj,
        'current_filter': filter_type  # Useful to highlight the active button in the frontend
    })
