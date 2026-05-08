from django.shortcuts import redirect
from django.http import HttpResponse


def unauthenticated_user(view_func):

    def wrapper_func(request, *args, **kwargs):

        if request.user.is_authenticated:

            return redirect('dashboard')

        else:

            return view_func(
                request,
                *args,
                **kwargs
            )

    return wrapper_func

# Prevents logged-in users from seeing : login page, signup page

from django.http import HttpResponse


def allowed_roles(allowed_roles=[]):

    def decorator(view_func):

        def wrapper_func(request, *args, **kwargs):

            role = request.user.profile.role

            if role in allowed_roles:

                return view_func(
                    request,
                    *args,
                    **kwargs
                )

            return HttpResponse(
                "Unauthorized"
            )

        return wrapper_func

    return decorator