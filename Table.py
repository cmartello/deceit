class Table:
    def __init__(self, p1, p2):
        self.left = p1
        self.right = p2
        self.status = 'Active'


    def report_match(self, wins, losses, draws=0):
        """Reports the match for the specified table as wins-losses,draws
        for the left-hand side of the table.  The right-hand player's
        scores are derived from this."""
        if self.status == 'Locked':
            return -1
        self.left.record_match(self.right, wins, losses, draws)
        self.right.record_match(self.left, losses, wins, draws)
        self.status = 'Reported'


    def __str__(self):
        a = str(self.left.match_points()) + ' ' + self.left.lastname + ', ' + self.left.firstname
        b = str(self.right.match_points()) + ' ' + self.right.lastname + ', ' + self.right.firstname

        a = '%2d %s, %s' % (self.left.match_points(), self.left.lastname, self.left.firstname)
        b = '%2d %s, %s' % (self.right.match_points(), self.right.lastname, self.right.firstname)
        return '%-32s %-32s' % (a, b)


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
    from Player import player
    a = player('John', 'Cleese')
    b = player('Eric', 'Idle')
    print 'Before:'
    c = Table(a,b)
    print c
    print 'After:'
    c.report_match(2,1,0)
    print c
    print 'Inverse:'
    print c.inverse_copy()
