from flask import Blueprint, render_template, current_app, request, session, redirect
from database.operations import select, call_proc
from database.sql_provider import SQLProvider
from db_request.view import view, view_w
import json
from access import internal_required


reports = Blueprint('reports', __name__,template_folder = 'templates', static_folder= 'static')

sql_provider = SQLProvider('reports/sql')

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

    if args['request_type'] == 'create_form1':
        sql_statement = 'report_owner'
        res = call_proc(current_app.config['DB_CONFIG'], sql_statement, year)
        return res
    else :
        sql_statement = 'report_arendator'
        res = call_proc(current_app.config['DB_CONFIG'], sql_statement, year)
        return res
def bus_logic_read(db_config, args):
    year = args.get('year')
    type = args.get('type')
    if args['request_type'] == 'read_form1':
        sql_statement = sql_provider.get('read_report_ow.sql', {'year': "'" + year + "'"})
    else :
        sql_statement = sql_provider.get('read_report_ar.sql', {'year': "'" + year + "'"})
    return select(db_config, sql_statement)

@reports.route('/info')
@internal_required()
def handler_inf():
    return render_template('reports_info.html')


@reports.route('/create_form')
@internal_required()
def handler_inf1():
    connector_args = controller(request.base_url, request.args)
    if connector_args.get('type') == "for_owner":
        result = select(current_app.config['DB_CONFIG'], sql_provider.get('year_for_create.sql', {}))
        context = {"result": result}
        type = "owner"
        return render_template('create_form.html', item=context, type = type)
    if connector_args.get('type') == "for_arendator":
        result = select(current_app.config['DB_CONFIG'], sql_provider.get('year_for_create.sql', {}))
        context = {"result": result}
        type = "arendator"
        return render_template('create_form.html', item=context, type = type)
    return render_template('create_form.html')

@reports.route('/read_form', methods=['GET', 'POST'])
@internal_required()
def handler_inf2():
    connector_args = controller(request.base_url, request.args)

    if connector_args.get('type') == "for_owner":
        result = select(current_app.config['DB_CONFIG'], sql_provider.get('year_report.sql', {}))
        context = {"result": result}
        message = "owner"
        return render_template('read_form_m.html', item=context, message = message)
    if connector_args.get('type') == "for_arendator":
        result = select(current_app.config['DB_CONFIG'], sql_provider.get('year_report_ar.sql', {}))
        context = {"result": result}
        message = "arendator"
        return render_template('read_form_m.html', item=context, message=message)

    return render_template('read_form_m.html')




@reports.route('/read_form/read', methods=['GET', 'POST'])
@internal_required()
def read_handler():
    connector_args = controller(request.base_url, request.args)
    result = bus_logic_read(current_app.config['DB_CONFIG'], connector_args)

    context = {"result": result,
               "tags": json.load(open('auth/configs/tags.json', "r", encoding='utf-8'))
               }
    return view_w('output_report_m.html', context)


@reports.route('/read_form1/read', methods=['GET', 'POST'])
@internal_required()
def read_handler3():
    connector_args = controller(request.base_url, request.args)
    result = bus_logic_read(current_app.config['DB_CONFIG'], connector_args)

    context = {"result": result,
               "tags": json.load(open('auth/configs/tags.json', "r", encoding='utf-8'))
               }
    return view_w('output_report_m.html', context)
@reports.route('/create_form/create', methods=['GET', 'POST'])
@internal_required()
def report_handler():
    connector_args = controller(request.base_url, request.args)
    print(connector_args)
    result = bus_logic_create(current_app.config['DB_CONFIG'], connector_args)
    if result == 1 :
        message = "Отчет был успешно создан!"
        return render_template('reports_info.html', message = message)
    else:
        message = "Не получилось ;("
        return render_template('reports_info.html', message = message)

@reports.route('/create_form1/create', methods=['GET', 'POST'])
@internal_required()
def report_handler1():
    connector_args = controller(request.base_url, request.args)
    result = bus_logic_create(current_app.config['DB_CONFIG'], connector_args)
    if result == 1 :
        message = "Отчет был успешно создан!"
        return render_template('reports_info.html', message = message)
    else:
        message = "Не получилось ;("
        return render_template('reports_info.html', message = message)