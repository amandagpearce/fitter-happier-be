from flask_smorest import abort, Blueprint
from flask.views import MethodView

from db import db

from schemas import StoreSchema
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("Store", __name__, description="Operações em stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store foi deletada"}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(
        200, StoreSchema(many=True)
    )  # many=True turns the response into a list
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:  # violates the constraint of unique name
            abort(400, message="Já existe uma store com esse nome")
        except SQLAlchemyError:
            abort(500, message="Ocorreu um erro ao salvar a store.")

        return store
