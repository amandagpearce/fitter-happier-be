from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

from db import db
from schemas import VideoAndExerciseSchema, VideoSchema
from models import VideoModel, ExercisesModel


blp = Blueprint("Video", __name__, description="Operações em videos")


@blp.route("/video/<int:video_id>")
class VideoDeletion(MethodView):
    def delete(self, video_id):
        """Exclui o video baseado no ID"""
        video = VideoModel.query.get_or_404(video_id)
        db.session.delete(video)
        db.session.commit()
        return {"message": "Video foi excluído"}


@blp.route("/video")
class StoreList(MethodView):
    @blp.arguments(VideoSchema)
    @blp.response(200, VideoSchema)
    def post(self, video_data):
        """Cria um novo vídeo ou retorna o id no banco se o yt_id já existe."""
        print(video_data)
        video = VideoModel.query.filter(
            VideoModel.yt_id == video_data["yt_id"]
        ).first()
        if video is None:
            video = VideoModel(**video_data)
        else:
            return video
        try:
            db.session.add(video)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Ocorreu um erro ao salvar o video.")

        return video


@blp.route("/exercise/<exercise_id>/video/<video_id>")
class LinkVideosToExercise(MethodView):
    @blp.response(201, VideoAndExerciseSchema)
    def post(self, exercise_id, video_id):
        """Atribui um video já criado ao exercício já criado"""
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
    def delete(self, exercise_id, video_id):
        """Remove o video do exercício"""
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
