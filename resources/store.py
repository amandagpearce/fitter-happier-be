import uuid
from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from db import stores

blp = Blueprint("Store", __name__, description="Operações em stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted"}
        except KeyError:
            abort(404, message="Store not found")


@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        if stores.values():
            return {"stores": list(stores.values())}
        else:
            abort(404, message="No stores found")

    def post(self):
        store_data = request.get_json()

        if "name" not in store_data:
            abort(
                400,
                message="Bad request. Campo 'name' precisa existir no payload",
            )

        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="Store já existe")

        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store

        return new_store, 201
