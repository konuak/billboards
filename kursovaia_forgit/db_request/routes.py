from flask import Blueprint, render_template, current_app, request, session, redirect
from database.operations import select
from database.sql_provider import SQLProvider
from db_request.view import view, view_w, view_m
from auth.routes import log_in
import json

from access import internal_required

db_work = Blueprint('db_work', __name__, template_folder='templates')
sql_provider = SQLProvider('db_request/sql')

@db_work.route('/sql/info')
@internal_required()
def auth_find():
    #message = session['vgroup']
    return render_template('info.html')

def BLogic_data(url_base_line, url_args_dict):
    args = {}
    args['request_type'] = url_base_line[url_base_line.find('/sql/info/') + 10:url_base_line.rfind('')]
    if args['request_type'] == 'find_id/shop/' or args['request_type'] == 'find_id/stuff/':
        args['request_type'] = url_base_line[url_base_line.find('/sql/info/find_id') + 18:url_base_line.rfind('/')]
    elif args['request_type'] == 'for_arendator/'  :
        args['request_type'] = url_base_line[url_base_line.find('/sql/info/for_arendator/') + 10:url_base_line.rfind('/')]
    elif args['request_type'] == 'for_arendator/find'  :
        args['request_type'] = url_base_line[url_base_line.find('/sql/info/for_arendator/find') + 10:url_base_line.rfind('/')]
    elif args['request_type'] == 'for_manager/find'  :
        args['request_type'] = url_base_line[url_base_line.find('/sql/info/for_manager/find') + 10:url_base_line.rfind('/')]

    for item in url_args_dict:
        if url_args_dict[item] != '':
            args[item] = url_args_dict[item]
    return args

def bus_logic(db_config, args):
    sql_statement = ''
    if args['request_type'] == 'for_arendator':
            sql_statement = sql_provider.get('dif_all_bill.sql', {})
    elif args['request_type'] == 'for_arendator/find/' :
        if  args.get('billid', None) == None:
            if  args.get('min_quality', None) != None and args.get('max_quality', None) != None :
                max_quality = args.get('max_quality', None)
                min_quality = args.get('min_quality', None)
                sql_statement = sql_provider.get('dif_bill_search_qualit.sql', {'max_quality' : "'" + max_quality + "'", 'min_quality' : "'" + min_quality + "'"})

            elif args.get('min_price', None) != None and args.get('max_price', None) != None :
                max_price = args.get('max_price', None)
                min_price = args.get('min_price', None)
                sql_statement = sql_provider.get('dif_bill_search_price.sql',{'max_price' : "'" + max_price + "'", 'min_price' : "'" + min_price + "'"})
            else:
                sql_statement = sql_provider.get('dif_all_bill.sql', {})

        elif args.get('billid', None) != None:
            idbill = args.get('billid', None)
            sql_statement = sql_provider.get('dif_bill_search.sql', {'idbill': "'" + idbill + "'"})
    elif args['request_type'] == 'for_manager/find/':
        if args.get('surname_a', None) != None:
            surname = args.get('surname_a', None)
            sql_statement = sql_provider.get('dif_a_search.sql', {'surname': "'" + str(surname) + "'"})
            res = select(db_config, sql_statement)
            return res
        elif args.get('phone_a', None) != None:
            phone = args.get('phone_a', None)
            sql_statement = sql_provider.get('dif_phonea_search.sql', {'phone': "'" + phone + "'"})
            res = select(db_config, sql_statement)
            return res
        elif args.get('birth_a', None) != None:
            birth = args.get('birth_a', None)
            sql_statement = sql_provider.get('dif_birtha_search.sql', {'birthday': "'" + str(birth) + "'"})
            res = select(db_config, sql_statement)
            return res
        elif args.get('id_cont', None) != None:
            id = args.get('id_cont', None)
            sql_statement = sql_provider.get('dif_arendator_id.sql', {'id_cont': "'" + id + "'"})
            res = select(db_config, sql_statement)
            return res
        sql_statement = sql_provider.get('dif_all_arendator.sql', {})
        res = select(db_config, sql_statement)
        return res
    if args['request_type'] == 'for_manager1/find/':
        if args.get('surname_o', None) != None:
            surname = args.get('surname_o', None)
            sql_statement = sql_provider.get('dif_o_search.sql', {'surname': "'" + str(surname) + "'"})
            res = select(db_config, sql_statement)
            return res
        elif args.get('phone_o', None) != None:
            phone = args.get('phone_o', None)
            sql_statement = sql_provider.get('dif_phone_search.sql', {'phone': "'" + phone + "'"})
            res = select(db_config, sql_statement)
            return res
        elif args.get('birth_o', None) != None:
            birth = args.get('birth_o', None)
            sql_statement = sql_provider.get('dif_birtho_search.sql', {'birthday': "'" + str(birth) + "'"})
            res = select(db_config, sql_statement)
            return res
        sql_statement = sql_provider.get('dif_all_owner.sql', {})
        res = select(db_config, sql_statement)
        return res
    res = select(db_config, sql_statement)
    return res

@db_work.route('/sql/info/for_arendator/' )
@db_work.route('/sql/info/for_arendator/find/' )
@internal_required()
def sql_request_handler44():
    b_logic_args = BLogic_data(request.base_url, request.args)
    result = bus_logic(current_app.config['DB_CONFIG'], b_logic_args)
    if result == []:
        message = "Такой билборд не найден :("
    else :
        message = ''
    context = {"result": result, "title": "title",
               "tags": json.load(open('auth/configs/tags.json', "r", encoding='utf-8'))}
    return view(context, message)

@db_work.route('/sql/info/for_manager/' )
@internal_required()
def sql_request_handler45():
    return render_template("output_info_manager_1.html")

@db_work.route('/sql/info/for_manager/find/' )
@db_work.route('/sql/info/for_manager1/find/' )
@internal_required()
def sql_request_handler456():
    b_logic_args = BLogic_data(request.base_url, request.args)
    print(b_logic_args.get('type') )
    if b_logic_args.get('type') == 'owner':
        return redirect('/db/sql/info/for_manager1/find/')
    result = bus_logic(current_app.config['DB_CONFIG'], b_logic_args)
    if result == []:
        message = "Такой пользователь не найден :("
    else :
        message = ''
    context = {"result": result, "title": "title",
               "tags": json.load(open('auth/configs/tags.json', "r", encoding='utf-8'))}
    return view_m(context, b_logic_args, message)





def controller(base, argument):
    args = {}
    args['request_type'] = base[base.find('/reports/') + 9:base.rfind('/')]
    for item in argument:
        if argument[item] != '':
            args[item] = argument[item]
    return args

def bus_logic_read(db_config, args):
    year = args.get('year')
    id_staff = session.get('id', None)
    sql_statement = sql_provider.get('owner_id.sql', {'id_staff': "'" + str(id_staff) + "'"})
    res = select(db_config, sql_statement)
    id_owner = res[0]
    id_owner = id_owner['id_o']
    if args['request_type'] == 'read_form':
        sql_statement = sql_provider.get('read_report_ow.sql', {'year': "'" + year + "'", 'id_owner': "'" + str(id_owner) + "'"})
    return select(db_config, sql_statement)
