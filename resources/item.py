from flask_smorest import abort, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from db import db
from sqlalchemy.exc import SQLAlchemyError
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel

blp = Blueprint("Items", __name__, description="Operações em items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(  # if no id is found, 404's returned
            item_id
        )  # query method comes from db.model class from flask-sqlalchemy
        return item

    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deletado"}

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(
        self, item_data, item_id
    ):  # the item_data from the validation needs to come before the root args
        item = ItemModel.query.get(item_id)

        if item:  # if exists, changes price and name
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:  # if doesnt exist, store id will be needed
            item = ItemModel(
                id=item_id, **item_data
            )  # passing item_id from the url

        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):

        item = ItemModel(**item_data)
        # **item_data turns the dictionary received into keyword args

        try:
            db.session.add(item)  # you can do multiple adds before "commit"
            db.session.commit()  # actually saving
            # can run commit once for multiple adds
        except SQLAlchemyError:
            abort(500, message="Erro ao inserir item no banco")

        return item
