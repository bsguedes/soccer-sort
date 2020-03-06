from random import choice


class Teams:
    def __init__(self, team_a, team_b, index, score=None):
        self.team_a = team_a
        self.team_b = team_b
        self.index = index
        strngth = sum([p.hidden() for p in team_a]) - sum([p.hidden() for p in team_b])
        self.strength = abs(strngth)
        self.adv = "A" if strngth > 0 else "B"
        self.score = score
        self.balance = abs(sum([a.simulated_balance(team_a, team_b) for a in team_a]) +
                           sum([a.simulated_balance(team_b, team_a) for a in team_b]))

    def get_winner(self):
        ta_str = int(sum([p.base() for p in self.team_a]))
        tb_str = int(sum([p.base() for p in self.team_b]))
        choices = [0] * ta_str + [1] * tb_str
        return self.team_a if choice(choices) == 0 else self.team_b

    def valid(self):
        gk_a = len([p for p in self.team_a if p.gk])
        gk_b = len([p for p in self.team_b if p.gk])
        return gk_a + gk_b < 2 or (gk_a >= 1 and gk_b >= 1)

    def __str__(self):
        score_str = "" if self.score is None else "A %i x %i B" % (self.score[0], self.score[1])  
        return "Teams balance %.2f --- strDelta: %.2f (%s) - %s" % (self.balance, self.strength, self.adv, score_str)
