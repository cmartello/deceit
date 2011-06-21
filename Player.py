class player:
    def __init__(self, f_name, l_name, pin=0):
        self.firstname = f_name
        self.lastname = l_name
        self.pin = pin
        self.opponents = []

        self.matches_won = 0
        self.matches_lost = 0
        self.matches_drawn = 0

        self.games_won = 0
        self.games_lost = 0
        self.games_drawn = 0

        self.status = 'active'


    def __str__(self):
        return '(%d-%d) %s, %s' % (self.matches_won, self.matches_lost, self.lastname, self.firstname)

    
    def long_report(self):
        print '%s, %s' % (self.lastname, self.firstname)
        print 'Matches : (%d) - %d - %d - %d' % ( self.match_points(), \
            self.matches_won, self.matches_lost, self.matches_drawn)
        print 'Games : (%d) %d - %d - %d' % ( self.game_points(), \
            self.games_won, self.games_lost, self.games_drawn)
        for x in self.opponents:
            print x[1], '-', x[2], x[0].lastname, ',', x[0].firstname

    
    def record_match(self, opponent, win, lose, draw=0):

        self.opponents.append((opponent, win, lose, draw))

        if win > lose:
            self.matches_won += 1
        elif lose > win:
            self.matches_lost += 1
        elif win == lose:
            self.matches_drawn += 1

        self.games_won += win
        self.games_lost += lose
        self.games_drawn += draw


    def game_points(self):
        return self.games_won * 3 + self.games_drawn * 1


    def match_points(self):
        return self.matches_won * 3 + self.matches_drawn * 1


    def game_win_percent(self):
        games = self.games_won + self.games_lost + self.games_drawn

        gwp = self.game_points() / (games * 3.0)

        if gwp < 1.0/3:
            return 1.0/3
        else:
            return gwp


    def match_win_percent(self):
        matches = len(self.opponents)

        mwp = self.match_points() / (matches*3.0)

        if mwp < 1.0/3:
            return 1.0/3
        else:
            return mwp

    def opp_match_win_percent(self):
        return sum([x[0].match_win_percent() for x in self.opponents]) / len(self.opponents)


    def opp_game_win_percent(self):
        return sum([x[0].game_win_percent() for x in self.opponents]) / len(self.opponents)
