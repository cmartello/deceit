"""The Tournament module is the top-level wrapper for everything else
that is likely to happen within a typical tournament."""

from random import shuffle
from Table import Table
from Player import Player
from math import ceil, log


def number_rounds(players, dci=False, top=8):
    """Calculates the number of swiss rounds before breaking to the top tier
    based on the number of players in the event.  Accepts two optional
    arguments that influence the number of rounds.

    In general, swiss rounds are determined by the ceiling of log_2(players)
    except that in a DCI preimere event, a modified chart is used for events
    with more than 128 players.

    Further, a break to top 4 requires one additonal round of swiss draw and
    a break to top 2 requires two additional rounds."""

    # solve 2^n = p for n and round n up -- the general number of swiss rounds
    base = int(ceil(log(players)/log(2)))

    # top n extra rounds.
    extra = 0
    if top == 4:
        extra = 1
    if top == 2:
        extra = 2

    # This is for the nasty chart at the end of the floor rules.
    if dci == True:
        if players >= 129 and players <= 226:
            base = 8
        if players >= 227 and players <= 409:
            base = 9
        if players >= 410:
            base = 10

    return base + extra


def point_sort(plx, ply):
    """Used by generate_pairings to sort players by points."""
    return plx.match_points() - ply.match_points()


def tiebreaker_sort(plx, ply):
    """Used for the top-8 break or final tiebreaker sort."""

    xscores, yscores = [], []

    # match points
    xscores.append(plx.match_points())
    yscores.append(ply.match_points())

    # opponent's match-win percentage
    xscores.append(plx.opp_match_win_percent())
    yscores.append(ply.opp_match_win_percent())

    # game-win percentage
    xscores.append(plx.game_win_percent())
    yscores.append(ply.game_win_percent())

    # opponent's game-win percentage
    xscores.append(plx.opp_game_win_percent())
    yscores.append(ply.opp_game_win_percent())

    for score in xrange(4):
        if xscores[score] > yscores[score]:
            return 1
        elif xscores[score] < yscores[score]:
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
        self.players = [Player('BYE', 'BYE')]
        self.round = 0
        self.tables = ['Nothing']


    def add_player(self, u_player):
        """Adds a player object to the tournament's list of players."""

        if self.round < 1:
            self.players.append(u_player)
        else:
            return -1


    def active_tables(self):
        """Returns a list of currently active tables if applicable.  Otherwise
        returns an empty list."""

        if self.round < 1:
            return []

        return [x for x in self.tables[self.round] if x.status == 'Active']


    def start_round(self):
        """Starts a new round if there's no active tables.  If there are open
        tables, it returns a list of those tables.  Otherwise, it returns
        True."""

        tables = self.active_tables()
        if len(tables) > 0:
            return tables
        self.generate_pairings()
        self.round += 1
        return True


    def finish_round(self):
        """If there are no currently active tables, finish_round simply locks
        all tables and returns true.  Otherwise, returns the active table
        list."""

        tables = self.active_tables()
        if len(tables) > 0:
            return tables
        for table in self.tables[self.round]:
            table.lock_table()
        return True


    def generate_pairings(self):
        """Generates pairings for the current round, first by shuffling the
        player list and then sorting by points.  The player with the lowest
        point total when there's an uneven number of players will get a bye.

        Pairings should not be generated mid-round; this is prevented by
        Tournament.start_round()
        """

        # Dummy table; only in place to make tables index from 1
        nobody = Player('NOBODY', 'NOBODY')
        pairings = [Table(nobody, nobody)]

        if len(self.players[1:]) % 2 == 0:
            plist = self.players[1:]
        else:
            plist = self.players[:]
        shuffle(plist)
        plist.sort(point_sort)
        while len(plist) > 1:
            pairings.append(Table(plist.pop(), plist.pop()))
        self.tables.append(pairings)


    def report_match(self, tableno, wins, losses, draws=0):
        """Reports the match for the specified table as wins-losses,draws
        for the left-hand side of the table.  The right-hand player's
        scores are derived from this.
        """
        if self.round < 1:
            return -1
        self.tables[self.round][tableno].report_match(wins, losses, draws)


    def list_tables(self, showall=False):
        """Lists the tables that are still playing in the event.  If all
        is True, it will instead list all tables.
        Deprecated -- Will be moved to console UI."""

        if self.round < 1:
            return -1

        if showall == True:
            for tnum in xrange(1, len(self.tables[self.round])):
                print '%3d' % tnum, self.tables[self.round][tnum]
        elif showall == False:
            for tnum in xrange(1, len(self.tables[self.round])):
                if self.tables[self.round][tnum].status == 'Active':
                    print '%3d' % tnum, self.tables[self.round][tnum]


    def list_pairings(self):
        """Prints out a list of all pairings with tables duplicated so that
        players can find their proper table easier.
        Deprecated -- Will be moved to console UI."""

        atables = self.tables[self.round][1:]
        btables = [atables[x].inverse_copy() for x in xrange(len(atables))]
        for count in xrange(len(atables)):
            atables[count].number = count + 1
            btables[count].number = count + 1
        all_tables = atables + btables
        all_tables.sort(table_sort)
        for table in all_tables:
            print '%3d' % table.number, table


    def top_players(self, players=8):
        """Performs a tiebreaker and returns the top n players where n is
        typically 8."""

        all_players = self.players[:]
        all_players.sort(tiebreaker_sort)
        return all_players[-players:]
