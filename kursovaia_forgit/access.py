import typing as t
from functools import wraps

from flask import request, session, current_app, render_template, redirect


def group_validation(config: dict):
    endpoint_app = request.endpoint.split('.')[0]
    if 'vgroup' in session:
        group = session['vgroup']
        if group in config and endpoint_app in config[group]:
            return True
    return False

def internal_required():
    def login_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            is_group = session.get("vgroup", False)
            if is_group:
                if group_validation(current_app.config['access_config']):
                    result = func(*args, **kwargs)
                    return result
                else:
                    message = "Упс, вы не имеете прав доступа к этой странице :("
                    return render_template('error_form.html', message = message)
            else:
                message = "Пожалуйста, пройдите авторизацию!"
                return render_template('error_form.html', message=message)
        return wrapper
    return login_wrapper


