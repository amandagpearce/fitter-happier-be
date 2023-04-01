from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request

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


@app.get("/doc", tags=[doc_tag])
def getDocs():
    """Redireciona p /openapi."""
    return redirect("/openapi/swagger")


@app.get("/store", tags=[store_tag])
def get_stores():
    """Faz a busca por todas as Stores cadastradass

    Retorna listagem de Stores.
    """
    return {"stores": stores}


@app.post("/store", tags=[store_tag])
def add_store():
    """Adiciona nova store"""

    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


# dynamic endpoint path
# @app.post("/store/<string:name>/item")
@app.route("/store/<string:name>/item", methods=["POST"], tags=[store_tag])
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {
                "name": request_data["name"],
                "price": request_data["price"],
            }
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 404


@app.route("/store/<string:name>", methods=["GET"])
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store, 200
    return {"message": "Store not found"}, 404


@app.route("/store/<string:name>/item", methods=["GET"])
def get_store_items(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}, 200
    return {"message": "Store not found"}, 404
