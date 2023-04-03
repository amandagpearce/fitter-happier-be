import os
from flask_cors import CORS
from flask import Flask
from flask_smorest import Api

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

from db import db
import models  # noqa


def create_app(db_url=None):  # factory pattern
    app = Flask(__name__)
    CORS(app)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/doc"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL",
        "sqlite:///data.db",  # if database_url is not found, default to sqlite
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)  # initializes sqlalchemy

    api = Api(app)

    with app.app_context():
        db.create_all()  # creating the dbs if they dont already exist

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app
