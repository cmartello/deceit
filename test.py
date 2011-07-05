""" test.py -- A simple script for testing the Tournament module by simulating
a short 32-player tournament and outputting the results.
"""

from Player import Player
from Tournament import Tournament
from random import randint
from console import list_tables, list_standings

if __name__ == '__main__':
    EVENT = Tournament('Test Event')
    for x in open('player_names.txt').readlines():
        x = x.strip('\n')
        first, last = x.split(' ')
        EVENT.add_player(Player(first, last))

    for x in xrange(5):
        EVENT.start_round()
        print 'Round: ', EVENT.round

        list_tables(EVENT, showall=True)

        for match in EVENT.tables[EVENT.round]:
            y = randint(1, 100)
            if y < 25:
                match.report_match(2, 1)
            if y >= 25 and y < 50:
                match.report_match(2, 0)
            if y >= 50 and y < 75:
                match.report_match(1, 2)
            if y >= 75 and y <= 100:
                match.report_match(0, 2)

        EVENT.finish_round()

    for x in EVENT.top_players():
        print x

    list_standings(EVENT, byscore=True)

    # now a test of the round-robin code.  Just for laughs, well use the
    # top eight players from the 'main event'.
    TOP8 = EVENT.top_players()

    # create new event
    RROBIN = Tournament('Round Robin Test', pairing='round')
    for x in TOP8:
        RROBIN.add_player(x)

    RROBIN.start_round()

    for x in RROBIN.tables[1:]:
        for y in x[1:]:
            print y
        print
