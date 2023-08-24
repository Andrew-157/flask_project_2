from .routes import bp
from .routes import Register, Login, ChangeUser


bp.add_url_rule(rule='/register/',
                view_func=Register.as_view(name='register'))
bp.add_url_rule(rule='/login/',
                view_func=Login.as_view(name='login'))
bp.add_url_rule(rule='/update_profile/',
                view_func=ChangeUser.as_view('change_user'))