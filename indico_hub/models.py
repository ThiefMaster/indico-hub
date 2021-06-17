from .db import db


class Instance(db.Model):
    __tablename__ = 'instances'
    id = db.Column(db.Integer, primary_key=True)
    # TODO: Implement a model that resembles a registered Indico instance
    uuid = db.Column(db.String, unique=True, nullable=False)
    enabled = db.Column(db.Boolean, default=True, nullable=False)
    url = db.Column(db.String, nullable=False)
    contact = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    organization = db.Column(db.String, nullable=False)
    crawl_date = db.Column(db.DateTime)
    # crawled_data = db.Column(JSONEncodedDict)
    # geolocation = db.Column(JSONEncodedDict)
    registration_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Instance {self.id} {self.url}>'
