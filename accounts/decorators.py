from django.core.exceptions import PermissionDenied


def user_is_vendor(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_vendor:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


def user_is_customer(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_customer:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_superuser(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap
