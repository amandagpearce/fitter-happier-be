from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    user_id = db.Column(
        db.String, db.ForeignKey("users.id"), unique=False, nullable=False
    )
    exercises = db.relationship(
        "ExercisesModel", back_populates="tags", secondary="exercise_tags"
    )
