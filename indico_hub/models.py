import uuid

from flask import json
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import VARCHAR, TypeDecorator

from .db import db


class JSONEncodedDict(TypeDecorator):
    """
    Represents an immutable structure as a json-encoded string.
    Usage::
        JSONEncodedDict(255)
    """

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class Instance(db.Model):
    __tablename__ = 'instances'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # TODO: Implement a model that resembles a registered Indico instance
    uuid = db.Column(UUID(as_uuid=True), default=lambda: str(uuid.uuid4()))
    # enabled = db.Column(db.Boolean, default=True, nullable=False)
    url = db.Column(db.String, nullable=False)
    contact = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    organization = db.Column(db.String, nullable=False)
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    crawl_date = db.Column(db.DateTime)
    crawled_data = db.Column(JSONEncodedDict)
    geolocation = db.Column(JSONEncodedDict)
    registration_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Instance {self.id} {self.url}>'
