from flask_sqlalchemy import SQLAlchemy
from models.players import Player
from services.db import db

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    PG = db.Column(db.Integer, nullable=False)
    SG = db.Column(db.Integer, nullable=False)
    SF = db.Column(db.Integer, nullable=False)
    PF = db.Column(db.Integer, nullable=False)
    C = db.Column(db.Integer, nullable=False)

