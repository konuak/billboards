from flask import render_template

def view(sentens, message):
    length = len(sentens)
    if length > 0 :
        return render_template('output_info_manager.html', item = sentens, message = message)
    else:
        return 'Не найдена'

def view_w(table_name, string):
    if len(string) > 0:
        return render_template(table_name, item = string)
    else:
        return 'Информация не найдена'

def view_m(sentens, args, message):
    length = len(sentens)
    if length > 0 :
        if args.get('type') != 'arendator' :
            type ='owner'

            return render_template('output_info_man.html', item = sentens, type = type, message = message)
        else:
            type =  'arendator'
            return render_template('output_info_man.html', item=sentens, type=type)

    else:

        return 'Не найдена'