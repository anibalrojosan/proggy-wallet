from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def menu(request):
    return render(request, 'menu.html', {'user': request.user})