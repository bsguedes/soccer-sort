from random import choice


class Teams:
    def __init__(self, team_a, team_b, index, score=None):
        self.team_a = team_a
        self.team_b = team_b
        self.index = index
        strngth = sum([p.hidden() for p in team_a]) - sum([p.hidden() for p in team_b])
        self.strength = abs(strngth)
        self.adv = "Azul" if strngth > 0 else "Vermelho"
        self.result = "" if score is None else ("Azul" if score[0] > score[1] else ("Vermelho" if score[1] > score[0] else "Empate"))
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
        balance = ("%.2f" % self.balance).ljust(10, ' ')
        strength = ("%.2f" % self.strength).ljust(10, ' ')
        adv = ("%s" % self.adv).ljust(10, ' ')
        blue_score = ("%i" % self.score[0] if self.score is not None else "").rjust(10, ' ')
        red_score = ("%i" % self.score[1] if self.score is not None else "").ljust(10, ' ')
        winner = ("%s" % self.result).rjust(10, ' ')
        aa = ("%i" % sum([p.hv[0] for p in self.team_a])).rjust(4, ' ')
        ad = ("%i" % sum([p.hv[1] for p in self.team_a])).rjust(4, ' ')
        at = ("%i" % sum([p.hv[2] for p in self.team_a])).rjust(4, ' '  )
        va = ("%i" % sum([p.hv[0] for p in self.team_b])).rjust(4, ' ')
        vd = ("%i" % sum([p.hv[1] for p in self.team_b])).rjust(4, ' ')
        vs = ("%i" % sum([p.hv[2] for p in self.team_b])).rjust(4, ' ')
        total = ("%.2f" % ((sum([p.hidden() for p in self.team_a]) + sum([p.hidden() for p in self.team_b]))/(len(self.team_a)+len(self.team_b)))).ljust(10, ' ')
        return "%s%s%s%s X %s%s %s%s%s%s%s%s  %s" %  (balance, strength, adv, blue_score, red_score, winner, aa, ad, at, va, vd, vs, total)
