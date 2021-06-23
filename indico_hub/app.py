import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from celery.app.base import Celery
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException, UnprocessableEntity

from . import __version__
from .config import CELERY_BROKER_URL
from .db import db, register_db_cli


try:
    from flask_cors import CORS
except ImportError:
    CORS = None
# adding this temporary

celery = Celery(__name__, broker=CELERY_BROKER_URL)


def create_app():
    from .server import api

    app = Flask(__name__)
    if os.environ.get('FLASK_ENABLE_CORS') and CORS is not None:
        CORS(app)

    app.config.from_pyfile('config.py')
    # TODO: Before going in prod we should load a config file here w/ the DB uri
    register_error_handlers(app)
    db.init_app(app)
    register_db_cli(app)
    app.register_blueprint(api)
    celery.conf.update(app.config)
    return app


def register_spec(test=False, test_host='localhost', test_port=12345):
    servers = (
        [{'url': f'http://{test_host}:{test_port}', 'description': 'Test server'}]
        if test
        else []
    )

    # Create an APISpec
    spec = APISpec(
        title='Indico Community Hub',
        version=__version__,
        openapi_version='3.0.3',
        info={
            'contact': {
                'name': 'Indico Team',
                'url': 'https://github.com/indico/indico-hub',
                'email': 'indico-team@cern.ch',
            }
        },
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
        servers=servers,
        tags=[{'name': 'instance', 'description': 'Instance operations'}],
    )
    spec.components.security_scheme(
        'bearer_token', {'type': 'http', 'scheme': 'bearer'}
    )
    return spec


def register_error_handlers(app):
    @app.errorhandler(UnprocessableEntity)
    def handle_unprocessableentity(exc):
        data = getattr(exc, 'data', None)
        if data and 'messages' in data:
            # this error came from a webargs parsing failure
            response = jsonify(webargs_errors=data['messages'])
            response.status_code = exc.code
            return response
        if exc.response:
            return exc
        return 'Unprocessable Entity'

    @app.errorhandler(HTTPException)
    def _handle_http_exception(exc):
        return jsonify(error=exc.description), exc.code

    @app.errorhandler(Exception)
    def _handle_exception(exc):
        app.logger.exception('Request failed')
        return jsonify(error='Internal error'), 500
