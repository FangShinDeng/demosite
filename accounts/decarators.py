from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def emailconfirm_required(func_view):
    def wrapper(request, *args, **kwargs):
        if not request.user.userprofile.email_confirmed:
            return redirect('not_email_verified')
        else:
            return func_view(request, *args, **kwargs)
    return wrapper

def allowed_users(allowed_roles=[]):
    def decarators(view_func):
        def wrapper(request, *args, **kwargs):
            group = None
            if request.users.groups.exists():
                group = request.users.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()
                
            # return view_func(request, *args, **kwargs)
        return wrapper
    return decarators