from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    position = db.Column(db.String(20), nullable=False)
