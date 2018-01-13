from sqlalchemy import func
from sqlalchemy.dialects import postgresql

from common import db


class Blog(db.Model):
    """This class represent blog model."""

    __tablename__ = 'blog'

    guid = db.Column(postgresql.UUID, index=True, unique=True, server_default=func.uuid_generate_v4(), primary_key=True)
    user_guid = db.Column(postgresql.UUID, index=True, nullable=False)
    title = db.Column(db.String(255), index=True, nullable=False)
    about = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)

    def __iter__(self):
        yield 'guid', self.guid
        yield 'user_guid', self.user_guid
        yield 'title', self.title
        yield 'about', self.about
        yield 'created_at', self.created_at
        yield 'updated_at', self.updated_at

    def __repr__(self):
        return '<Blog %s>' % self.title
