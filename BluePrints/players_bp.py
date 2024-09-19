from flask import Flask, request, jsonify, Blueprint
from models.players import Player
from services.db import db
from models.team_compare import Team

players_bp = Blueprint('players_bp', __name__)

#get the players by position
@players_bp.route('/positions/<string:position>', methods=['GET'])
@players_bp.route('/positions/<string:position>/<string:season>', methods=['GET'])
def get_players_by_position(position,season=None):
    players_query = Player.query.filter_by(position=position)
    if season:
        players_query = players_query.filter_by(season=season)

    players = players_query.all()

    players_grouped_by_id = {}
    for player in players:
        if player.player_id in players_grouped_by_id:
            players_grouped_by_id[player.player_id].append(player)
        else:
            players_grouped_by_id[player.player_id] = [player]

    players_and_stats = []
    for player_id, player_list in players_grouped_by_id.items():

        total_points = 0
        total_two_percent = 0
        total_three_percent = 0
        total_ATR = 0
        seasons = set()
        team = "Unknown"

        for player in player_list:
            total_points += player.points if player.points is not None else 0
            total_two_percent += player.two_percent if player.two_percent is not None else 0
            total_three_percent += player.three_percent if player.three_percent is not None else 0
            total_ATR += player.ATR if player.ATR is not None else 0
            seasons.add(player.season)
            team = player.team


        num_entries = len(player_list)
        avg_points = total_points / num_entries
        avg_two_percent = total_two_percent / num_entries
        avg_three_percent = total_three_percent / num_entries
        avg_ATR = total_ATR / num_entries


        player_to_print = {
            "player_id": player_id,
            "name": player_list[0].name,
            "team": team,
            "position": player_list[0].position,
            "points": avg_points,
            "two_percent": avg_two_percent,
            "three_percent": avg_three_percent,
            "ATR": avg_ATR,
            "seasons": list(seasons),
            "PPG_ratio": player_list[0].PPG_ratio
        }
        players_and_stats.append(player_to_print)

    return jsonify(players_and_stats)


@players_bp.route('/create_team', methods=['POST'])
def create_team():
    data = request.get_json()

    # קבלת פרטי הקבוצה מהבקשה
    name = data.get('name')
    pg_id = data.get('PG')
    sg_id = data.get('SG')
    sf_id = data.get('SF')
    pf_id = data.get('PF')
    c_id = data.get('C')

    # בדוק אם כל השדות נמסרו
    if not all([name, pg_id, sg_id, sf_id, pf_id, c_id]):
        return jsonify({"error": "All fields are required."}), 400

    # בדוק אם השחקנים קיימים
    player_ids = [pg_id, sg_id, sf_id, pf_id, c_id]
    for player_id in player_ids:
        if not Player.query.filter_by(player_id=player_id).first():
            return jsonify({"error": "One or more player IDs are invalid."}), 400

    # יצירת אובייקט קבוצה חדש
    new_team = Team(
        name=name,
        PG=pg_id,
        SG=sg_id,
        SF=sf_id,
        PF=pf_id,
        C=c_id
    )

    try:
        db.session.add(new_team)
        db.session.commit()
        return jsonify({"message": "Team created successfully!", "team": new_team.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating the team: " + str(e)}), 500

#get the player stats by player_id

