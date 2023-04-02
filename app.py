from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
import uuid

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


# get all stores route
@app.get("/stores", tags=[store_tag])
def get_stores():
    """Faz a busca por todas as Stores cadastradas

    Retorna listagem de Stores.
    """
    if stores.values():
        return {"stores": list(stores.values())}
    else:
        return {"message": "no stores found"}, 404


# get all items route
@app.get("/items", tags=[store_tag])
def get_items():
    """Faz a busca por todas os Items cadastrados

    Retorna listagem de Items.
    """
    if items.values():
        return {"items": list(items.values())}
    else:
        return {"message": "no items found"}, 404


# add new store route
@app.post("/store", tags=[store_tag])
def create_store():
    """Adiciona nova store"""

    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store

    return new_store, 201


# add new item route
@app.post("/item", tags=[store_tag])
def create_item():
    item_data = request.get_json()

    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404

    item_id = uuid.uuid4().hex
    new_item = {**item_data, "id": item_id}
    items[item_id] = new_item

    return new_item, 201


# get item by store id
# dynamic endpoint path issue
# @app.get("/item/<string:item_id>") # doesn't work
@app.route("/item/<string:item_id>", methods=["GET"])
def get_item(item_id):
    try:
        return items[item_id], 200
    except KeyError:
        return {"message": "Item not found"}, 404


# get store by id route
@app.route("/store/<string:store_id>", methods=["GET"])
def get_store(store_id):
    try:
        return stores
    except KeyError:
        return {"message": "Store not found"}, 404
