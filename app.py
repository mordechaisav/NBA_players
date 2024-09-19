import os
from flask import Flask
from services.db import db
from services import service
from BluePrints.players_bp import players_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nba_players.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db_file = 'instance/nba_players.db'

# Check if the database file exists
if not os.path.exists(db_file):
    with app.app_context():
        db.init_app(app)
        db.create_all()
        service.load_data()
else:
    db.init_app(app)

app.register_blueprint(players_bp)

if __name__ == '__main__':
    app.run(debug=True)
