from functools import wraps
from flask_login import current_user
from flask import abort


def role_required(role):
    """Decorator function for ensuring only authorised users access a certain page"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            elif not current_user.type == role:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator
