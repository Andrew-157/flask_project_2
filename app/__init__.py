import functools

from flask import Flask, g, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
from sqlalchemy.orm import DeclarativeBase


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.become_user'))
        return view(**kwargs)
    return wrapped_view


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(metadata=Base.metadata)
migrate = Migrate()


def create_app(config_name: str = 'production'):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config[config_name])

    from . import models
    from .auth.urls import bp as auth_bp
    from .recommendations.urls import bp as recommendations_bp
    from .main import routes as main_routes

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_routes.bp)
    app.register_blueprint(recommendations_bp)

    return app
