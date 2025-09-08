# goalgearApp/utils.py
from django.shortcuts import redirect

def user_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user' not in request.session:
            return redirect('/Login')
        return view_func(request, *args, **kwargs)
    return wrapper
