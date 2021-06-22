# from marshmallow import Schema
# from webargs import fields


# TODO: Implement Marshmallow schemas for the API request data

from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from .models import Instance


"""
payload = {
        'url': BASE_URL,
        'contact': contact,
        'email': email,
        'organization': "it"
    }
"""


class InstanceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Instance
        include_relationships = True
        include_fk = True
        load_instance = True


class ValidationSchema(Schema):
    # enabled = fields.Boolean(required=True)
    url = fields.String(required=True)
    contact = fields.String(required=True)
    email = fields.Email(required=True)
    organization = fields.String(required=True)
    # crawl_date = fields.DateTime()
    # crawled_data = db.Column(JSONEncodedDict)
    # geolocation = db.Column(JSONEncodedDict)
    # registration_date = fields.DateTime(required=True)


class UpdateInstance(Schema):
    enabled = fields.Boolean()
    url = fields.String()
    contact = fields.String()
    email = fields.Email()
    organization = fields.String()

class Statistics(Schema):
    python_version = fields.String(required=True)
    indico_version = fields.String(required=True)
    operating_system = fields.String(required=True)
    postgres_version = fields.String(required=True)
    language = fields.String(required=True)
    debug = fields.Boolean(required=True)
    events = fields.Integer(required=True)
    contributions = fields.Integer(required=True)
    users = fields.Integer(required=True)
    attachments = fields.Integer(required=True)
