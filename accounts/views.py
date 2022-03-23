from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserCreateForm
from . import models
from django.db.models.signals import post_save
from django.dispatch import receiver

@login_required(login_url="login")
def home(request):
    context = {}
    return render(request, "accounts/dashboard.html", context)

def register(request):
    form = UserCreateForm()
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for user: ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, "accounts/register.html", context)

def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # if models.UserProfile.objects.get(user_id=request.user.id)
                
            if not user.userprofile.email_confirmed:
                return redirect('not_email_verified')

            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or password is incorrect')
            # return render(request, "accounts/login.html", context)
    context = {}
    return render(request, "accounts/login.html", context)


def logout_view(request):
    logout(request)
    return redirect('login')

def email_verify(request):
    context = {}
    return render(request, "accounts/email_verify.html", context)

def not_email_verified(request):
    context = {}
    return render(request, "accounts/not_email_verified.html", context)