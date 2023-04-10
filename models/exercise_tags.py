from db import db


class ExerciseTags(db.Model):
    __tablename__ = "exercise_tags"

    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))


# mapping of many to many relationship
# one item can have many tags, one tag can belong to many items
