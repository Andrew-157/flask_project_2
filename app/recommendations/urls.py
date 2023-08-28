from .routes import bp
from .routes import PostRecommendation, UpdateRecommendation, DeleteRecommendation


bp.add_url_rule(
    '/recommend/', view_func=PostRecommendation.as_view(name='post_recommendation'))
bp.add_url_rule('/recommendations/<int:id>/update/',
                view_func=UpdateRecommendation.as_view(name='update_recommendation'))
bp.add_url_rule('/recommendations/<int:id>/delete',
                view_func=DeleteRecommendation.as_view(name='delete_recommendation'))
