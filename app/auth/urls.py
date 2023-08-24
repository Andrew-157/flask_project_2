from .routes import bp
from .routes import Register


bp.add_url_rule(rule='/register/',
                view_func=Register.as_view('register'))