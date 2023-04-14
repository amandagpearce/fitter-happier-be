from db import db


class ExerciseLogs(db.Model):
    __tablename__ = "exercise_logs"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"))
