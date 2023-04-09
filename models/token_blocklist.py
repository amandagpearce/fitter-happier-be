from db import db


class TokenBlocklistModel(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String)
