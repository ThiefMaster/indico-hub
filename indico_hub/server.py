from copy import Error
import click
from flask import Blueprint, current_app, json, request, abort, jsonify
from flask_swagger import swagger
from flask.wrappers import Response
from marshmallow import fields, validate, ValidationError
import requests

from .app import register_spec
from .register import register


from webargs.flaskparser import use_args, parser

from .db import db
from .models import Instance
from .schemas import *


api = Blueprint('api', __name__, cli_group=None)


@api.cli.command('openapi')
@click.option(
    '--json',
    'as_json',
    is_flag=True,
)
@click.option(
    '--test',
    '-t',
    is_flag=True,
    help='Specify a test server (useful for Swagger UI)',
)
@click.option('--host', '-h')
@click.option('--port', '-p')
def _openapi(test, as_json, host, port):
    """Generate OpenAPI metadata from Flask app."""
    with current_app.test_request_context():
        spec = register_spec(test=test, test_host=host, test_port=port)
        # TODO: Register all the exposed view functions here.
        #       Don't worry about this at the beginning though!
        # spec.path(view=...)

        if as_json:
            print(json.dumps(spec.to_dict()))
        else:
            print(spec.to_yaml())



# TODO: Implement the API endpoints here

"""
Here I will be recieving info from user who is registering their instance
The info will be in the form of 
payload = {
        'url': BASE_URL,
        'contact': contact,
        'email': email,
        'organization': "it"
    }
"""
'''
@api.route("/instance", methods=["POST"])
def instance():
    resp = register("Hank", "g@gmail.com")
    print(resp)
    return resp, 200

'''
req_args = {
    'contact': fields.String(required=True),
    'email': fields.String(required=True),
    'organization': fields.String(required=True)
}


@api.route("/api/instance", methods= ["POST"])
def register():
    #allows for repetition so far
    """
    mock function for registering an instance to the database
    ---
    parameters: 
        None
    

    responses:
          201:
            description: instance registered 
          404:
            description: instance is already registered
    """
    
    print("validating params...")
    
    errors = validationSchema().validate(request.form)
    if errors:
        current_app.logger.exception("register: missing an argument")
        abort(400)
    
    contact = request.form.get("contact")
    email = request.form.get("email")
    org = request.form.get("organization")
    print("creating instance...")
    inst = Instance.query.filter_by(contact= contact).first()
    if (inst):
        current_app.logger.exception("register: This instance is already registered")
        abort(401)

    inst = Instance(contact= contact,
                    email = email,
                    organization = org) 
  
    print("storing instance ...")                    
    db.session.add(inst)
    db.session.commit()
    toJson = instanceSchema()
    myJson = toJson.dump(inst)
    return myJson, 201


@api.route("/all")
def all():
    all = Instance.query.all()
    schema = instanceSchema(many=True)
    return jsonify(schema.dump(all)), 200

