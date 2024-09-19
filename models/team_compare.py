from flask_sqlalchemy import SQLAlchemy
from models.players import Player
db = SQLAlchemy()

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    PG = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    SG = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    SF = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    PF = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    C = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)


    point_guard = db.relationship('Player', foreign_keys=[PG])
    shooting_guard = db.relationship('Player', foreign_keys=[SG])
    small_forward = db.relationship('Player', foreign_keys=[SF])
    power_forward = db.relationship('Player', foreign_keys=[PF])
    center = db.relationship('Player', foreign_keys=[C])
