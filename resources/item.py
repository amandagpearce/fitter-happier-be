from flask_smorest import abort, Blueprint
from flask.views import MethodView

from db import db
from sqlalchemy.exc import SQLAlchemyError
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel

blp = Blueprint("Items", __name__, description="Operações em items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
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

    @blp.arguments(
        ItemUpdateSchema
    )  # the item_data from the validation needs to come before the root args
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
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
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(
        self, item_data
    ):  # item_data contains the validated fields from marshmallow

        item = ItemModel(
            **item_data
        )  # **item_data turns the dictionary received into keyword args

        try:
            db.session.add(item)  # you can do multiple adds before "commit"
            db.session.commit()  # actually saving; can run commit once for multiple adds
        except SQLAlchemyError:
            abort(500, message="Erro ao inserir item no banco")

        return item
