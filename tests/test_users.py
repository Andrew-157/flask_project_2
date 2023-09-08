import pytest
from flask import Flask, Response, g, session
from werkzeug.security import generate_password_hash

from app.users.crud import get_user_with_username
from app.models import User
from app import db
from .conftest import AuthActions


def test_register(client, app: Flask):
    response: Response = client.get('/auth/register/')
    assert response.status_code == 200
    response: Response = client.post('/auth/register/',
                                     data={'username': 'new_user',
                                           'email': 'new_user@gmail.com',
                                           'password1': '34somepassword34',
                                           'password2': '34somepassword34'})
    messages = None
    with client.session_transaction() as session:
        messages = dict(session['_flashes'])
    assert response.status_code == 302
    assert response.headers['Location'] == '/'
    assert messages['success'] == 'You successfully registered.'
    with client:
        client.get('/')
        user = get_user_with_username(username='new_user')
        assert user is not None
        assert g.user.id == user.id


@pytest.mark.parametrize(
    ('username', 'email', 'password1', 'password2', 'message'),
    (
        ('new_user*', 'new_user@gmail.com', '34somepassword34', '34somepassword34',
         b'Username is not valid.Letters, digits and @/./+/-/_ only.'),
        ('new_user', 'ne', '34somepassword34',
         '34somepassword34', b'Invalid email address.'),
        ('new_user', 'new_user@gmail.com', '123', '1235',
         b'Field must be between 8 and 255 characters long.'),
        ('new_user', 'new_user@gmail.com', '34somepassword34',
         '43somepassword43', b'Passwords did not match.'),
        ('test_user', 'new_user@gmail.com',
         '34somepassword34', '34somepassword34', b'A user with this username already exists.'),
        ('new_user', 'test_user@gmail.com', '34somepassword34', '34somepassword34',
         b'A user with this email already exists.')
    )
)
def test_register_validate_input(client, username, email, password1, password2, message):
    response: Response = client.post('/auth/register/',
                                     data={'username': username,
                                           'email': email,
                                           'password1': password1,
                                           'password2': password2})
    assert response.status_code == 200
    assert message in response.data


def test_register_with_empty_data(client):
    response: Response = client.post('/auth/register/', data={})
    assert response.status_code == 200
    error_message = b'This field is required.'
    assert error_message in response.data
    assert response.data.count(error_message) == 4


def test_register_with_no_data(client):
    response: Response = client.post('/auth/register/', data=None)
    assert response.status_code == 200
    error_message = b'This field is required.'
    assert error_message in response.data
    assert response.data.count(error_message) == 4


def test_login(client):
    response: Response = client.get('/auth/login/')
    assert response.status_code == 200
    response = client.post('/auth/login/',
                           data={'username': 'test_user',
                                 'password': '34somepassword34'})
    with client.session_transaction() as session:
        messages = dict(session['_flashes'])
    assert response.status_code == 302
    assert response.headers['Location'] == '/'
    assert messages['success'] == 'Welcome Back!'
    with client:
        client.get('/')
        test_user = get_user_with_username(username='test_user')
        assert g.user.id == test_user.id


@pytest.mark.parametrize(
    ('username', 'password', 'message'),
    (
        ('noone', 'ransompassword', b'This username was not found.'),
        ('test_user', 'wrongpassword', b'Wrong password.')
    )
)
def test_login_validate_input(client, username, password, message):
    response: Response = client.post('/auth/login/',
                                     data={'username': username,
                                           'password': password})
    assert response.status_code == 200
    assert message in response.data


def test_login_with_empty_data(client):
    response: Response = client.post('/auth/login/',
                                     data={})
    assert response.status_code == 200
    error_message = b'This field is required.'
    assert error_message in response.data
    assert response.data.count(error_message) == 2


def test_login_with_no_data(client):
    response: Response = client.post('/auth/login/',
                                     data=None)
    assert response.status_code == 200
    error_message = b'This field is required.'
    assert error_message in response.data
    assert response.data.count(error_message) == 2


def test_logout_by_not_logged_user(client):
    response: Response = client.get('/auth/logout/')
    assert response.status_code == 302
    assert response.headers['Location'] == '/'
    with client.session_transaction() as session:
        messages = dict(session['_flashes'])
    assert messages['success'] == 'You successfully logged out.'


def test_logout_by_logged_user(client, auth: AuthActions):
    auth.login()
    response: Response = client.get('/auth/logout/')
    assert response.status_code == 302
    assert response.headers['Location'] == '/'
    with client.session_transaction() as session:
        messages = dict(session['_flashes'])
    assert messages['success'] == 'You successfully logged out.'
    with client:
        assert 'user_id' not in session


def test_become_user_route(client):
    response: Response = client.get('/auth/authenticate/')
    assert response.status_code == 200
    assert b'Register' in response.data
    assert b'Login' in response.data


def test_change_user(client, auth: AuthActions):
    login = auth.login()
    response: Response = client.get('/auth/update_profile/')
    assert response.status_code == 200
    response: Response = client.post('/auth/update_profile/',
                                     data={'username': 'test_user1',
                                           'email': 'test_user1@gmail.com'})
    with client.session_transaction() as session:
        messages = dict(session['_flashes'])
    assert response.status_code == 302
    assert response.headers["Location"] == '/'
    assert messages['success'] == 'You successfully updated your profile.'
    with client:
        client.get('/')
        assert g.user.username == 'test_user1'
        assert g.user.email == 'test_user1@gmail.com'


@pytest.mark.parametrize(
    ('username', 'email', 'message'),
    (
        ('test_user*', 'test_user@gmail.com',
         b'Username is not valid.Letters, digits and @/./+/-/_ only.'),
        ('test_user', 'ghjkjh', b'Invalid email address.'),
        ('random_name', 'test_user@gmail.com',
         b'A user with this username already exists.'),
        ('test_user', 'random_email@gmail.com',
         b'A user with this email already exists.')
    )
)
def test_change_user_validate_input(app: Flask, client, auth: AuthActions, username, email, message):
    user = User(username='random_name',
                email='random_email@gmail.com',
                password=generate_password_hash("34somepassword34"))
    with app.app_context():
        db.session.add(user)
        db.session.commit()
    auth.login()
    response: Response = client.post('/auth/update_profile/',
                                     data={'username': username,
                                           'email': email})
    assert response.status_code == 200
    assert message in response.data


def test_change_user_with_empty_data(client, auth: AuthActions):
    auth.login()
    response: Response = client.post('/auth/update_profile/',
                                     data={})
    assert response.status_code == 200
    error_message = b'This field is required.'
    assert error_message in response.data
    assert response.data.count(error_message) == 2


def test_change_user_with_no_data(client, auth: AuthActions):
    auth.login()
    response: Response = client.post('/auth/update_profile/',
                                     data=None)
    assert response.status_code == 200
    error_message = b'This field is required.'
    assert error_message in response.data
    assert response.data.count(error_message) == 2


def test_change_user_for_not_logged_user(client):
    response: Response = client.get('/auth/update_profile/')
    assert response.status_code == 302
    assert response.headers['Location'] == '/auth/authenticate/'
    response: Response = client.post('/auth/update_profile/')
    assert response.status_code == 302
    assert response.headers['Location'] == '/auth/authenticate/'
