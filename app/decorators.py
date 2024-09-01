from functools import wraps
from flask_login import current_user
from flask import url_for, redirect


def annonymous_user(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return f(*args, **kwargs)

    return decorated_func