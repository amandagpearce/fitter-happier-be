from flask_smorest import abort, Blueprint
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt,
    create_refresh_token,
    get_jwt_identity,
)

from db import db
from schemas import UserSchema
from models import UserModel, TokenBlocklistModel

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


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

        abort(401, message="Invalid credentials.")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]  # or get_jwt().get("jti")

        token = TokenBlocklistModel(token=jti)
        db.session.add(token)
        db.session.commit()

        return {"message": "Logout executado."}, 200


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}
