from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    store_id = db.Column(
        db.Integer(), db.ForeignKey("stores.id"), nullable=False
    )
    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship(
        "ItemModel", back_populates="tags", secondary="item_tags"
    )


# secondary refers to the secondary table in item_tags

# sqlalchemy will go through the secondary table to find what items the tag
# is related to

# it will see what items have the tag id and pull these items to populate
# "items"
