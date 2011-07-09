"""Contains the player object, the key of the program."""


class Player:
    """An object that tracks a player's status within a tournament.  Comes
    with a number of helper functions for determining scores beyond the
    basics.  A player must be given a first and last name, and a DCI PIN is
    optional."""

    def __init__(self, f_name, l_name, pin=0):
        """Spawns a player with the supplied first and last names and zero
        points with no recorded opponents."""

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
        return '(%d-%d) %s, %s' % (self.matches_won, self.matches_lost, \
            self.lastname, self.firstname)

    def long_report(self):
        """Prints out a slightly more detailed description of the player than
        that provided by __str__()."""

        print '%s, %s' % (self.lastname, self.firstname)
        print 'Matches : (%d) - %d - %d - %d' % (self.match_points(), \
            self.matches_won, self.matches_lost, self.matches_drawn)
        print 'Games : (%d) %d - %d - %d' % (self.game_points(), \
            self.games_won, self.games_lost, self.games_drawn)
        for opp in self.opponents:
            print opp[1], '-', opp[2], opp[0].lastname, ',', opp[0].firstname

    def record_match(self, opponent, win, lose, draw=0):
        """Key match recording function; accepts a player object in the
        opponent field and the relevant number of wins and losses.  The
        number of draws is an optional field, defaulting to 0."""

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
        """Returns the number of game points for this player."""

        return self.games_won * 3 + self.games_drawn * 1

    def match_points(self):
        """Returns the number of match points for this player."""

        return self.matches_won * 3 + self.matches_drawn * 1

    def game_win_percent(self):
        """Returns this player's game-win percentage for tiebreakers."""

        games = self.games_won + self.games_lost + self.games_drawn

        # avoid a div/0 bug
        if games == 0:
            return 1.0 / 3

        gwp = self.game_points() / (games * 3.0)

        # per the floor rules, a player's GWP is never below 0.333
        if gwp < 1.0 / 3:
            return 1.0 / 3
        else:
            return gwp

    def match_win_percent(self):
        """Returns this player's match-win percentage for tiebreakers."""

        matches = len(self.opponents)

        # avoid a div/0 bug
        if matches == 0:
            return 1.0 / 3

        mwp = self.match_points() / (matches * 3.0)

        # again per the floor rules, a player's MWP is never below 0.333
        if mwp < 1.0 / 3:
            return 1.0 / 3
        else:
            return mwp

    def opp_match_win_percent(self):
        """Returns the average of this player's opponent's match-win
        percentages."""

        # avoid a div/0 bug
        if len(self.opponents) == 0:
            return 1.0 / 3

        return sum([x[0].match_win_percent() for x in self.opponents])\
            / len(self.opponents)

    def opp_game_win_percent(self):
        """Returns the average of this player's opponent's game-win
        percentages."""

        # avoid a div/0 bug
        if len(self.opponents) == 0:
            return 1.0 / 3

        return sum([x[0].game_win_percent() for x in self.opponents])\
            / len(self.opponents)

    def set_status(self, status='drop'):
        """Changes the player's status from 'active' to something else.
        All non-active statuses are considered to have left the tournament
        and will therefore not be paired.
        Status choices:
            'drop' -- Player voluntarily left the event.
            'cut' -- Player did not advance to the next round.
            'disq' -- Player was disqualified.
        """

        # make sure that the status change is valid
        if status not in ['drop', 'cut', 'disq']:
            return -1
        else:
            self.status = status

    def won_most_recent(self):
        """Returns True if the player won their most recent match.  Useful
        for single-elimination events."""

        # Avoid an index out of range error
        if len(self.opponents) < 1:
            return False

        if self.opponents[-1][1] > self.opponents[-1][2]:
            return True
        else:
            return False
