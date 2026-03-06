from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Transaction

@login_required
def menu(request):
    return render(request, 'menu.html')

@login_required
def deposit(request):
    return render(request, 'deposit.html')

@login_required
def transfer(request):
    # List other users as contacts
    contacts = User.objects.exclude(id=request.user.id)
    return render(request, 'sendmoney.html', {'contacts': contacts})

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
