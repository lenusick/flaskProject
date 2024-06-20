from functools import wraps
from flask import redirect
from flask_login import current_user


def permission_required(perm):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(perm):
                return redirect('/')
            return f(*args, **kwargs)

        return decorated_function

    return decorator
