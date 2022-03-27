from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import decarators
from .forms import UserCreateForm
from .modules import send_activate_mail
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from .utils import token_generator
from .models import User, UserProfile

@login_required(login_url="login")
def home(request):
    # print(request.user.userprofile.email_confirmed)
    context = {}
    return render(request, "accounts/index.html", context)

def register(request):
    form = UserCreateForm()
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            send_activate_mail(request, user)

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

def not_email_verified(request):
    context = {}
    return render(request, "accounts/not_email_verified.html", context)

def activate_user(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user=None

    if user is not None and token_generator.check_token(user=user, token=token):
        profile = UserProfile.objects.get(user=user)
        profile.email_confirmed = True
        profile.save()

        messages.success(request, 'Email success activate')
        login(request, user)
        return redirect('home')

    context = {}
    return render(request, 'accounts/activate_user_failed.html', context)

def terms_of_service(request):
    return render(request, 'accounts/terms-of-service.html')

@login_required(login_url="login")
def permissions_management(request):
    context = {}
    return render(request, 'accounts/permissions_management.html', context)

def user_profile(request):
    context = {}
    return render(request, 'accounts/user_profile.html', context)