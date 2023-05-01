from db import db


class ExercisesModel(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    type = db.Column(db.String(1), nullable=False, unique=True)
    description = db.Column(db.String(80))
    videos = db.relationship(
        "VideoModel", back_populates="exercises", secondary="exercise_videos"
    )
