from flask_smorest import abort, Blueprint
from flask.views import MethodView

# from flask_jwt_extended import jwt_required

from db import db
from sqlalchemy.exc import SQLAlchemyError
from schemas import ExerciseSchema, ExerciseUpdateSchema, ExerciseLogSchema
from models import ExercisesModel, ExerciseLogs

blp = Blueprint("Exercícios", __name__, description="Operações em exercícios")


@blp.route("/exercise/<int:exercise_id>")
class exercise(MethodView):
    @blp.response(200, ExerciseSchema)
    def get(self, exercise_id):
        exercise = ExercisesModel.query.get_or_404(exercise_id)
        return exercise

    def delete(self, exercise_id):
        exercise = ExercisesModel.query.get_or_404(exercise_id)
        db.session.delete(exercise)
        db.session.commit()
        return {"message": "exercício deletado"}

    @blp.arguments(ExerciseUpdateSchema)
    @blp.response(200, ExerciseUpdateSchema)
    def put(self, exercise_data, exercise_id):
        exercise = ExercisesModel.query.get(exercise_id)

        if exercise:
            exercise.name = exercise_data["name"]
        else:
            abort(500, message="exercise_id não existe")

        db.session.add(exercise)
        db.session.commit()

        return exercise


@blp.route("/exercise")
class exerciseList(MethodView):
    @blp.response(200, ExerciseSchema(many=True))
    def get(self):
        return ExercisesModel.query.all()

    @blp.arguments(ExerciseSchema)
    @blp.response(201, ExerciseSchema)
    def post(self, exercise_data):
        exercise = ExercisesModel(**exercise_data)

        try:
            db.session.add(exercise)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Erro ao inserir exercise no banco")

        return exercise


@blp.route("/exercise/log/<int:exercise_id>")
class exerciseLog(MethodView):
    @blp.arguments(ExerciseLogSchema)
    @blp.response(201, ExerciseLogSchema)
    def post(self, log_data, exercise_id):
        exercise = ExercisesModel.query.get_or_404(exercise_id)
        if exercise:
            log = ExerciseLogs(exercise_id=exercise_id, **log_data)
        else:
            abort(500, message="Exercicio não existe")

        try:
            db.session.add(log)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Erro ao inserir log no banco")

        return {log}, 201
