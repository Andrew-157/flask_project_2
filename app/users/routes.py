import functools

from flask import Blueprint, render_template, request, redirect, url_for, g, session, flash
from flask.views import MethodView
from werkzeug.security import generate_password_hash

from .. import db, login_required
from ..models import User
from .forms import RegisterForm, LoginForm, ChangeUserForm
from .crud import get_user_by_id, get_user_with_username

bp = Blueprint(name='users',
               import_name=__name__)


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
        self.template_name = 'users/register.html'
        self.success_message = 'You successfully registered.'

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
            flash(self.success_message, category='success')
            return redirect(url_for('main.index'))
        return render_template(self.template_name, form=form)


class Login(MethodView):
    methods = ['GET', 'POST']

    def __init__(self) -> None:
        self.form_class = LoginForm
        self.template_name = 'users/login.html'
        self.success_message = 'Welcome Back!'

    def get(self):
        form = self.form_class()
        return render_template(self.template_name, form=form)

    def post(self):
        form = self.form_class(request.form)
        if form.validate_on_submit():
            username = form.username.data
            user = get_user_with_username(username=username)
            session['user_id'] = user.id
            flash(self.success_message, category='success')
            return redirect(url_for('main.index'))
        return render_template(self.template_name, form=form)


@bp.route(rule='/auth/logout/')
def logout():
    session.clear()
    flash('You successfully logged out.', category='success')
    return redirect(url_for('main.index'))


class ChangeUser(MethodView):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def __init__(self) -> None:
        self.form_class = ChangeUserForm
        self.template_name = 'users/change_user.html'
        self.success_message = 'You successfully updated your profile.'

    def get(self):
        current_user: User = g.user
        form = self.form_class(username=current_user.username,
                               email=current_user.email)
        return render_template(self.template_name, form=form)

    def post(self):
        current_user: User = g.user
        form = self.form_class(request.form)
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.add(current_user)
            db.session.commit()
            flash(self.success_message, category='success')
            return redirect(url_for('main.index'))
        return render_template(self.template_name, form=form)


@bp.route(rule='/auth/authenticate/', methods=['GET'])
def become_user():
    return render_template('users/become_user.html')
