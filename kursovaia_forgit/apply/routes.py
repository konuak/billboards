from flask import Blueprint, render_template, current_app, request, session, redirect
from database.operations import select, call_proc
from database.sql_provider import SQLProvider
from database.connection import DBContextManager
from db_request.view import view, view_w
import json
from access import internal_required

apply = Blueprint('apply', __name__,template_folder = 'templates', static_folder= 'static')

sql_provider = SQLProvider('apply/sql')

def controller(base, argument):
    args = {}
    args['request_type'] = base[base.find('/reports/') + 9:base.rfind('/')]
    for item in argument:
        if argument[item] != '':
            args[item] = argument[item]

    return args

def bus_logic_create(db_config, args):
    year = args.get('year')
    type = args.get('type')
    if type == 'for_owner':
        sql_statement = 'report_owner'
    else :
        sql_statement = 'report_arendator'
    p = call_proc(current_app.config['DB_CONFIG'], sql_statement, year)
    return call_proc(current_app.config['DB_CONFIG'],sql_statement ,year)

def bus_logic_apply(db_config, args):
    with DBContextManager(current_app.config['DB_CONFIG']) as cursor:
        id = args.get('approved')
        sql_statement = sql_provider.get('update_status.sql', {'id': "'" + id + "'"})
        return cursor.execute(sql_statement)

@apply.route('/', methods=['GET', 'POST'])
def choose():
    sql_code = sql_provider.get('bills_app.sql', {})
    print(sql_code)
    items = select(current_app.config['DB_CONFIG'], sql_code)
    args = controller(request.base_url, request.args)
    print(args)
    res = bus_logic_apply(current_app.config['DB_CONFIG'], args)
    print(res)
    return render_template('choose.html', items =  items)