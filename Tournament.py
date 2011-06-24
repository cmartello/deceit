"""The Tournament module is the top-level wrapper for everything else
that is likely to happen within a typical tournament."""

from random import shuffle
from Table import Table
from Player import player


def point_sort(plx, ply):
    """Used by generate_pairings to sort players by points."""
    return plx.match_points() - ply.match_points()


def tiebreaker_sort(plx, ply):
    """Used for the top-8 break or final tiebreaker sort."""
    # match points
    xmp, ymp = plx.match_points(), ply.match_points()
    if xmp > ymp:
        return 1
    if xmp < ymp:
        return -1

    # opponent's match-win percentage
    xomw, yomw = plx.opp_match_win_percent(), ply.opp_match_win_percent()
    if xomw > yomw:
        return 1
    elif xomw < yomw:
        return -1

    # game-win percentage
    xgwp, ygwp = plx.game_win_percent(), ply.game_win_percent()
    if xgwp > ygwp:
        return 1
    elif xgwp < ygwp:
        return -1

    # opponent's game-win percentage
    xogwp, yogwp = plx.opp_game_win_percent(), ply.opp_game_win_percent()
    if xogwp > yogwp:
        return 1
    elif xogwp < yogwp:
        return -1

    # unbroken tie
    return 0


def table_sort(plx, ply):
    """A simple last-name sort for Table objects."""
    return cmp(plx.left.lastname, ply.left.lastname)


class Tournament:
    """Module that encapsulates all relevant tournament functions."""

    def __init__(self, event_name, regnum = 0):
        """Starts a tournament.  Requires a name for the event, and you may
        optionally supply a registration number for DCI-sanctioned events.
        Note that the year and day fields will be automatically added, though
        this code is still in the future."""

        self.event_name = event_name
        self.regnum = regnum
        self.players = [player('BYE', 'BYE')]
        self.state = 'signup'
        self.round = 0


    def add_player(self, u_player):
        """Adds a player object to the tournament's list of players."""
        if self.state == 'signup':
            self.players.append(u_player)
        else:
            return -1


    def generate_pairings(self):
        """Generates pairings for the current round, first by shuffling the
        player list and then sorting by points.  The player with the lowest
        point total when there's an uneven number of players will get a bye.
        """

        # don't regenerate pairings mid-round!
        if self.state == 'playing':
            return -1

        # Dummy table; only in place to make tables index from 1
        nobody = player('NOBODY', 'NOBODY')
        self.tables = [Table(nobody, nobody)]

        if len(self.players[1:]) % 2 == 0:
            plist = self.players[1:]
        else:
            plist = self.players[:]
        shuffle(plist)
        plist.sort(point_sort)
        self.round += 1
        while len(plist) > 1:
            self.tables.append(Table(plist.pop(), plist.pop()))


    def report_match(self, tableno, wins, losses, draws=0):
        """Reports the match for the specified table as wins-losses,draws
        for the left-hand side of the table.  The right-hand player's
        scores are derived from this.
        """
        if self.round < 1:
            return -1
        self.tables[tableno].report_match(wins, losses, draws)


    def list_tables(self, showall=False):
        """Lists the tables that are still playing in the event.  If all
        is True, it will instead list all tables."""

        if self.round < 1:
            return -1

        if showall == True:
            for tnum in xrange(1, len(self.tables)):
                print '%3d' % tnum, self.tables[tnum]
        elif showall == False:
            for tnum in xrange(1, len(self.tables)):
                if self.tables[tnum].status == 'Active':
                    print '%3d' % tnum, self.tables[tnum]


    def list_pairings(self):
        """Prints out a list of all pairings with tables duplicated so that
        players can find their proper table easier."""
        atables = self.tables[1:]
        btables = [atables[x].inverse_copy() for x in xrange(len(atables))]
        for count in xrange(len(atables)):
            atables[count].number = count + 1
            btables[count].number = count + 1
        all_tables = atables + btables
        all_tables.sort(table_sort)
        for table in all_tables:
            print '%3d' % table.number, table
