from random import shuffle
from Table import Table
from Player import player


def point_sort(x, y):
    """Used by generate_pairings to sort players by points."""
    return x.match_points() - y.match_points()


def tiebreaker_sort(x, y):
    # match points
    xmp, ymp = x.match_points(), y.match_points()
    if xmp != ymp:
        return xmp - ymp

    # opponent's match-win percentage
    xomw, yomw = x.opp_match_win_percent(), y.opp_match_win_percent()
    if xomw > yomw:
        return 1
    elif xomw < yomw:
        return -1

    # game-win percentage
    xgwp, ygwp = x.game_win_percent(), y.game_win_percent()
    if xgwp > ygwp:
        return 1
    elif xgwp < ygwp:
        return -1

    # opponent's game-win percentage
    xogwp, yogwp = x.opp_game_win_percent(), y.opp_game_win_percent()
    if xogwp > yogwp:
        return 1
    elif xogwp < yogwp:
        return -1

    # unbroken tie
    return 0


def table_sort(x, y):
    return cmp(x.left.lastname, y.left.lastname)


class Tournament:
    def __init__(self, event_name, regnum = 0):
        self.players = [player('BYE', 'BYE')]
        self.state = 'signup'
        self.round = 0


    def add_player(self, player):
        if self.state == 'signup':
            self.players.append(player)
        else:
            return -1


    def generate_pairings(self):
        # don't regenerate pairings mid-round!
        if self.state == 'playing':
            return -1

        self.tables = [Table(player('NOBODY', 'NOBODY'), player('NOBODY', 'NOBODY'))]

        if len(self.players[1:]) % 2 == 0:
            a = self.players[1:]
        else:
            a = self.players[:]
        shuffle(a)
        a.sort(point_sort)
        self.round += 1
        while len(a) > 1:
            self.tables.append(Table(a.pop(), a.pop()))


    def report_match(self, tableno, wins, losses, draws=0):
        """Reports the match for the specified table as wins-losses,draws
        for the left-hand side of the table.  The right-hand player's
        scores are derived from this.
        """
        if self.round < 1:
            return -1
        self.tables[tableno].report_match(wins, losses, draws)


    def list_tables(self, all=False):
        """Lists the tables that are still playing in the event.  If all
        is True, it will instead list all tables."""

        if self.round < 1:
            return -1

        if all == True:
            for x in xrange(1,len(self.tables)):
                print '%3d' % x, self.tables[x]
        elif all == False:
            for x in xrange(1,len(self.tables)):
                if self.tables[x].status == 'Active':
                    print '%3d' % x, self.tables[x]


    def list_pairings(self):
        """Prints out a list of all pairings with tables duplicated so that
        players can find their proper table easier."""
        a = self.tables[1:]
        b = [a[x].inverse_copy() for x in xrange(len(a))]
        for x in xrange(len(a)):
            a[x].number = x + 1
            b[x].number = x + 1
        c = a + b
        c.sort(table_sort)
        for x in c:
            print '%3d' % x.number, x
