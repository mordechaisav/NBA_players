from flask_sqlalchemy import SQLAlchemy
from services.db import db

class PlayerStats(db.Model):
    __tablename__ = 'player_stats'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.player_id'), nullable=True)
    position = db.Column(db.String(20), nullable=True)
    season = db.Column(db.String(10), nullable=True)
    games_played = db.Column(db.Integer, nullable=True)
    points = db.Column(db.Integer, nullable=True)
    two_percent = db.Column(db.Float, nullable=True,default=0.0)
    three_percent = db.Column(db.Float, nullable=True, default=0.0)
    ATR = db.Column(db.Float, nullable=True)
    team = db.Column(db.String(30), nullable=True)
    PPG_ratio = db.Column(db.Float, nullable=True)
