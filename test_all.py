"""A crude attempt at unit-testing DeCeIt."""

from Player import Player
from Table import Table
import Tournament

# Player tests

PLA = Player('John', 'Sheridan')
PLB = Player('Jeffrey', 'Sinclair')

print PLA
PLA.long_report()

print 'PLA.game_points() : ', PLA.game_points()
print 'PLA.match_points() : ', PLA.match_points()
print 'PLA.game_win_percent() : ', PLA.game_win_percent()
print 'PLA.match_win_percent() : ', PLA.match_win_percent()
print 'PLA.opp_match_win_percent() : ', PLA.opp_match_win_percent()
print 'PLA.opp_game_win_percent() : ', PLA.opp_game_win_percent()
print 'PLA.won_most_recent() : ', PLA.won_most_recent()
print 'PLA.set_status() (BAD) : ', PLA.set_status('badvalue')
PLA.set_status('drop')
print 'PLA.set_status result : ', PLA.status

# respawn player A
PLA = Player('John', 'Sheridan')

# Match report
PLA.record_match(PLB, 2, 1)
PLB.record_match(PLA, 1, 2)

print 'After match report (2-1 in favor of PLA):'

print PLA
PLA.long_report()

print 'PLA.game_points() : ', PLA.game_points()
print 'PLA.match_points() : ', PLA.match_points()
print 'PLA.game_win_percent() : ', PLA.game_win_percent()
print 'PLA.match_win_percent() : ', PLA.match_win_percent()
print 'PLA.opp_match_win_percent() : ', PLA.opp_match_win_percent()
print 'PLA.opp_game_win_percent() : ', PLA.opp_game_win_percent()
print 'PLA.won_most_recent() : ', PLA.won_most_recent()

PLA.record_match(PLB, 0, 0, 1)
PLB.record_match(PLA, 0, 0, 1)

print 'After match report (draw) :'

print PLA
PLA.long_report()

print 'PLA.game_points() : ', PLA.game_points()
print 'PLA.match_points() : ', PLA.match_points()
print 'PLA.game_win_percent() : ', PLA.game_win_percent()
print 'PLA.match_win_percent() : ', PLA.match_win_percent()
print 'PLA.opp_match_win_percent() : ', PLA.opp_match_win_percent()
print 'PLA.opp_game_win_percent() : ', PLA.opp_game_win_percent()
print 'PLA.won_most_recent() : ', PLA.won_most_recent()


# make b lose another round
PLB.record_match(PLA, 0, 2)
PLA.record_match(PLB, 2, 0)
print 'PLB.game_win_percent() : ', PLB.game_win_percent()

# Table tests

PLA = Player('John', 'Sheridan')
PLB = Player('Jeffrey', 'Sinclair')
PLC = Player('BYE', 'BYE')
TA0 = Table(PLA, PLB)
TA1 = Table(PLC, PLA)
TA2 = Table(PLB, PLC)

print TA0
TA0.report_match(2, 1)
TA0.lock_table()
print TA0.report_match(1, 2)
print TA0.inverse_copy()
print TA1
print TA2

# Tournament module tests

# Tournament.number_rounds() tests
print 'Tournament.number_rounds(192, True, 4):', \
    Tournament.number_rounds(192, True, 4)
print 'Tournament.number_rounds(384, True, 2):', \
    Tournament.number_rounds(384, True, 2)
print 'Tournament.number_rounds(512, True):', \
    Tournament.number_rounds(512, True)

# Tournament simulation
PF_NAMES = ['Jeffrey', 'John', 'Micheal', 'Steven', 'Warren', 'Zack', \
    'Susan', 'Marcus']
PL_NAMES = ['Sinclair', 'Sheridan', 'Garibaldi', 'Franklin', 'Keffer', \
    'Allen', 'Ivanova', 'Cole']

EVENT = Tournament.Tournament('Test event')

for x in xrange(8):
    EVENT.add_player(Player(PF_NAMES[x], PL_NAMES[x]))

print 'Attempting to report a match too early: ', \
    EVENT.report_match(1, 2, 1)

for y in xrange(3):
    EVENT.start_round()

    if y == 0:
        print 'Attempting to add a late player: ', \
            EVENT.add_player(Player('Late', 'Jerk'))
        print 'Attempting to start a started round: ', \
            type(EVENT.start_round())
        print "Attempting to finish a round that isn't over: ", \
            type(EVENT.finish_round())

    # show all the tables
    for x in sorted(EVENT.tables[EVENT.round][1:], Tournament.table_sort):
        print x
    print

    EVENT.report_match(1, 2, 0)
    EVENT.report_match(2, 1, 1)
    EVENT.report_match(3, 2, 1)

    # drop player 8 after the first round
    if y == 0:
        EVENT.report_match(4, 0, 2)
        EVENT.players[7].set_status('drop')

    EVENT.finish_round()

# show players in order
for x in EVENT.top_players():
    print x

# create a round-robin schedule
EVENT2 = Tournament.Tournament('Test for Round Robin', pairing='robin')

for x in xrange(8):
    EVENT2.add_player(Player(PF_NAMES[x], PL_NAMES[x]))

EVENT2.start_round()

# do a couple rounds of single elimination
EVENT3 = Tournament.Tournament('Single-elimination test', pairing='single')

for x in xrange(8):
    EVENT3.add_player(Player(PF_NAMES[x], PL_NAMES[x]))

EVENT3.start_round()
EVENT3.report_match(1, 2, 0)
EVENT3.report_match(2, 0, 2)
EVENT3.report_match(3, 2, 1)
EVENT3.report_match(4, 1, 2)
EVENT3.finish_round()
EVENT3.start_round()

# do a round of single-elimination with four players, seeded
EVENT4 = Tournament.Tournament('Single-elimination test 2', pairing='single')
print 'Event 4 pairing:', EVENT4.pairing

for x in [x for x in EVENT3.players[1:] if x.status == 'active']:
    EVENT4.add_player(x)

EVENT4.start_round()

EVENT5 = Tournament.Tournament('Round-robin with byes', pairing='robin')
print 'Event 5 pairing:', EVENT5.pairing


for x in xrange(7):
    EVENT5.add_player(Player(PF_NAMES[x], PL_NAMES[x]))

EVENT5.start_round()

# create an event with an invalid pairing method
EVENT6 = Tournament.Tournament('Invalid', pairing='foobarbaz')
