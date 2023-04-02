import uuid
from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from db import items, stores

blp = Blueprint("Items", __name__, description="Operações em items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id], 200
        except KeyError:
            abort(404, message="Item not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message="Item not found")

    def put(self, item_id):
        item_data = request.get_json()

        if "price" not in item_data or "name" not in item_data:
            abort(
                400,
                message="Bad request. 'price' e 'name' devem estar no payload",
            )

        try:
            item = items[item_id]
            item |= (
                item_data  # |= in place modification to change the dictionary
            )

            return item

        except KeyError:
            abort(404, message="Item não encontrado")


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        if items.values():
            return {"items": list(items.values())}
        else:
            abort(404, message="No items found")

    def post(self):
        item_data = request.get_json()

        # checando se todos os campos estão presentes no payload
        if (
            "price" not in item_data
            or "store_id" not in item_data
            or "name" not in item_data
        ):
            abort(
                400,
                message="""Bad request. Inclua 'price', 'store_id' e 'name' no
                payload""",
            )

        # checando se o item já não existe p/ prevenir items duplicados
        for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message="Item já existe")

        # checando se a store existe
        if item_data["store_id"] not in stores:
            abort(404, message="Store not found")

        item_id = uuid.uuid4().hex
        new_item = {**item_data, "id": item_id}
        items[item_id] = new_item

        return new_item, 201
