from flask import Flask, redirect, render_template, url_for, abort
from flask_sqlalchemy import SQLAlchemy

import os
import sys

from shortly.db.database import init_db
from shortly.db.models import URL
from shortly.api.URL_API import URL_API
from shortly.utils import get_env, get_db_uri

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

DEV_ENV = os.getenv('FLASK_ENV') == 'development'


def _get_env_vars(lst):
    vars = {}
    for var in lst:
        vars[var.split('_')[-1]] = get_env(var)
    return vars


def create_app(test_config=None):
    if dsn := os.getenv('SENTRY_DSN'):
        sentry_sdk.init(dsn=dsn, integrations=[FlaskIntegration(), SqlalchemyIntegration()])

    app = Flask(__name__,
                instance_relative_config=True,
                static_url_path='')
    app.logger.debug("FLASK_ENV: %s" % os.getenv('FLASK_ENV'))

    ###################################################################################################################
    # CONFIG
    ###################################################################################################################
    database_uri = get_db_uri()

    app.config.from_mapping(
        SECRET_KEY='secret key' if DEV_ENV else os.urandom(16),
        SQLALCHEMY_DATABASE_URI=database_uri,
        SERVER_NAME='shortly.localhost:5000',
    )

    if test_config is not None:
        app.config.from_mapping(test_config)

    ###################################################################################################################
    # ROUTES
    ###################################################################################################################
    @app.route('/')
    def hello_world():
        return 'Hello World!'

    @app.route('/<string:short>')
    def resolve_url(short):
        if url := URL.query.filter(URL.short == short).first():
            return redirect(url.url, 303)
        abort(404)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    app.add_url_rule('/api', view_func=URL_API.as_view('url_api'))

    ###################################################################################################################
    # CLI
    ###################################################################################################################
    app.cli.add_command(init_db)

    return app
