from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship(
        "ItemModel",
        back_populates="store",
        lazy="dynamic",  # the items here wont be fecthed unless we tell it to
        cascade="all, delete",
    )


# will go intto items table and retrieve items where the store_id matches
# the id here
