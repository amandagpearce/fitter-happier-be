from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False
    )
    # will populate stores with the StoreModel object whose id matches the FK
    store = db.relationship("StoreModel", back_populates="items")
    # the Stores table is used by the StoreModel class


# when we have a store_id using the stores table we can define a relationship
# with the storemodel class
# MEANING we can access later MyItem.store and have the store content

# back_populates="items" - the store model will also receive items field
