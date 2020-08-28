from flask import Flask, redirect, render_template, url_for, abort

import os
import sys

from shortly.db.database import init_db, setup_db
from shortly.utils import get_env, get_db_uri

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration


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
    app.config.from_mapping(
        SECRET_KEY='secret key' if os.getenv('FLASK_ENV') == 'development' else os.urandom(16),
        SERVER_NAME='shortly.localhost:5000',
        SQLALCHEMY_DATABASE_URI=get_db_uri(),
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
    )

    if test_config is not None:
        app.config.from_mapping(test_config)

    setup_db(app)
    from shortly.db.models import URL
    from shortly.api.URL_API import URL_API

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
