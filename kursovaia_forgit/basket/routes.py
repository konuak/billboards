from flask import Blueprint, request, render_template, current_app, session, redirect
from database.sql_provider import SQLProvider
from database.operations import select
from database.connection import DBContextManager
import redis, time
from datetime import datetime
from access import internal_required
basket_bp = Blueprint('basket',
                    __name__,
                    template_folder='Templates',
                    static_folder='static'
)


sql_provider = SQLProvider('basket/sql')
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


def controller(base, argument):
    args = {}
    args['request_type'] = base[base.find('/reports/') + 9:base.rfind('/')]
    for item in argument:
        if argument[item] != '':
            args[item] = argument[item]
    return args
def redis_insert():
        connector_args = controller(request.base_url, request.args)
        start_date = connector_args.get('start_date', None)
        end_date = connector_args.get('end_date', None)
        session['start_ar'] = start_date
        session['end_ar'] = end_date
        if start_date is not None and end_date is not None:
            year_s, month_s = start_date.split('-')
            year_e, month_e = end_date.split('-')
            sql_code = sql_provider.get('all_items.sql', {'year': year_s, 'month': month_s})
            session['year_s'] = year_s
            session['month_s'] = month_s
            session['year_e'] = year_e
            session['month_e'] = month_e
            items = select(current_app.config['DB_CONFIG'], sql_code)

            for item in items:
                r.hset(item['id_bill'], 'id_bill', item['id_bill'])
                r.hset(item['id_bill'], 'quality', item['quality'])
                r.hset(item['id_bill'], 'price', item['price'])
                r.hset(item['id_bill'], 'size', item['size'])
                r.hset(item['id_bill'], 'type_bill', item['type_bill'])
                r.hset(item['id_bill'], 'address', item['address'])
                r.expire(item['id_bill'], 60)
            return items
        else:
            sql_code = sql_provider.get('all_items.sql', {})
            items = select(current_app.config['DB_CONFIG'], sql_code)
            for item in items:
                r.hset(item['id_bill'], 'id_bill', item['id_bill'])
                r.hset(item['id_bill'], 'quality', item['quality'])
                r.hset(item['id_bill'], 'price', item['price'])
                r.hset(item['id_bill'], 'size', item['size'])
                r.hset(item['id_bill'], 'type_bill', item['type_bill'])
                r.hset(item['id_bill'], 'address', item['address'])
                r.expire(item['id_bill'], 60)
            return items

@basket_bp.route('/', methods=['GET', 'POST'])
@internal_required()
def basket_index():
    message = ''
    if 'message' in session:
        message = session['message']
        session.pop('message')
        session.pop('basket')
    items = redis_insert()
    basket = session.get('basket', {})
    if request.method == 'POST':
        id_bill = request.form['id_bill']
        item_id = '1'
        if 'item_id' in session :
            item_id = str(int(session['item_id'])+1)
        item_address = request.form['address']
        item_data = request.form['date_ords']
        m = item_data
        start_date, end_date = m.split(', ')
        year_e, month_e = end_date.split('-')
        year_s, month_s = start_date.split('-')
        if (int(year_e) - int(year_s)) == 0:
            months_passed = int(month_e) - int(month_s) +1
        elif (int(year_e) - int(year_s)) > 0 :
            months_passed = (12 - int(month_s)+ 1)+ (int(year_e) - int(year_s) - 1)*12 + int(month_e)
        item_price =  int(request.form['price'])*months_passed
        basket[item_id] = { 'id_bill': id_bill, 'price': item_price, 'address' : item_address,  'start_ar': item_data }
        session['basket'] = basket
        session['item_id'] = item_id
        return redirect('/basket/')
    current_date = str(datetime.now().date())
    return render_template('basket_index.html', items = items, basket = basket,  message = message, date = current_date)

@basket_bp.route('/clear', methods=['GET', 'POST'])
@internal_required()
def basket_clear():
    if 'basket' in session :
        session.pop('basket')
    return redirect('/basket')


@basket_bp.route('/buy')
@internal_required()
def buy_basket():
    basket = session.get('basket', {})
    if basket:
        with DBContextManager(current_app.config['DB_CONFIG']) as cursor:
            item_ids = [item_id for item_id in basket]
            id_bills = []
            for i in item_ids:
                id_bills.append(basket[i]['id_bill'])
            total_summa = 0
            for i in item_ids:
                total_summa += basket[i]['price']
            item_ids = ','.join(item_ids)
            id_bills = ','.join(id_bills)
            sql_code = sql_provider.get('item_by_id.sql', {'item_ids':id_bills})
            cursor.execute(sql_code)
            schema = [col[0] for col in cursor.description]
            item_descriptions = [dict(zip(schema, row)) for row in cursor.fetchall()]
            #for item_description in item_descriptions:

                #n_inserts = int(basket[str(item_description['id_bill'])]['count'])
               # if n_inserts > 1 :
                   # message = "Один из билбордов уже занят"
                   # session['message'] = message
                   # return redirect('/basket')
            current_date = str(datetime.now().date())
            id_staff = session['id']
            sql_statement = sql_provider.get('arendator_id.sql', {'id_staff': "'" + str(id_staff) + "'"})
            res = select(current_app.config['DB_CONFIG'], sql_statement)
            id_arendator = res[0]
            id_arendator = id_arendator['Id_cont']
            sql_order = sql_provider.get('create_order.sql', { 'total_summa': total_summa, 'date_ord' :"'" + str(current_date) + "'", 'Id_cont' : id_arendator})
            cursor.execute(sql_order)
            order_id = cursor.lastrowid
            for item_description in item_descriptions:
                m = basket[i]['start_ar']
                start_date, end_date = m.split(', ')
                end_date = end_date +"-01"
                start_date = start_date + "-01"
                sql_detail = sql_provider.get('create_order_details.sql', {'order_id': order_id,
                                                                           'ym_start': "'" + str(start_date) + "'",
                                                                           'ym_end': "'" + str(end_date) + "'",
                                                                           'idbill': item_description['id_bill'],
                                                                           'price': item_description['price']
                                                                           })
                cursor.execute(sql_detail)
                #r.hset(str(item_description['prod_id']), "count", n_left)
                #sql_code = sql_provider.get('update_storage.sql', {'n_left': n_left, 'item_id': item_description['prod_id']})
                message = "Заказ был успешно создан!"
                session['message'] = message
    return  redirect('/basket')
