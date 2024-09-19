from flask import Flask
from services.db import db
from services import service
from BluePrints.players_bp import players_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nba_players.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()
    service.load_data()
app.register_blueprint(players_bp)
if __name__ == '__main__':
    app.run(debug=True)