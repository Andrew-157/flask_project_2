from flask import Blueprint, render_template, request, redirect, url_for, g, session
from flask.views import MethodView
from werkzeug.security import generate_password_hash

from .. import db
from ..models import User
from .forms import RegisterForm, LoginForm
from .crud import get_user_by_id, get_user_with_username

bp = Blueprint(name='auth', 
               import_name=__name__,
               url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_user_by_id(id=user_id)

class Register(MethodView):
    methods = ['GET', 'POST']

    def __init__(self) -> None:
        self.form_class = RegisterForm
        self.template_name = 'auth/register.html'

    def get(self):
        form = self.form_class()
        return render_template(self.template_name, form=form)
    
    def post(self):
        form = self.form_class(request.form)
        if form.validate_on_submit():
            new_user = User(username=form.username.data, 
                            email=form.email.data,
                            password=generate_password_hash(form.password1.data))
            db.session.add(new_user)
            db.session.commit()
            session.clear()
            session['user_id'] = new_user.id
            return redirect(url_for('main.index'))
        return render_template(self.template_name, form=form)
    

class Login(MethodView):
    methods = ['GET', 'POST']

    def __init__(self) -> None:
        self.form_class = LoginForm
        self.template_name = 'auth/login.html'

    def get(self):
        form = self.form_class()
        return render_template(self.template_name, form=form)
    
    def post(self):
        form = self.form_class(request.form)
        if form.validate_on_submit():
            username = form.username.data
            user = get_user_with_username(username=username)
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        return render_template(self.template_name, form=form)
    

@bp.route(rule='/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))