from flask import request
from flask.views import MethodView

from shortly.api.URLSchema import UrlSchema
from shortly.db.database import db
from shortly.db.models import URL
from shortly.utils import fail, success

from marshmallow import ValidationError


class UrlApi(MethodView):
    def get(self):
        """
        Check whether the URL has been shortened and return the short link.
        :return: shortened URL or error
        """
        try:
            json = UrlSchema().load(request.get_json())
        except ValidationError as err:
            return fail(err.messages), 400

        url = json['url']
        if entry := URL.query.filter(URL.url == url).first():
            return success(entry)
        return fail("Could not find shortened URL"), 404

    def post(self):
        """
        Shorten an URL and return the shortened link.
        :return: shortened URL or error
        """
        try:
            json = UrlSchema().load(request.get_json())
        except ValidationError as err:
            return fail(err.messages), 400

        url = json['url']
        entry = URL(url)
        db.session.add(entry)
        db.session.commit()

        return success(entry), 201

    def delete(self):
        pass
