from sqlalchemy import func
from sqlalchemy.dialects import postgresql

from common import db


class Comment(db.Model):
    """This class represent comment model."""

    __tablename__ = 'comment'

    guid = db.Column(postgresql.UUID, index=True, unique=True, server_default=func.uuid_generate_v4(), primary_key=True)
    post_guid = db.Column(postgresql.UUID, index=True, nullable=False)
    user_guid = db.Column(postgresql.UUID, index=True, nullable=False)
    body = db.Column(db.Text, nullable=True)
    reply_to_guid = db.Column(postgresql.UUID, index=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)

    reply_to = db.relationship('Comment', backref=db.backref('replies', lazy=True))

    def __iter__(self):
        yield 'guid', self.guid
        yield 'post_guid', self.post_guid
        yield 'user_guid', self.user_guid
        yield 'body', self.body
        yield 'reply_to_guid', self.reply_to_guid
        yield 'created_at', self.created_at
        yield 'updated_at', self.updated_at

    def __repr__(self):
        return '<Comment %s>' % self.guid
