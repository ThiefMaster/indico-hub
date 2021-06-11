import click
from flask import Blueprint, current_app, json

from .app import register_spec


# from webargs.flaskparser import use_kwargs

# from .db import db
# from .models import Instance
# from .schemas import ...


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
