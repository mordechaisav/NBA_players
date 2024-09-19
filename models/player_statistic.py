from flask_sqlalchemy import SQLAlchemy
from models.players import Player
db = SQLAlchemy()


class PlayerStats(db.Model):
    __tablename__ = 'player_stats'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    position = db.Column(db.String(20), nullable=False)
    season = db.Column(db.String(10), nullable=False)
    games_played = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    two_percent = db.Column(db.Float, nullable=False)
    three_percent = db.Column(db.Float, nullable=False)
    ATR = db.Column(db.Float, nullable=False)
    PPG_ratio = db.Column(db.Float, nullable=False)
