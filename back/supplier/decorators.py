from django.core.exceptions import PermissionDenied
from .models import Supplier_Account


def is_supplier(function):
    def wrap(request, *args, **kwargs):
        if request.session['user_role'] == 'supplier':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def is_loggedin(function):
    def wrap(request, *args, **kwargs):
        if 'user_email' in request.session:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
