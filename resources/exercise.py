from flask_smorest import abort, Blueprint
from flask.views import MethodView

# from flask_jwt_extended import jwt_required

from db import db
from sqlalchemy.exc import SQLAlchemyError
from schemas import ExerciseSchema
from models import ExercisesModel

blp = Blueprint("Exercícios", __name__, description="Operações em exercícios")


@blp.route("/exercise/<int:exercise_id>")
class exercise(MethodView):
    # @jwt_required()
    @blp.response(200, ExerciseSchema)
    def get(self, exercise_id):
        exercise = ExercisesModel.query.get_or_404(
            exercise_id
        )  # query method comes from db.model class from flask-sqlalchemy
        return exercise

    # @jwt_required()
    def delete(self, exercise_id):
        exercise = ExercisesModel.query.get_or_404(exercise_id)
        db.session.delete(exercise)
        db.session.commit()
        return {"message": "exercise deletado"}

    # # @jwt_required()
    # @blp.arguments(exerciseUpdateSchema)
    # @blp.response(200, ExerciseSchema)
    # def put(
    #     self, exercise_data, exercise_id
    # ):  # the exercise_data from the validation needs to come before the root args
    #     exercise = ExercisesModel.query.get(exercise_id)

    #     if exercise:  # if exists, changes price and name
    #         exercise.price = exercise_data["price"]
    #         exercise.name = exercise_data["name"]
    #     else:  # if doesnt exist, store id will be needed
    #         exercise = ExercisesModel(
    #             id=exercise_id, **exercise_data
    #         )  # passing exercise_id from the url

    #     db.session.add(exercise)
    #     db.session.commit()

    #     return exercise


@blp.route("/exercise")
class exerciseList(MethodView):
    # @jwt_required()
    @blp.response(200, ExerciseSchema(many=True))
    def get(self):
        return ExercisesModel.query.all()

    # @jwt_required(fresh=True)
    @blp.arguments(ExerciseSchema)
    @blp.response(201, ExerciseSchema)
    def post(self, exercise_data):
        exercise = ExercisesModel(**exercise_data)
        # **exercise_data turns the dictionary received into keyword args

        try:
            db.session.add(exercise)
            db.session.commit()  # actually saving
            # can run commit once for multiple adds
        except SQLAlchemyError:
            abort(500, message="Erro ao inserir exercise no banco")

        return exercise
