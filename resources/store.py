import uuid
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from db import stores
from schemas import StoreSchema

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

    @blp.arguments(StoreSchema)
    def post(self, store_data):

        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="Store já existe")

        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store

        return new_store, 201
