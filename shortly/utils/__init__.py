import os
from .Errors import *
from flask import current_app


def get_env(name):
    if var := os.getenv(name):
        return var
    else:
        raise SettingNotFound("'%s' missing in environment" % name)


def get_db_uri():
    database_uri = 'sqlite:////tmp/shortly.db.sqlite'

    db_backend = os.getenv('SHORTLY_DB_BACKEND')
    # use default sqlite if SHORTLY_DB_BACKEND is not defined
    if os.getenv('FLASK_ENV') == 'development' and db_backend is None:
        return database_uri
    db_backend = db_backend.lower()

    if db_backend == 'mysql':
        database_uri = 'mysql://{user}:{password}@{host}/{database}'.format(
            user=os.getenv('SHORTLY_DB_USER'),
            password=os.getenv('SHORTLY_DB_PASSWORD'),
            host=os.getenv('SHORTLY_DB_HOST'),
            database=os.getenv('SHORTLY_DB_NAME'),
        )
    elif db_backend == 'sqlite':
        database_uri = 'sqlite:///{path}'.format(path=os.getenv('SHORTLY_DB_PATH'))

    return database_uri


def fail(msg, fields=None):
    response = fields or {}
    response['message'] = msg
    response['status'] = 'error'
    return response


def success(entry, fields=None):
    response = fields or {}
    response['url'] = 'http://{url}/{base64}'.format(url=current_app.config['SERVER_NAME'],
                                              base64=entry.short)
    response['status'] = 'success'
    return response
