"""The Table module for deceit is used for tracking matches and aids in
reporting them.  Contains some test code at the very end.
"""

class Table:
    """Simple class representing each match.  Contains a 'left' and 'right'
    player object and a couple helper functions."""

    def __init__(self, left, right):
        """Creates a table object from two supplied player objects."""

        self.left = left
        self.right = right
        self.status = 'Active'

        # The dummy player BYE gets an auto-loss
        if self.left.firstname == 'BYE':
            self.report_match(0, 2)

        if self.right.firstname == 'BYE':
            self.report_match(2, 0)


    def report_match(self, wins, losses, draws=0):
        """Reports the match for the specified table as wins-losses,draws
        for the left-hand side of the table.  The right-hand player's
        scores are derived from this."""

        if self.status == 'Locked' or self.status == 'Reported':
            return -1
        self.left.record_match(self.right, wins, losses, draws)
        self.right.record_match(self.left, losses, wins, draws)
        self.status = 'Reported'


    def __str__(self):
        left = str(self.left.match_points()) + ' ' +\
            self.left.lastname + ', ' + self.left.firstname
        right = str(self.right.match_points()) + ' ' +\
            self.right.lastname + ', ' + self.right.firstname

        left = '%2d %s, %s' % (self.left.match_points(), \
            self.left.lastname, self.left.firstname)
        right = '%2d %s, %s' % (self.right.match_points(), \
            self.right.lastname, self.right.firstname)
        return '%-32s %-32s' % (left, right)


    def lock_table(self):
        """Called when going to a new round.  Merely prevents results from
        being altered further."""

        self.status = 'Locked'


    def inverse_copy(self):
        """When generating a printable pairings list, it is preferable to
        have all tables listed twice, one with the positions reversed,
        allowing players to find their table by last name quickly."""

        return Table(self.right, self.left)


# test code
if __name__ == '__main__':
    from Player import Player
    PLAYER1 = Player('John', 'Cleese')
    PLAYER2 = Player('Eric', 'Idle')
    print 'Before:'
    TESTTABLE = Table(PLAYER1, PLAYER2)
    print TESTTABLE
    print 'After:'
    TESTTABLE.report_match(2, 1, 0)
    print TESTTABLE
    print 'Inverse:'
    print TESTTABLE.inverse_copy()
