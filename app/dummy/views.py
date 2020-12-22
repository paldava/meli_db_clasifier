from flask import Blueprint
from flask_restplus import Api, Resource

dummy = Blueprint("dummy", __name__)

api = Api(dummy, title="Dummy API object", description="For python-init demostration purposes")


@api.route("/")
class DummyResource(Resource):
    def get(self):
        return "Hello world"
