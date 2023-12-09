from flask import Blueprint, render_template, request, session, redirect, current_app
from database.operations import select

from database.sql_provider import SQLProvider
import json

auth_app = Blueprint('auth_app', __name__, template_folder='templates')

sql_provider = SQLProvider('auth/sql')

def groups(login, password):
    db_config = current_app.config['DB_CONFIG']
    sql_statement = sql_provider.get('groups.sql', {'login': "'" + login + "'", 'password': "'" + password + "'"})
    res = select(db_config, sql_statement)

    return res

def log_in():
    message = ''
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        data = groups(login, password)
        if len(data)>0:
                session['vgroup'] = data[0]['vgroup']
                session['id'] = data[0]['staff_id']
                message = session['vgroup']
                print(message)
                return 'main_nav.html', message
        else:
            message = "Неверный логин или пароль"
            return 'login_form.html', message
    else:
        if 'vgroup' in session:
            message = session['vgroup']

            return 'account.html', message
        else:
            message = "Пройдите авторизацию перед работой на сайте"
            return 'login_form.html', message
    return 'login_form.html', message


@auth_app.route('/login/', methods=['GET', 'POST'])

def login_handler():
    name_html, message = log_in()
    if name_html == 'main_nav.html':
        return  render_template(name_html, message=message)
    else:
        return render_template(name_html, message=message)


@auth_app.route('/logout/')
def logout_handler():
    session.pop('vgroup', None)
    return redirect('/auth/login/')


@auth_app.route('/authentication')
def authentication_handler(): pass


@auth_app.route('/register')
def register_handler(): pass





