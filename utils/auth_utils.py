# utils/auth_utils.py
from functools import wraps

from flask import session, jsonify


def is_user_in_group(group_name):
    """Check if the logged-in user belongs to a given group."""
    if 'user_info' in session:
        user_groups = session['user_info'].get('groups', [])
        return group_name in user_groups
    return False

def kitchen_role_required(f):
    """
    Decorator to ensure the user has the 'kitchen' role.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_user_in_group('lsit-ken3239/roles/restaurant/kitchen'):
            return jsonify({"error": "You do not have permission to access this resource"}), 403
        return f(*args, **kwargs)
    return decorated_function

def customer_role_required(f):
    """
    Decorator to ensure the user has the 'customer' role.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_user_in_group('lsit-ken3239/roles/restaurant/customer'):
            return jsonify({"error": "You do not have permission to access this resource"}), 403
        return f(*args, **kwargs)
    return decorated_function

def waiter_role_required(f):
    """
    Decorator to ensure the user has the 'waiter' role.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_user_in_group('lsit-ken3239/roles/restaurant/waiter'):
            return jsonify({"error": "You do not have permission to access this resource"}), 403
        return f(*args, **kwargs)
    return decorated_function