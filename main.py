import random
import loader
from teams import Teams

simulations = 5000

next_match = loader.load_next_match()
players = loader.load_player_list()
games = loader.load_games_list()
    

def generate_teams(player_list):
    team_list = []
    for i in range(simulations):
        random.shuffle(player_list)
        team = Teams(player_list[:len(player_list)//2], player_list[len(player_list)//2:], i)
        if team.valid():
            team_list .append(team)
    return team_list


def sort_by(team_list, criteria):
    result = sorted(teams, 
                    key=lambda e: e.strength if criteria == 'strength' else sorted(team_list, key=lambda g: g.balance))
    return result


def find_first_common(a, b):
    la = []
    lb = []
    for i in range(len(a)):
        la.append(a[i].index)
        lb.append(b[i].index)
        intersection = [x for x in la if x in lb]
        if len(intersection) > 0:
            idx = intersection[0]
            return [p for p in a if p.index == idx][0], i


def update_matches(team_a, team_b):
    for p in team_a:
        for q in team_a:
            if p != q:
                p.add_match_with_player(q, True)
        for q in team_b:
            p.add_match_with_player(q, False)


if __name__ == "__main__":
    # load history
    for game in games:
        winner = [[q for q in players if q.name == p][0] for p in game['winner']]
        loser = [[q for q in players if q.name == p][0] for p in game['loser']]
        teams = Teams(winner, loser, 0)
        for p in winner:
            p.add_match_result(True)
        for p in loser:
            p.add_match_result(False)
        update_matches(teams.team_a, teams.team_b)
        update_matches(teams.team_b, teams.team_a)
        print(teams)
    
    # run simulations
    teams = generate_teams([[q for q in players if q.name == p][0] for p in next_match])
    str_team = sort_by(teams, 'strength')
    bal_team = sort_by(teams, 'balance')
    teams, index = find_first_common(str_team, bal_team)
    print("Next teams should be:")
    print("TEAM A: %s" % ", ".join([p.name for p in teams.team_a]))
    print("TEAM B: %s" % ", ".join([p.name for p in teams.team_b]))
    print(index, str(teams))
    
    for p in sorted(players, key=lambda e:e.name):
        print("\n")
        print(p)
        print("      " + " ".join(sorted(["%s: %s" % (q.name, i) for q, i in p.players.items()])))
