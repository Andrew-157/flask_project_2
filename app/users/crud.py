from sqlalchemy import select

from .. import db
from ..models import User

def get_user_by_id(id: int) -> User:
    return db.session.get(User, id)


def get_user_with_username(username: str) -> User | None:
    stmt = select(User).where(User.username==username)
    return db.session.scalar(stmt)


def get_user_with_email(email: str) -> User | None:
    stmt = select(User).where(User.email==email)
    return db.session.scalar(stmt)