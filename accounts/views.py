from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserCreateForm
from .modules import custom_send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from datetime import datetime
from .utils import token_generator
from .models import User, UserProfile

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
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(request, username=username, password=password)
            context = {
                "username": username, 
                "domain": get_current_site(request),
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": token_generator.make_token(user),
            }
            print(context)
            custom_send_mail(
                subject="Register Success Inform", 
                receivers=[email],
                html_template="accounts/email_activate.html",
                context=context
                )

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

def send_activate_mail(user, request):    

    email_body = render_to_string(
        template_name="accounts/activate.html",
        context={
            "username": user.username,
            "domain": get_current_site(request),
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": token_generator._make_hash_value(user, datetime.now()) 
        }
    )
    print(email_body)

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
        return redirect('login')

    context = {}
    return render(request, 'accounts/activate_user_failed.html', context)