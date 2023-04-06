from flask_smorest import abort, Blueprint
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256

from db import db
from schemas import UserSchema
from models import UserModel

blp = Blueprint("Users", "users", description="Operações em Usuários")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first():
            abort(409, message="Esse username já existe.")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "Usuario criado com sucesso"}, 201


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(
        self, user_id
    ):  # wont be publicly available in the api, just for testing
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "Usuario deletado"}, 200
