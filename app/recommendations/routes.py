from datetime import datetime
from typing import Any
from flask import Blueprint, render_template, request, redirect, url_for, g, session, flash, abort
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy

from .. import db, login_required
from ..models import Recommendation, Tag, FictionType, User
from .forms import PostUpdateRecommendationForm
from .crud import get_fiction_type_by_name, get_tag_by_name, get_recommendation_by_id

bp = Blueprint(
    name='recommendations',
    import_name=__name__
)


def parse_tags(tags: str) -> list[str]:
    tags = tags.strip()
    new_tags_list = []

    tags_list = tags.split(',')
    for tag in tags_list:
        if tag.isspace():
            pass
        elif not tag:
            pass
        else:
            new_tags_list.append(tag.lower())

    for index, tag in enumerate(new_tags_list):
        tag: str = tag.strip()
        tag = '-'.join(tag.split(' '))
        new_tags_list[index] = tag

    return new_tags_list


def get_tags_objects(tags_list: list[str]) -> list[Tag]:
    tags_objects_list = []
    for tag in tags_list:
        tag_object = get_tag_by_name(name=tag)
        if tag_object:
            tags_objects_list.append(tag_object)
        else:
            new_tag_object = Tag(name=tag)
            tags_objects_list.append(new_tag_object)

    return tags_objects_list


def get_fiction_type_object(name: str) -> FictionType:
    name = name.strip().lower()
    fiction_type_object = get_fiction_type_by_name(name=name)
    if fiction_type_object:
        return fiction_type_object
    fiction_type_object = FictionType(name=name,
                                      slug=name.replace(' ', '-'))
    return fiction_type_object


class PostRecommendation(MethodView):
    methods = ['GET', 'POST']

    def __init__(self) -> None:
        self.form_class = PostUpdateRecommendationForm
        self.template_name = 'recommendations/post_recommendation.html'
        self.success_message = 'You successfully posted new recommendation!'
        self.info_message = 'To create a recommendation, you need to be an authenticated user.'

    def get(self):
        current_user: User = g.user
        if not current_user:
            flash(message=self.info_message, category='info')
            return redirect(url_for('main.index'))
        form = self.form_class()
        return render_template(self.template_name, form=form)

    def post(self):
        form = self.form_class(request.form)
        current_user: User = g.user
        if not current_user:
            flash(message=self.info_message, category='info')
            return redirect(url_for('main.index'))
        if form.validate_on_submit():
            fiction_type = get_fiction_type_object(
                name=form.fiction_type.data)
            new_recommendation = Recommendation(
                title=form.title.data,
                short_description=form.short_description.data,
                opinion=form.opinion.data,
                user_id=current_user.id,
                fiction_type=fiction_type
            )
            tags_list = parse_tags(tags=form.tags.data)
            tags_objects_list = get_tags_objects(tags_list=tags_list)
            new_recommendation.tags = tags_objects_list
            db.session.add(new_recommendation)
            db.session.commit()
            flash(message=self.success_message, category='success')
            return redirect(url_for('recommendations.recommendation_detail', id=new_recommendation.id))
        return render_template(self.template_name, form=form)


@bp.route('/recommendations/<int:id>/', methods=['GET'])
def recommendation_detail(id):
    recommendation = get_recommendation_by_id(id=id)
    if not recommendation:
        abort(404)

    return render_template('recommendations/recommendation_detail.html', recommendation=recommendation)


class UpdateRecommendation(MethodView):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def __init__(self) -> None:
        self.form_class = PostUpdateRecommendationForm
        self.template_name = 'recommendations/update_recommendation.html'
        self.success_message = 'You successfully updated your recommendation!'

    def get(self, id: int):
        current_user: User = g.user
        recommendation = get_recommendation_by_id(id=id)
        if not recommendation:
            abort(404)
        if recommendation.user != current_user:
            abort(403)
        tags = [tag.name for tag in recommendation.tags]
        tags = ', '.join(tags)
        form = self.form_class(title=recommendation.title,
                               fiction_type=recommendation.fiction_type,
                               opinion=recommendation.opinion,
                               short_description=recommendation.short_description,
                               tags=tags)
        return render_template(self.template_name, form=form, recommendation=recommendation)

    def post(self, id: int):
        current_user: User = g.user
        recommendation = get_recommendation_by_id(id=id)
        if not recommendation:
            abort(404)
        if recommendation.user != current_user:
            abort(403)
        form = self.form_class(formdata=request.form)
        if form.validate_on_submit():
            fiction_type = get_fiction_type_object(name=form.fiction_type.data)
            recommendation.title = form.title.data
            recommendation.short_description = form.short_description.data
            recommendation.opinion = form.opinion.data
            recommendation.fiction_type = fiction_type
            recommendation.updated = datetime.utcnow()

            tags_list = parse_tags(tags=form.tags.data)
            tags_objects_list = get_tags_objects(tags_list=tags_list)
            recommendation.tags = tags_objects_list

            db.session.add(recommendation)
            db.session.commit()
            flash(self.success_message, category='success')
            return redirect(url_for('recommendations.recommendation_detail', id=recommendation.id))
        return render_template(self.template_name, form=form,
                               recommendation=recommendation)


class DeleteRecommendation(MethodView):
    decorators = [login_required]
    methods = ['POST']

    def __init__(self):
        self.success_message = 'You successfully deleted your recommendation!'

    def post(self, id):
        current_user: User = g.user
        recommendation = db.session.get(Recommendation, id)
        if not recommendation:
            abort(404)
        if recommendation.user != current_user:
            abort(403)
        db.session.delete(recommendation)
        db.session.commit()
        flash(self.success_message, category='success')
        return redirect(url_for('main.index'))
