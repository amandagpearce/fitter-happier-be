from db import db


class VideoModel(db.Model):
    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    yt_id = db.Column(db.String(80), unique=True, nullable=False)
    exercises = db.relationship(
        "ExercisesModel",
        back_populates="videos",
        secondary="exercise_videos",
    )


# will go intto items table and retrieve items where the store_id matches
# the id here
