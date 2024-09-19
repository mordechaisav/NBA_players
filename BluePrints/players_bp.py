from flask import Flask, request, jsonify, Blueprint
from models.players import Player
from models.player_stats import PlayerStats
from services.service import calculate_PPG_ratio

players_bp = Blueprint('players_bp', __name__)

#get the players by position
@players_bp.route('/position/<string:position>', methods=['GET'])
def get_players_by_position(position):
    players = Player.query.filter_by(position=position).all()
    players_and_stats = []
    for player in players:
        stats = PlayerStats.query.filter_by(player_id=player.id).all()
        points, two_percent, three_percent, ATR = 0, 0, 0, 0
        seasons = []
        team = ''
        if stats:

            if len(stats) > 0:

                for i in range(len(stats)):
                    points += stats[i].points
                    two_percent += stats[i].two_percent
                    three_percent += stats[i].three_percent
                    ATR += stats[i].ATR
                    if stats[i].season not in seasons:
                        seasons.append(stats[i].season)
                team = stats[0].team

                points /= len(stats)
                two_percent /= len(stats)
                three_percent /= len(stats)
                ATR /= len(stats)
        PPG_ratio = calculate_PPG_ratio()
        player_to_print = {"name":player.name,"team":team,"position":player.position,"points":points,"two_percent":two_percent,"three_percent":three_percent,"ATR":ATR,"seasons":seasons,"PPG_ratio":PPG_ratio[position]  }
        players_and_stats.append(player_to_print)
    return jsonify(players_and_stats)
