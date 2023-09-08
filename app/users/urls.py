from .routes import bp
from .routes import Register, Login, ChangeUser


bp.add_url_rule(rule='/auth/register/',
                view_func=Register.as_view(name='register'))
bp.add_url_rule(rule='/auth/login/',
                view_func=Login.as_view(name='login'))
bp.add_url_rule(rule='/auth/update_profile/',
                view_func=ChangeUser.as_view(name='change_user'))
