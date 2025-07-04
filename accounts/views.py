from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
import sweetify

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
