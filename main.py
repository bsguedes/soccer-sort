import random
import loader
from teams import Teams
import argparse

simulations = 5000

next_match = loader.load_next_match()
players = loader.load_player_list()
games = loader.load_games_list()

parser = argparse.ArgumentParser()
parser.add_argument('-b', action='store_true')
parser.add_argument('-s', action='store_true')
args = parser.parse_args()    

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
    print("\nBalance   Strength  Adv             Azul X Vermelho      Winner   AA  AD  AS  VA  VD  VS  Avg.")
    for game in games:
        blue = [[q for q in players if q.name == p][0] for p in game['Azul']['players']]
        red = [[q for q in players if q.name == p][0] for p in game['Vermelho']['players']]
        score_blue = game['Azul']['score']
        score_red = game['Vermelho']['score']
        teams = Teams(blue, red, 0, [score_blue, score_red])
        tie = []
        if score_blue == score_red:
            blue_result = 0
            red_result = 0
        else:
            blue_result = 1 if score_blue > score_red else -1
            red_result = 1 if score_red > score_blue else -1
        for p in blue:
            p.add_match_result(blue_result)
        for p in red:
            p.add_match_result(red_result)
        update_matches(teams.team_a, teams.team_b)
        update_matches(teams.team_b, teams.team_a)
        print(teams)
    
    # run simulations
    teams = generate_teams([[q for q in players if q.name == p][0] for p in next_match])
    str_team = sort_by(teams, 'strength')
    bal_team = sort_by(teams, 'balance')
    if args.b:
        teams, index = bal_team[0], 0
    elif args.s:
        teams, index = str_team[0], 0
    else:
        teams, index = find_first_common(str_team, bal_team)
    
    for p in sorted(players, key=lambda e:e.name):
        print("\n")
        print(p)
        print("      " + " ".join(sorted(["%s: %s" % (q.name, i) for q, i in p.players.items()])))

    print("\n Current Rank \n")
    print("Name                Sc   J   V   E   D")
    for p in sorted(players, key=lambda e:e.hidden(), reverse=True):
        name = p.name.ljust(15, ' ')
        score = ("%.2f" % p.hidden()).rjust(6, ' ')
        j = ("%i" % len(p.wins)).rjust(3, ' ')
        v = ("%i" % len([1 for x in p.wins if x == 1])).rjust(3, ' ')
        e = ("%i" % len([1 for x in p.wins if x == 0])).rjust(3, ' ')
        d = ("%i" % len([1 for x in p.wins if x == -1])).rjust(3, ' ')

        print("%s %s %s %s %s %s" % (name, score, j, v, e, d))

    print("\nNext teams should be:")
    print("TEAM Azul: %s" % ", ".join([p.name for p in sorted(teams.team_a, key=lambda e:e.name)]))
    print("TEAM Vermelho: %s" % ", ".join([p.name for p in sorted(teams.team_b, key=lambda e:e.name)]))
    print("\nBalance   Strength  Adv             Azul X Vermelho      Winner   AA  AD  AS  VA  VD  VS  Avg.")
    print(str(teams))