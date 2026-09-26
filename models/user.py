from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    firstName = db.Column(db.String(64), nullable=True)
    lastName = db.Column(db.String(64), nullable=True)

    avatar = db.Column(db.String(64), nullable=True)
    admin = db.Column(db.Boolean, default=False)

    active = db.Column(db.Boolean, default=True)
    # authProvider = db.Column(db.String(64), nullable=True)  # TODO: Temp, map to provdier table
    authProvider = db.Column(db.Integer, nullable=1)  # TODO: Temp, map to provdier table