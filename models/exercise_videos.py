from db import db


class ExerciseVideos(db.Model):
    __tablename__ = "exercise_videos"

    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"))
    video_id = db.Column(db.Integer, db.ForeignKey("videos.id"))


# mapping of many to many relationship
# one exercise can have many videos, one video can belong to many exercises
