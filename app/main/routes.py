from flask import Blueprint, render_template, session, g


bp = Blueprint(name='main', import_name=__name__)



@bp.route(rule='/', methods=['GET'])
def index():
    return render_template('main/index.html')