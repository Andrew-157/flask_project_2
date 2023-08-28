from .routes import bp
from .routes import PostRecommendation


bp.add_url_rule(
    '/recommend/', view_func=PostRecommendation.as_view(name='post_recommendation'))
