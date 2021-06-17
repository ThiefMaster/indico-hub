from copy import Error
import click
from flask import Blueprint, current_app, json, request, abort, jsonify
from flask_swagger import swagger
from flask.wrappers import Response
from marshmallow import fields, validate, ValidationError
import requests

from .app import register_spec


from webargs.flaskparser import use_kwargs

from .db import db
from .models import Instance
from .schemas import InstanceSchema, ValidationSchema, UpdateInstance

#
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
        spec.path(view=register)
        spec.path(view=update_instance)
        spec.path(view=get_instance)
        

        if as_json:
            print(json.dumps(spec.to_dict()))
        else:
            print(spec.to_yaml())



# TODO: Implement the API endpoints here
'''
'''

@api.route("/api/instance", methods= ["POST"])
@use_kwargs(ValidationSchema, location='json')
def register(
    uuid,
    enabled,
    url,
    contact,
    email,
    organization,
    crawl_date,
    registration_date):
    """
    mock function for registering an instance to the database
    ---
    parameters: 
        Instance.get_json()
    
    

    responses:
          201:
            description: instance registered 
          404:
            description: instance is already registered
    """
    
    print("validating params...")
    
    """ errors = ValidationSchema().validate(request.form)
    if errors:
        current_app.logger.exception("register: missing an argument: \n\t"+ str(errors))
        abort(400, description="BAD_REQUEST")"""
    inst = Instance().query.filter_by(uuid= uuid).first()
    if (inst):
        current_app.logger.exception("register: This instance is already registered")
        abort(401, description="BAD_REQUEST")
        
    print("creating instance...")
    inst = Instance(uuid=uuid, enabled=enabled, url=url, contact=contact, email=email, organization=organization, crawl_date=crawl_date,registration_date=registration_date)
    print("storing instance ...")                    
    db.session.add(inst)
    db.session.commit()
    return InstanceSchema().dumps(inst), 201


'''
6/16
In here I will complete translating updating api code into a 
fresher code. Here I will implement the /instance/<uuid>
'''
@api.route("/api/instance/<string:uuid>",  methods=["PATCH", "POST"])
@use_kwargs(UpdateInstance, location='json')
def update_instance(uuid, **kwargs):
    """
    updates information regarding the instance
    ---
    parameters:
        -enabled
        -url
        -contact
        -email
        -organization
    responses:
        200: updated instance
        400: missing argument | bad_url | Instance doesn't exist
    """
    #validate params
        #make a schema to validate the existance of ['enabled', 'url', 'contact', 'email', 'organization']
    
    #find existing instance
    print("find existing instance")
    if uuid is None:
        abort(400, description="BAD_URL")
    
    inst = Instance().query.filter_by(uuid = uuid).first()
    if inst is None:
        abort(404, description="BAD REQUEST")
    
    #update instance with new info
    print("update instance with new info")
    for attr in kwargs:
        setattr(inst, attr, kwargs[attr])
    db.session.commit()
    return jsonify(InstanceSchema().dump(inst))
    


@api.route("/api/instance/<string:uuid>", methods=["GET"])
def get_instance(uuid):
    instance = Instance().query.filter_by(uuid=uuid).first()
    if instance is None:
        abort(404, description="instance not found")
    
    rv = jsonify(InstanceSchema().dump(instance))
    rv.headers['Access-Control-Allow-Origin'] = '*'
    return rv


@api.route("/all")
def all():
    all = Instance().query.all()
    schema = InstanceSchema(many=True)
    return jsonify(schema.dump(all)), 200



