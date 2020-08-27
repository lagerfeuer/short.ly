from flask import request
from flask.views import MethodView

from shortly.db.database import db_session
from shortly.db.models import URL
from shortly.utils import fail, success


class URL_API(MethodView):
    def get(self):
        """
        Check whether the URL has been shortened and return the short link.
        :return: shortened URL or error
        """
        json = request.get_json()
        if json is None:
            return fail("No payload"), 400
        url = json.get('url')
        if url is None:
            return fail("Field 'url' missing."), 400
        if entry := URL.query.filter(URL.url == url).first():
            return success(entry)
        return fail("Could not find shortened URL"), 404

    def post(self):
        """
        Shorten an URL and return the shortened link.
        :return: shortened URL or error
        """
        json = request.get_json()
        if json is None:
            return fail("No payload"), 400
        url = json.get('url')
        if url is None:
            return fail("Field 'url' missing."), 400

        entry = URL(url)
        db_session.add(entry)
        db_session.commit()

        return success(entry)

    def delete(self):
        pass
