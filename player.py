class Player:
    def __init__(self, name, atk, dfs, sta, gk=False):
        self.name = name
        self.players = {}
        self.wins = []
        self.hv = [atk, dfs, sta]
        self.gk = gk
        self.rate = 1.05

    def add_match_with_player(self, player, same_team):
        if player not in self.players:
            self.players[player] = 0
        self.players[player] += (1 if same_team else -1)

    def add_match_result(self, win):
        self.wins.append(win)

    def current_balance(self):
        return sum([self.players[player] ** 2 for player in self.players])

    def simulated_balance(self, my_team, their_team):
        my_team_score = sum([(self.players[player] + 1) ** 2 for player in my_team if player in self.players])
        their_team_score = sum([(self.players[player] - 1) ** 2 for player in their_team if player in self.players])
        return their_team_score + my_team_score

    def hidden(self):
        return self.base() * (self.rate ** self.recent())

    def base(self):
        return (self.hv[0] * 2 + self.hv[1] * 2 + self.hv[2] * 2) / 6.0

    def delta(self):
        return 100 * (self.hidden() - self.base()) / self.base()

    def recent(self):
        return sum(self.wins)

    def __str__(self):
        return "%s W-%i L-%i %.2f %.3f %.1f %%" % \
               (self.name, len([x for x in self.wins if x > 0]),
                len([x for x in self.wins if x < 0]), self.base(), self.hidden(), self.delta())
