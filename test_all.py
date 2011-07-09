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
