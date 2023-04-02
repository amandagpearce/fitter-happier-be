from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
import uuid
from flask_smorest import abort

from db import items, stores

info = Info(title="fitter-happier API", version="1.0.0")
app = OpenAPI(__name__, info=info)
# app = Flask(__name__)
CORS(app)

store_tag = Tag(
    name="Store", description="Adição, visualização e remoção de stores"
)

doc_tag = Tag(
    name="Documentação", description="Visualização da documentação da API"
)


# swagger doc route
@app.get("/doc", tags=[doc_tag])
def getDocs():
    """Redireciona p /openapi."""
    return redirect("/openapi/swagger")


#
# STORES ROUTES
#

# get all stores
@app.get("/stores", tags=[store_tag])
def get_stores():
    """Faz a busca por todas as Stores cadastradas

    Retorna listagem de Stores.
    """
    if stores.values():
        return {"stores": list(stores.values())}
    else:
        abort(404, message="No stores found")


# get store by id
@app.route("/store/<string:store_id>", methods=["GET"])
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found")


# add new store
@app.post("/store", tags=[store_tag])
def create_store():
    """Adiciona nova store"""

    store_data = request.get_json()

    if "name" not in store_data:
        abort(
            400, message="Bad request. Campo 'name' precisa existir no payload"
        )

    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message="Store já existe")

    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store

    return new_store, 201


@app.route("/store/<string:store_id>", methods=["DELETE"])
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted"}
    except KeyError:
        abort(404, message="Store not found")


#
# ITEMS ROUTES
#

# get all items
@app.get("/items", tags=[store_tag])
def get_items():
    """Faz a busca por todas os Items cadastrados

    Retorna listagem de Items.
    """
    if items.values():
        return {"items": list(items.values())}
    else:
        abort(404, message="No items found")


# add new item
@app.post("/item", tags=[store_tag])
def create_item():
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


# get item by id
# dynamic endpoint path issue
# @app.get("/item/<string:item_id>") # doesn't work
@app.route("/item/<string:item_id>", methods=["GET"])
def get_item(item_id):
    try:
        return items[item_id], 200
    except KeyError:
        abort(404, message="Item not found")


@app.route("/item/<string:item_id>", methods=["DELETE"])
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}
    except KeyError:
        abort(404, message="Item not found")


@app.route("/item/<string:item_id>", methods=["PUT"])
def update_item(item_id):
    item_data = request.get_json()

    if "price" not in item_data or "name" not in item_data:
        abort(
            400,
            message="Bad request. 'price' e 'name' são necessário no payload",
        )

    try:
        item = items[item_id]
        item |= item_data  # |= in place modification to change the dictionary

        return item

    except KeyError:
        abort(404, message="Item não encontrado")
