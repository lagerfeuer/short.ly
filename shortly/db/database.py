import click
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from shortly.utils import get_db_uri

database_uri = get_db_uri()
engine = create_engine(database_uri, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


@click.command('init-db')
def init_db():
    # import all models, needed by create_all
    import shortly.db.models
    Base.metadata.create_all(bind=engine)
    click.echo("DB initialized: %s" % database_uri)
