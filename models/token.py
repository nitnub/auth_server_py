from db import db


class TokenModel(db.Model):
    __tablename__ = "tokens"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(64), unique=True, nullable=False)
    iat = db.Column(db.Integer, nullable=False)
    exp = db.Column(db.Integer, nullable=False)
    iaDateTime = db.Column(db.DateTime, nullable=False)
    iaTime = db.Column(db.Time, nullable=False)

