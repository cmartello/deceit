from Player import Player
from Tournament import Tournament
from random import randint

if __name__ == '__main__':
    event = Tournament('Test Event')
    for x in open('player_names.txt').readlines():
        x = x.strip('\n')
        first, last = x.split(' ')
        event.add_player(Player(first, last))

    for x in xrange(5):
        event.start_round()
        print 'Round: ', event.round

        event.list_tables(showall=True)

        for match in event.tables[event.round]:
            y = randint(1,100)
            if y < 25:
                match.report_match(2,1)
            if y >= 25 and y < 50:
                match.report_match(2,0)
            if y >= 50 and y < 75:
                match.report_match(1,2)
            if y >= 75 and y < 100:
                match.report_match(0,2)

        event.finish_round()
