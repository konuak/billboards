from flask import Blueprint, render_template, current_app, request, session
from database.operations import select
from database.sql_provider import SQLProvider
from db_request_dir.view import view, view_w
from auth.routes import log_in
import json

from access import internal_required

db_work_dir = Blueprint('db_work_dir', __name__, template_folder='templates')
sql_provider = SQLProvider('db_request_dir/sql')


def controller(base, argument):
    args = {}
    args['request_type'] = base[base.find('/db_dir/sql/') + 12:base.rfind('/')]
    for item in argument:
        if argument[item] != '':
            args[item] = argument[item]
    return args
def bus_logic_read(db_config, args):
    sql_statement = ''
    year = args.get('year')
    type = args.get('type')
    if type == 'for_owner':
        sql_statement = sql_provider.get('read_report_ow.sql', {'year': "'" + year + "'"})
    else :
        sql_statement = sql_provider.get('read_report_ar.sql', {'year': "'" + year + "'"})
    return select(db_config, sql_statement)


@db_work_dir.route('sql/reports/info')
@db_work_dir.route('sql/read_form')
@internal_required()
def handler_inf2():
    connector_args = controller(request.base_url, request.args)
    if connector_args.get('type') == "for_owner":
        result = select(current_app.config['DB_CONFIG'], sql_provider.get('year_report.sql', {}))
        context = {"result": result}
        message = "owner"
        return render_template('read_form.html', item=context, message = message)
    if connector_args.get('type') == "for_arendator":
        result = select(current_app.config['DB_CONFIG'], sql_provider.get('year_reportar.sql', {}))
        context = {"result": result}
        message = "arendator"
        return render_template('read_form.html', item=context, message = message)

    return render_template('read_form.html')


@db_work_dir.route('sql/read_form/reads', methods=['GET', 'POST'])
@internal_required()
def read_handler():
    connector_args = controller(request.base_url, request.args)
    result = bus_logic_read(current_app.config['DB_CONFIG'], connector_args)
    context = {"result": result,
               "tags": json.load(open('auth/configs/tags.json', "r", encoding='utf-8'))
               }
    return view_w('output_report.html', context)

