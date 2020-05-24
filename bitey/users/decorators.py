from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def is_anonymous(redirect_url):
    def is_anonymous_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.is_anonymous:
                return func(*args, **kwargs)
            else:
                return redirect(url_for(redirect_url))

        return wrapper

    return is_anonymous_wrapper


def is_activated(redirect_url):
    def is_activated_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.activated:
                return func(*args, **kwargs)
            else:
                flash('You have to activate your account to access this page.', 'info')

                return redirect(url_for(redirect_url))

        return wrapper

    return is_activated_wrapper
