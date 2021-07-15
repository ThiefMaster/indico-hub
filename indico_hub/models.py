import uuid

from flask import json
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.types import VARCHAR, TypeDecorator

from .db import db





class Instance(db.Model):
    __tablename__ = 'instances'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # TODO: Implement a model that resembles a registered Indico instance
    uuid = db.Column(UUID(as_uuid=True), default=lambda: str(uuid.uuid4()))
    url = db.Column(db.String, nullable=False)
    contact = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    organization = db.Column(db.String, nullable=False)
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    geolocation = db.Column(JSONB)
    registration_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Instance {self.id} {self.url}>'
