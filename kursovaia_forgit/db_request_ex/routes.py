from flask import Blueprint, render_template, current_app, request, session
from database.operations import select
from database.sql_provider import SQLProvider
from db_request_dir.view import view, view_w
from database.connection import DBContextManager
from auth.routes import log_in
import json

from access import internal_required

db_work_ex = Blueprint('db_work_ex', __name__, template_folder='templates')
sql_provider = SQLProvider('db_request_ex/sql')

def controller(base, argument):
    args = {}
    args['request_type'] = base[base.find('/db_ex/sql/') + 11:base.rfind('/')]
    for item in argument:
        if argument[item] != '':
            args[item] = argument[item]
    return args
def bus_logic_read(db_config, args):
    sql_statement = ''
    year = args.get('year')
    id_staff = session.get('id', None)
    if session.get('vgroup',None) == 'arendator':
        sql_statement = sql_provider.get('arendator_id.sql', {'id_staff': "'" + str(id_staff) + "'"})
        res = select(db_config, sql_statement)
        id_arendator = res[0]
        id_arendator = id_arendator['Id_cont']
        if args['request_type'] == 'reports':
            sql_statement = sql_provider.get('year_report_arendator.sql', {'id_arendator': "'" + str(id_arendator) + "'"})
        if args['request_type'] == 'read_form':
            sql_statement = sql_provider.get('read_report_arendator.sql',
                                                 {'year': "'" + year + "'",
                                                  'id_arendator': "'" + str(id_arendator) + "'"})
        if args['request_type'] == 'arend_billb':
            sql_statement = sql_provider.get('arend_find.sql', {'id_arendator': "'" + str(id_arendator) + "'"})
    else :
        sql_statement = sql_provider.get('owner_id.sql', {'id_staff': "'" + str(id_staff) + "'"})
        res = select(db_config, sql_statement)
        id_owner = res[0]
        id_owner = id_owner['id_o']
        if args['request_type'] == 'reports':
            sql_statement = sql_provider.get('year_report.sql', {'id_owner': "'" + str(id_owner) + "'"})
        if args['request_type'] == 'read_form':
            sql_statement = sql_provider.get('read_report_owner.sql', {'year': "'" + year + "'", 'id_owner': "'" + str(id_owner) + "'"})
        if args['request_type'] == 'add_billb':

            if args.get('address') != None :
                with DBContextManager(current_app.config['DB_CONFIG']) as cursor:
                    size = args.get('size')
                    price = args.get('price')
                    address  = args.get('address')
                    date_build  = args.get('date_build')
                    type_bill = args.get('type')
                    sql_statement = sql_provider.get('add_new.sql', {'ido': "'" + str(id_owner) + "'",
                                                                 'size': "" + size + "",
                                                                 'price': "" + price + "",
                                                                 'address': "'" + str(address) + "'",
                                                                 'date_build': "'" + str(date_build) + "'",
                                                                 'type_bill': "'" + str(type_bill) + "'"})
                    return cursor.execute(sql_statement)
            sql_statement = sql_provider.get('find_my.sql', {'id_owner': "'" + str(id_owner) + "'"})


    return select(db_config, sql_statement)


@db_work_ex.route('sql/reports/info')
@db_work_ex.route('sql/read_form')
@internal_required()
def handler_inf2():
    connector_args = controller(request.base_url, request.args)
    result = bus_logic_read(current_app.config['DB_CONFIG'], connector_args)
    context = {"result": result}
    return render_template('read_form_ex.html', item = context)


@db_work_ex.route('sql/read_form/read', methods=['GET', 'POST'])
@internal_required()
def read_handler():
    connector_args = controller(request.base_url, request.args)
    result = bus_logic_read(current_app.config['DB_CONFIG'], connector_args)
    context = {"result": result,
               "tags": json.load(open('auth/configs/tags.json', "r", encoding='utf-8'))
               }
    return view_w('output_report_ex.html', context)

@db_work_ex.route('sql/add_billb/form', methods=['GET', 'POST'])
@db_work_ex.route('sql/arend_bill/form', methods=['GET', 'POST'])
@internal_required()
def handler_for_add():
    connector_args = controller(request.base_url, request.args)
    result = bus_logic_read(current_app.config['DB_CONFIG'], connector_args)
    if result == 1 :
        message = "Добавленный билборд на рассмотрении!"
        return render_template('add_form.html', message = message)
    context = {"result": result,
               "tags": json.load(open('auth/configs/tags.json', "r", encoding='utf-8'))
               }
    return view_w('my_billb.html', context )
@db_work_ex.route('sql/arend_billb/form', methods=['GET', 'POST'])
@internal_required()
def handler_for_add1():
    connector_args = controller(request.base_url, request.args)
    result = bus_logic_read(current_app.config['DB_CONFIG'], connector_args)
    context = {"result": result,
               "tags": json.load(open('auth/configs/tags.json', "r", encoding='utf-8'))
               }
    return view_w('arend_billb.html', context )

@db_work_ex.route('sql/add_new/form', methods=['GET', 'POST'])
@internal_required()
def handler_for_addbil():
    return render_template('add_form.html')
