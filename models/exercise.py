from db import db


class ExercisesModel(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(1), nullable=False)
    description = db.Column(db.String(80))
    user_id = db.Column(
        db.String, db.ForeignKey("users.id"), unique=False, nullable=False
    )
    tags = db.relationship(
        "TagModel", back_populates="exercises", secondary="exercise_tags"
    )
    videos = db.relationship(
        "VideoModel", back_populates="exercises", secondary="exercise_videos"
    )


# when we have a store_id using the stores table we can define a relationship
# with the storemodel class
# MEANING we can access later MyItem.store and have the store content

# back_populates="items" - the store model will also receive items field

# back_populates="items" on tags field, relating items to tags
