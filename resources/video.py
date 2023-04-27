from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from schemas import VideoAndExerciseSchema, VideoSchema, ExerciseSchema
from models import VideoModel, ExercisesModel


blp = Blueprint("Video", __name__, description="Operações em videos")


@blp.route("/video/<int:exercise_id>")
class GetVideoFromExercise(MethodView):
    @blp.response(200, ExerciseSchema)
    def get(self, exercise_id):
        exercise = ExercisesModel.query.get(
            exercise_id
        )  # query method comes from db.model class from flask-sqlalchemy
        return exercise


@blp.route("/video/<int:video_id>")
class VideoDeletion(MethodView):
    def delete(self, video_id):
        video = VideoModel.query.get_or_404(video_id)
        db.session.delete(video)
        db.session.commit()
        return {"message": "Video foi excluído"}


@blp.route("/video")
class StoreList(MethodView):
    @blp.response(
        200, VideoSchema(many=True)
    )  # many=True turns the response into a list
    def get(self):
        return VideoModel.query.all()

    @blp.arguments(VideoSchema)
    @blp.response(200, VideoSchema)
    def post(self, video_data):
        video = VideoModel(**video_data)
        try:
            db.session.add(video)
            db.session.commit()
        except IntegrityError:  # violates the constraint of unique name
            abort(400, message="Já existe um video com esse nome")
        except SQLAlchemyError:
            abort(500, message="Ocorreu um erro ao salvar o video.")

        return video


@blp.route(
    "/exercise/<exercise_id>/video/<video_id>"
)  # links videos + exercises
class LinkVideosToExercise(MethodView):
    @blp.response(201, VideoAndExerciseSchema)
    def post(self, exercise_id, video_id):
        exercise = ExercisesModel.query.get_or_404(exercise_id)
        video = VideoModel.query.get_or_404(video_id)

        exercise.videos.append(video)

        try:
            db.session.add(exercise)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                500, message="Ocorreu um erro ao inserir o video no exercicio"
            )

        return video

    @blp.response(200, VideoAndExerciseSchema)
    def delete(self, exercise_id, video_id):  # un-links videos + exercises
        exercise = ExercisesModel.query.get_or_404(exercise_id)
        video = VideoModel.query.get_or_404(video_id)
        exercise.videos.remove(video)

        try:
            db.session.add(exercise)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Ocorreu um erro ao remover video do exercicio")

        return {
            "message": "Video removido do exercício",
            "video": video,
            "exercicio": exercise,
        }
