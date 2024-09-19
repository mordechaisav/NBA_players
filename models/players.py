from flask_sqlalchemy import SQLAlchemy
from services.db import db

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(80), nullable=True)
    position = db.Column(db.String(20), nullable=True)
    season = db.Column(db.String(10), nullable=True)
    games_played = db.Column(db.Integer, nullable=True)
    points = db.Column(db.Integer, nullable=True)
    two_percent = db.Column(db.Float, nullable=True, default=0.0)
    three_percent = db.Column(db.Float, nullable=True, default=0.0)
    ATR = db.Column(db.Float, nullable=True)
    team = db.Column(db.String(30), nullable=True)
    PPG_ratio = db.Column(db.Float, nullable=True)
    def to_dict(self):
        return {"id": self.id, "player_id": self.player_id, "name": self.name, "position": self.position, "season": self.season, "games_played": self.games_played, "points": self.points, "two_percent": self.two_percent, "three_percent": self.three_percent, "ATR": self.ATR, "team": self.team, "PPG_ratio": self.PPG_ratio}