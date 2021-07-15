import click
from flask import Blueprint, abort, current_app, json, jsonify
from webargs.flaskparser import use_kwargs

from .app import register_spec
from .crawler import geolocate
from .db import db
from .es_conf import es
from .models import Instance
from .schemas import InstanceSchema, Statistics, UpdateInstance, ValidationSchema


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
@api.route('/api/instance/', methods=['POST'])
@use_kwargs(ValidationSchema, location='json')
def register(url, contact, email, organization):
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
    inst = Instance(
        url=url,
        contact=contact,
        email=email,
        organization=organization,
    )
    db.session.add(inst)
    db.session.commit()
    uuid = InstanceSchema().dump(inst)['uuid']
    return jsonify({'uuid': uuid}), 201


@api.route('/api/instance/<string:uuid>', methods=['PATCH', 'POST'])
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
        201: unregistered instance
        400: missing argument | bad_url | Instance doesn't exist
    """
    inst = Instance.query.filter_by(uuid=uuid).first()
    if inst is None:
        abort(404, description='BAD REQUEST: user already exist')

    for attr in kwargs:
        setattr(inst, attr, kwargs[attr])
    db.session.commit()
    uuid = InstanceSchema().dump(inst)['uuid']
    return jsonify({'uuid': uuid}), 200


@api.route('/api/instance/<string:uuid>', methods=['GET'])
def get_instance(uuid):
    """
    Gets info about the instance
    ---
    arguments:
        uuid
    responses:
        200: found instance and returned info
        404: instance not found
    """
    instance = Instance.query.filter_by(uuid=uuid).first()
    if instance is None:
        abort(404, description='instance not found')
    rv = jsonify(InstanceSchema().dump(instance))
    rv.headers['Access-Control-Allow-Origin'] = '*'
    return rv


@api.route('/api/instance/<string:uuid>/submit', methods=['POST', 'PATCH'])
@use_kwargs(Statistics, location='json')
def get_stats(
    python_version,
    indico_version,
    operating_system,
    postgres_version,
    language,
    debug,
    uuid,
    **kwargs,
):
    """
    Collects statistics from (registered & active) instances
    ---
    arguments:
        uuid
    parameters:
        python_version:
        indico_version:
        operating_system:
        postgres_version:
        language:
        kwargs:
            debug:
            events:
            contributions:
            users:
            attachments:
    responses:
        200: found instance and returned info
        404: instance not found
    """
    # fetch machine data
    inst = Instance.query.filter_by(uuid=uuid).first()
    if inst is None:
        abort(404, description='BAD REQUEST: instance isnt registered.')
    # get inst info
    inst_data = ValidationSchema().dump(inst)
    # will send these data to elasticsearch
    machine_data = {
        'python_version': python_version,
        'indico_version': indico_version,
        'operating_system': operating_system,
        'postgres_version': postgres_version,
        'language': language,
        'debug': debug,
        'ip': '',
    }
    # adding optional info and url
    for field in kwargs:
        if field == 'timestamp':
            machine_data['@timestamp'] = kwargs[field]
        else:
            machine_data[field] = kwargs[field]
    machine_data['url'] = inst_data['url']
    result = es.index(index='reg_data', id=uuid, body=machine_data)
    result = geolocate(inst)
    return jsonify(result)


@api.route('/api/instance/<string:uuid>/get', methods=['GET'])
def get_user(uuid):
    results = es.get(index='reg_data', id=uuid)
    return jsonify(results['_source'])


@api.route('/api/instance/getAll/es')
def get_all_es():
    res = es.search(
        index='reg_data',
        filter_path=['hits.hits._*'],
        body={'query': {'match_all': {}}},
    )['hits']['hits']
    return jsonify(res)


@api.route('/all')
def all():
    all = Instance.query.all()
    schema = InstanceSchema(many=True)
    return jsonify(schema.dump(all)), 200


@api.route('/deleteAll')
def delete():
    num_rows = db.session.query(Instance).delete()
    db.session.commit()
    es.indices.delete(index='reg_data', ignore=[400, 404])
    return f'{num_rows}'
