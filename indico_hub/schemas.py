# from marshmallow import Schema
# from webargs import fields


# TODO: Implement Marshmallow schemas for the API request data

from flask_marshmallow import *
from marshmallow import *
from marshmallow_sqlalchemy import *
from .models import *
"""
payload = {
        'url': BASE_URL,
        'contact': contact,
        'email': email,
        'organization': "it"
    }
"""
class instance(SQLAlchemyAutoSchema):
    class Meta:
        model = Instance
        include_relationships = True
        include_fk = True
        load_instance = True
