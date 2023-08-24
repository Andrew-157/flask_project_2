from .routes import bp
from .routes import Register, Login


bp.add_url_rule(rule='/register/',
                view_func=Register.as_view(name='register'))
bp.add_url_rule(rule='/login/',
                view_func=Login.as_view(name='login'))