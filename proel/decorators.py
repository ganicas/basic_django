from django.core.exceptions import PermissionDenied
from django.utils.functional import wraps

from django.shortcuts import render
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect


def role_required(*roles):
    """
    Check specified role(s) and return a 403
    if user doesn't have permission to view
    based alot on: github.com/mzupan/django-decorators/blob/master/auth.py
    and: djangofoo.com/253/writing-django-decorators
    """

    def check_role(user):
        return getattr(user, 'role', None) in roles

    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            if check_role(request.user):
                return func(request, *args, **kwargs)
            else:
                response = render('403.html', RequestContext(request, {}))
                response.status_code = 403
                return response

        return wraps(func)(inner_decorator)

    return decorator


def require_access(template, action, special=False):
    """
    This decorator checks if the user is allowed to see the designated section of the website

    :param special: controls redirection to dashboard
    :param template: template
    :param action: action
    :return: raises a http-forbidden if access fails, view if it passes
    """
    def deco(fn):
        def wrapper(request, *args, **kwargs):
            user_type = request.user.user_type
            status = request.user.can_access(user_type=user_type, template=template, action=action)
            if status:
                return fn(request, *args, **kwargs)
            else:
                if special:
                    return HttpResponseRedirect('dashboard')
                raise PermissionDenied
        wrapper.__name__ = fn.__name__
        wrapper.__doc__ = fn.__doc__
        return wrapper
    return deco
