from Player import player

if __name__ == '__main__':
    a = player('Stan', 'Marsh')
    b = player('Eric', 'Cartman')
    c = player('Kyle', 'Broflowski')
    d = player('Kenny', 'McCormick')

    # round 1
    a.record_match(b, 2, 1)
    b.record_match(a, 1, 2)
    c.record_match(d, 2, 0)
    d.record_match(c, 0, 2)

    # round 2
    a.record_match(c, 1, 2)
    c.record_match(a, 2, 1)
    b.record_match(d, 1, 0, 1)
    d.record_match(b, 0, 1, 1)

    print a
    print b
    print c
    print d
