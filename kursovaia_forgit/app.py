import json
from flask import Flask, render_template, session

from auth.routes import auth_app

from db_request.routes import db_work
from access import internal_required
from reports.routes import reports
from db_request_dir.routes import db_work_dir
from db_request_ex.routes import db_work_ex
from basket.routes import basket_bp
from apply.routes import apply
app = Flask(__name__)

app.register_blueprint(db_work, url_prefix='/db')
app.config['DB_CONFIG'] = json.load(open('configs/db.json'))
app.register_blueprint(db_work_dir, url_prefix='/db_dir')
app.register_blueprint(reports, url_prefix='/reports')
app.register_blueprint(db_work_ex, url_prefix='/db_ex')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(basket_bp, url_prefix='/basket')
app.register_blueprint(apply, url_prefix='/apply')
app.config['access_config'] = json.load(open('configs/access_config.json'))

app.secret_key = 'elliss'



@app.route('/', methods=['GET', 'POST'])
@internal_required()
def index():
    message = session['vgroup']
    return render_template('main_nav.html', message = message)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5004)
