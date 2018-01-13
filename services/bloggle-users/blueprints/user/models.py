from sqlalchemy import func, event
from sqlalchemy.dialects import postgresql
from werkzeug.security import generate_password_hash, check_password_hash

from common import db


class User(db.Model):
    """This class represent user model."""

    __tablename__ = 'user'

    guid = db.Column(postgresql.UUID, index=True, unique=True, server_default=func.uuid_generate_v4(), primary_key=True)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(32), nullable=True)
    last_name = db.Column(db.String(32), nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        """Set user password"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check user password"""
        return check_password_hash(self.password, password)

    def __iter__(self):
        yield 'guid', self.guid
        yield 'email', self.email
        yield 'first_name', self.first_name
        yield 'last_name', self.last_name
        yield 'created_at', self.created_at
        yield 'updated_at', self.updated_at

    def __repr__(self):
        return '<User %s>' % self.email
