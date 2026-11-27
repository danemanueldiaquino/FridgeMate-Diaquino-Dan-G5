from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def role_required(role):

    def decorator(view_func):

        @login_required
        def wrapper(request, *args, **kwargs):

            if role == 'manager':
                allowed = getattr(request.user, 'is_fridge_manager', False)
            else:
                allowed = request.user.role == role

            if not allowed:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator