from flask import render_template

def view(sentens):
    length = len(sentens)
    print(sentens.get('args'))
    a = sentens.get('args')
    if length > 0 :
        return render_template('output_info_manager.html', item = sentens)
    else:
        return 'Не найдена'

def view_w(table_name, string):
    if len(string) > 0:
        return render_template(table_name, item = string)
    else:
        return 'Информация не найдена'