from random import shuffle

def point_sort(x, y):
    """Used by generate_pairings to sort players by points."""
    return x.match_points() - y.match_points()


class Tournament:
    def __init__(self, event_name, regnum = 0):
        self.players = []
        self.state = 'signup'
        self.round = 0


    def add_player(self, player):
        if self.state == 'signup':
            self.players.append(player)
        else:
            return -1


    def generate_pairings(self):
        self.tables = []
        self.round += 1
        a = self.players[:]
        shuffle(a)
        a.sort(point_sort)
        while len(a) > 1:
            self.tables.append((a.pop(), a.pop()))


    def report_match(self, tableno, wins, losses, draws):
        """Reports the match for the specified table as wins-losses,draws
        for the left-hand side of the table.  The right-hand player's
        scores are derived from this."""
        if self.round < 1:
            return -1
        self.tables[tableno][0].record_match(self.tables[tableno][1],\
            wins, losses, draws)

        self.tables[tableno][1].record_match(self.tables[tableno][0],\
            losses, wins, draws)


    def list_tables(self):
        if self.round < 1:
            return -1

        for x in xrange(len(self.tables)):
            print x, self.tables[x][0], self.tables[x][1]

