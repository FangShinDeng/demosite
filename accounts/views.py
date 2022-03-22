from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreateForm
from django.contrib.auth.decorators import login_required

# Create your views here.
# login/ [name='login']
# logout/ [name='logout']
# password_change/ [name='password_change']
# password_change/done/ [name='password_change_done']
# password_reset/ [name='password_reset']
# password_reset/done/ [name='password_reset_done']
# reset/<uidb64>/<token>/ [name='password_reset_confirm']
# reset/done/ [name='password_reset_complete']


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