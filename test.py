from Player import player
from Tournament import Tournament
from random import randint

if __name__ == '__main__':
    event = Tournament('Test Event')
    for x in open('player_names.txt').readlines():
        x = x.strip('\n')
        first, last = x.split(' ')
        event.add_player(player(first, last))
    event.generate_pairings()
    print 'Round ', event.round
    event.list_tables(all=True)

    # generate results
    for x in xrange(4):
        for x in xrange(len(event.tables)):
            wins, losses, draws = 0, 0, 0

            while (wins+losses+draws) < 3:
                result = randint(1,100)
                if result <= 45:
                    wins += 1
                elif result >= 55:
                    losses += 1
                else:
                    draws += 1

            event.report_match(x, wins, losses, draws)

        event.generate_pairings()
        print 'Round :', event.round
        event.list_tables(all=True)
