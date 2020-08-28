from flask import current_app
from shortly.db.database import db

import hashlib
from base64 import urlsafe_b64encode
from datetime import datetime, timezone


def _hash(url, length=6):
    hsh = hashlib.sha1(bytes(url, encoding='utf-8')).digest()
    return str(urlsafe_b64encode(hsh), 'utf-8')[:length]


class URL(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(1024), nullable=False)
    short = db.Column(db.String(64), nullable=False, unique=True)
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, url):
        self.url = url

        tmp = _hash(url)
        while URL.query.filter(URL.short == tmp).first() is not None:
            tmp = _hash(tmp)
        self.short = tmp

        self.created = datetime.now(timezone.utc)
