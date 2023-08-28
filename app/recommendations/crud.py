from sqlalchemy import select

from .. import db
from ..models import FictionType, Tag


def get_fiction_type_by_name(name: str) -> FictionType | None:
    stmt = select(FictionType).where(FictionType.name == name)
    return db.session.scalar(stmt)


def get_tag_by_name(name: str) -> Tag | None:
    stmt = select(Tag).where(Tag.name == name)
    return db.session.scalar(stmt)
