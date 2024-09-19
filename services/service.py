from flask import Flask, request, jsonify
from flask import current_app as app
from models.players import db, Player

from models.player_stats import PlayerStats
import requests
def get_data_for_season(season):
    url = f'http://b8c40s8.143.198.70.30.sslip.io/api/PlayerDataTotals/season/{season}'
    response = requests.get(url)
    return response.json()

def load_data():
    with app.app_context():
        seasons = [2022,2023,2024]

        for season in seasons:
            data = get_data_for_season(season)
            for player_data in data:
                insert_player_to_db(player_data,season)

        calculate_PPG_ratio()

def insert_player_to_db(player_data,season):
    #check if player already exists
    player = Player.query.filter_by(player_id=player_data['playerId'], season=season,team=player_data['team']).first()
    if player:
        return player

    else:
        player = create_player_model(player_data)
        db.session.add(player)
        db.session.commit()
        return player


def create_player_model(player_data):
    player_id = player_data['playerId']
    player_name = player_data['playerName']
    position = player_data['position']
    points = player_data['points']
    two_percent = player_data['twoPercent']
    three_percent = player_data['threePercent']
    game_played = player_data['games']
    ATR = player_data['assists'] / player_data['turnovers'] if player_data['turnovers'] > 0 else player_data['assists']
    player = Player(player_id=player_id,name=player_name, position=position, points=points, two_percent=two_percent, three_percent=three_percent, games_played=game_played, ATR=ATR)
    return player

def create_player_stats_model(player_data, season):
    player_id = player_data['playerId']
    position = player_data['position']
    points = player_data['points']
    two_percent = player_data['twoPercent']
    three_percent = player_data['threePercent']
    game_played = player_data['games']
    ATR = player_data['assists'] / player_data['turnovers'] if player_data['turnovers'] > 0 else player_data['assists']

    player_stats = PlayerStats(player_id=player_id, season=season, position=position,games_played=game_played, points=points, two_percent=two_percent, three_percent=three_percent, ATR=ATR)
    return player_stats

def insert_player_stats_to_db(player_data, season):
    #check if player stats already exists
    player_stats = PlayerStats.query.filter_by(player_id=player_data['playerId'], season=season,team=player_data['team']).first()
    if player_stats:
        return player_stats
    player_stats = create_player_stats_model(player_data, season)
    db.session.add(player_stats)
    db.session.commit()
    return player_stats

def calculate_PPG_ratio():
    ppg_ratio ={}
    with app.app_context():
        all_players = PlayerStats.query.all()
        #group by position
        for position in ['PG', 'SG', 'SF', 'PF', 'C']:
            players_in_position = [player for player in all_players if player.position == position]

            position_average = sum([playerA.points for playerA in players_in_position]) / len(players_in_position)
            ppg_ratio[position] = position_average
        return ppg_ratio

