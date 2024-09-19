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
        player = create_player_model(player_data,season)
        db.session.add(player)
        db.session.commit()
        return player


def create_player_model(player_data,season):
    player_id = player_data['playerId']
    player_name = player_data['playerName']
    position = player_data['position']
    points = player_data['points']
    two_percent = player_data['twoPercent']
    three_percent = player_data['threePercent']
    game_played = player_data['games']
    team = player_data['team']
    ATR = player_data['assists'] / player_data['turnovers'] if player_data['turnovers'] > 0 else player_data['assists']
    player = Player(player_id=player_id,name=player_name,season=season, position=position, points=points, two_percent=two_percent, three_percent=three_percent, games_played=game_played, ATR=ATR, team=team)
    return player


def calculate_PPG_ratio():
    ppg_ratio ={}
    with app.app_context():
        all_players = Player.query.all()
        #group by position
        for position in ['PG', 'SG', 'SF', 'PF', 'C']:
            players_in_position = [player for player in all_players if player.position == position]

            position_average = sum([playerA.points for playerA in players_in_position]) / len(players_in_position)
            ppg_ratio[position] = position_average
        for player in all_players:
            if len(player.position) == 2:
                player.PPG_ratio = ppg_ratio[player.position]
            db.session.commit()
            print(f'PPG ratio for {player.name} is {player.PPG_ratio}')
        return ppg_ratio

def calculate_stats_list_of_players(players):
    players_and_stats = []
    for player_id, player_list in players.items():

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
    return players_and_stats