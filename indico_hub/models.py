from .db import db


class Instance(db.Model):
    __tablename__ = 'instances'
    id = db.Column(db.Integer, primary_key=True)
    # TODO: Implement a model that resembles a registered Indico instance
    contact = db.Column(db.String(255))
    email = db.Column(db.String(255))
    organization = db.Column(db.String(255))