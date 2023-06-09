from flask_smorest import abort, Blueprint
from flask.views import MethodView

# from flask_jwt_extended import jwt_required

from db import db
from sqlalchemy.exc import SQLAlchemyError
from schemas import (
    ExerciseSchema,
    PlainExerciseSchema,
    ExerciseUpdateSchema,
    ExerciseLogSchema,
)
from models import ExercisesModel, ExerciseLogs

blp = Blueprint("Exercícios", __name__, description="Operações em exercícios")


@blp.route("/exercise/<int:exercise_id>")
class exercise(MethodView):
    @blp.response(200, ExerciseSchema)
    def get(self, exercise_id):
        """Encontra e retorna o exercício baseado no ID"""
        exercise = ExercisesModel.query.get_or_404(exercise_id)
        return exercise

    def delete(self, exercise_id):
        """Exclui o exercício baseado no ID"""
        exercise = ExercisesModel.query.get_or_404(exercise_id)
        db.session.delete(exercise)
        db.session.commit()
        return {"message": "exercício deletado"}

    @blp.arguments(ExerciseUpdateSchema)
    @blp.response(200, ExerciseUpdateSchema)
    def put(self, exercise_data, exercise_id):
        """Muda o título dado ao exercício baseado no ID"""
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
        """Retorna todos os exercícios já cadastrados"""
        return ExercisesModel.query.all()

    @blp.arguments(PlainExerciseSchema)
    @blp.response(201, PlainExerciseSchema)
    def post(self, exercise_data):
        """Cria um novo exercício"""
        exercise = ExercisesModel(**exercise_data)

        try:
            db.session.add(exercise)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Erro ao inserir exercício no banco")

        return exercise


@blp.route("/exercise/log/<int:exercise_id>")
class exerciseLog(MethodView):
    @blp.arguments(ExerciseLogSchema)
    @blp.response(201, ExerciseLogSchema)
    def post(self, log_data, exercise_id):
        """Cria um novo log do exercício baseado na data e ID do exercício"""
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
