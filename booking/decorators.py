from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def staff_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        role = getattr(request.user, "role", None)
        if not (
            request.user.is_staff
            or request.user.is_superuser
            or getattr(role, "staff", False)
        ):
            raise PermissionDenied("You can`t go here")
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            raise PermissionDenied("Only for admins")
        return view_func(request, *args, **kwargs)
    return wrapper