import pytest
from flask import Flask
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models import User


@pytest.fixture
def app() -> Flask:

    app = create_app(config_name='testing')

    with app.app_context():
        db.create_all()
        new_user = User(username='test_user',
                        email='test_user@gmail.com',
                        password=generate_password_hash('34somepassword34'))
        db.session.add(new_user)
        db.session.commit()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app: Flask):
    return app.test_client()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self,
              username='test_user',
              password='34somepassword34'
              ):
        response = self._client.post(
            '/auth/login/', data={'username': username,
                                  'password': password}
        )


@pytest.fixture
def auth(client):
    return AuthActions(client)
