from flask import Flask, request, jsonify, Blueprint
from models.players import Player
from services.db import db
from models.team_compare import Team
from services.service import calculate_stats_list_of_players

players_bp = Blueprint('players_bp', __name__)

#get the players by position
@players_bp.route('/positions/<string:position>', methods=['GET'])
@players_bp.route('/positions/<string:position>/<string:season>', methods=['GET'])
def get_players_by_position(position,season=None):
    players_query = Player.query.filter_by(position=position)
    if season:
        players_query = players_query.filter_by(season=season)

    players = players_query.all()
    if not players:
        return jsonify({"error": f"No players found for position {position}"}), 404
    players_grouped_by_id = {}
    for player in players:
        if player.player_id in players_grouped_by_id:
            players_grouped_by_id[player.player_id].append(player)
        else:
            players_grouped_by_id[player.player_id] = [player]

    players_and_stats = calculate_stats_list_of_players(players_grouped_by_id)


    return jsonify(players_and_stats)


@players_bp.route('/create_team', methods=['POST'])
def create_team():
    data = request.get_json()


    name = data.get('name')
    pg_id = data.get('PG')
    sg_id = data.get('SG')
    sf_id = data.get('SF')
    pf_id = data.get('PF')
    c_id = data.get('C')

    if not all([name, pg_id, sg_id, sf_id, pf_id, c_id]):
        return jsonify({"error": "All fields are required."}), 400


    player_ids = [pg_id, sg_id, sf_id, pf_id, c_id]
    for player_id in player_ids:
        if not Player.query.filter_by(player_id=player_id).first():
            return jsonify({"error": "One or more player IDs are invalid."}), 400


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

#updat team
@players_bp.route('/teams/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    data = request.get_json()

    name = data.get('name')
    pg_id = data.get('PG')
    sg_id = data.get('SG')
    sf_id = data.get('SF')
    pf_id = data.get('PF')
    c_id = data.get('C')

    if not all([name, pg_id, sg_id, sf_id, pf_id, c_id]):
        return jsonify({"error": "All fields are required."}), 400

    team = Team.query.get_or_404(team_id)
    if team is None:
        return jsonify({"error": "Team not found."}), 404
    if not Player.query.filter_by(player_id=pg_id).first():
        return jsonify({"error": "One or more player IDs are invalid."}), 400
    if not Player.query.filter_by(player_id=sg_id).first():
        return jsonify({"error": "One or more player IDs are invalid."}), 400
    if not Player.query.filter_by(player_id=sf_id).first():
        return jsonify({"error": "One or more player IDs are invalid."}), 400
    if not Player.query.filter_by(player_id=pf_id).first():
        return jsonify({"error": "One or more player IDs are invalid."}), 400
    if not Player.query.filter_by(player_id=c_id).first():
        return jsonify({"error": "One or more player IDs are invalid."}), 400

    team.name = name
    team.PG = pg_id
    team.SG = sg_id
    team.SF = sf_id
    team.PF = pf_id
    team.C = c_id

    try:
        db.session.commit()
        return jsonify({"message": "Team updated successfully!", "team": team.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while updating the team: " + str(e)}), 500

#get the team
@players_bp.route('/teams/<int:team_id>', methods=['GET'])
def get_team(team_id):
    team = Team.query.get_or_404(team_id)

    if team is None:
        return jsonify({"error": "Team not found."}), 404
    players_id = [team.PG, team.SG, team.SF, team.PF, team.C]
    players = Player.query.filter(Player.player_id.in_(players_id)).all()

    if not players:
        return jsonify({"error": "No players found for this team."}), 404

    team_players = {}
    for player in players:
        if player.player_id not in team_players:
            team_players[player.player_id] = [player]
        else:
            team_players[player.player_id].append(player)



    team_players_and_stats = calculate_stats_list_of_players(team_players)
    if not team_players_and_stats:
        return jsonify({"error": "No players found for this team."}), 404
    return jsonify(team_players_and_stats)

#delete team
@players_bp.route('/teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)

    if team is None:
        return jsonify({"error": "Team not found."}), 404

    try:
        db.session.delete(team)
        db.session.commit()
        return jsonify({"message": "Team deleted successfully!", "team_id": team_id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the team: " + str(e)}), 500



