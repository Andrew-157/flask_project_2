from sqlalchemy import select
from sqlalchemy.orm import joinedload

from .. import db
from ..models import FictionType, Tag, Recommendation


def get_fiction_type_by_name(name: str) -> FictionType | None:
    stmt = select(FictionType).where(FictionType.name == name)
    return db.session.scalar(stmt)


def get_tag_by_name(name: str) -> Tag | None:
    stmt = select(Tag).where(Tag.name == name)
    return db.session.scalar(stmt)


def get_recommendation_by_id(id: int) -> Recommendation | None:
    stmt = select(Recommendation).\
        where(Recommendation.id == id).\
        options(joinedload(Recommendation.tags),
                joinedload(Recommendation.fiction_type),
                joinedload(Recommendation.user))
    return db.session.scalars(stmt).unique().one_or_none()


def get_fiction_type_by_slug(fiction_type_slug: str) -> FictionType | None:
    stmt = select(FictionType).where(FictionType.slug == fiction_type_slug)
    return db.session.scalar(stmt)


def get_recommendations_by_fiction_type_object(fiction_type: FictionType) -> list["Recommendation"]:
    stmt = select(Recommendation).\
        where(Recommendation.fiction_type == fiction_type).\
        options(
            joinedload(Recommendation.tags),
            joinedload(Recommendation.fiction_type),
            joinedload(Recommendation.user)
    )
    return db.session.scalars(stmt).unique().all()
