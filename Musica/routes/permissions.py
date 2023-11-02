from functools import wraps
from flask import redirect, url_for, flash, session
from .welcome import current_user

# def decorator_function(f):
#     @wraps(f)
#     def wrapper_function(*args, **kwargs):
#         #check
#         return f(*args, **kwargs)
#     return wrapper_function

from functools import wraps

# def my_decorator(argument1, argument2):
#     def decorator_function(original_function):
#         @wraps(original_function)
#         def wrapper(*args, **kwargs):
#             # You can use argument1 and argument2 here
#             result = original_function(*args, **kwargs)
#             return result
#         return wrapper
#     return decorator_function

def allowed_for(list):
    def decorator(f):
        @wraps(f)
        def wrapper(*args,**kwargs):
            if session.get('role') in list:
                    return f(*args,**kwargs)
            flash('You are not allowed to access this route!','warning')
            return redirect(url_for('home'))
        return wrapper
    return decorator