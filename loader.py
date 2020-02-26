import json
from player import Player


def load_next_match():
    content = open('_next_match.json', 'r', encoding='utf-8').read()
    return json.loads(content)


def load_player_list():
    players = []
    content = open('_players.json', 'r', encoding='utf-8').read()
    for player in json.loads(content):
        n = player["name"]
        a = player["atk"]
        d = player["def"]
        s = player["sta"]
        g = "gk" in player and player["gk"]
        players.append(Player(n, a, d, s, g))
    return players


def load_games_list():
    content = open('_matches.json', 'r', encoding='utf-8').read()
    return json.loads(content)
