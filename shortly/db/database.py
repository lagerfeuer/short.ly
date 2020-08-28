import click
from flask_sqlalchemy import SQLAlchemy

db = None


def setup_db(app):
    global db
    db = SQLAlchemy(app)


@click.command('init-db')
def init_db():
    # import all models, needed by create_all
    import shortly.db.models
    db.create_all()
    click.echo("DB initialized")
