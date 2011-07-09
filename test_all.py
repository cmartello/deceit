from Player import Player
from Table import Table

# Player tests

a = Player('John', 'Sheridan')
b = Player('Jeffrey', 'Sinclair')

print a
a.long_report()

print 'a.game_points() : ', a.game_points()
print 'a.match_points() : ', a.match_points()
print 'a.game_win_percent() : ', a.game_win_percent()
print 'a.match_win_percent() : ', a.match_win_percent()
print 'a.opp_match_win_percent() : ', a.opp_match_win_percent()
print 'a.opp_game_win_percent() : ', a.opp_game_win_percent()
print 'a.won_most_recent() : ', a.won_most_recent()
print 'a.set_status() (BAD) : ', a.set_status('badvalue')
a.set_status('drop')
print 'a.set_status result : ', a.status

# respawn player A
a = Player('John', 'Sheridan')

# Match report
a.record_match(b, 2, 1)
b.record_match(a, 1, 2)

print 'After match report (2-1 in favor of a):'

print a
a.long_report()

print 'a.game_points() : ', a.game_points()
print 'a.match_points() : ', a.match_points()
print 'a.game_win_percent() : ', a.game_win_percent()
print 'a.match_win_percent() : ', a.match_win_percent()
print 'a.opp_match_win_percent() : ', a.opp_match_win_percent()
print 'a.opp_game_win_percent() : ', a.opp_game_win_percent()
print 'a.won_most_recent() : ', a.won_most_recent()

a.record_match(b,0,0,1)
b.record_match(a,0,0,1)

print 'After match report (draw) :'

print a
a.long_report()

print 'a.game_points() : ', a.game_points()
print 'a.match_points() : ', a.match_points()
print 'a.game_win_percent() : ', a.game_win_percent()
print 'a.match_win_percent() : ', a.match_win_percent()
print 'a.opp_match_win_percent() : ', a.opp_match_win_percent()
print 'a.opp_game_win_percent() : ', a.opp_game_win_percent()
print 'a.won_most_recent() : ', a.won_most_recent()


# make b lose another round
b.record_match(a,0,2)
a.record_match(b,2,0)
print 'b.game_win_percent() : ', b.game_win_percent()

# Table tests

a = Player('John', 'Sheridan')
b = Player('Jeffrey', 'Sinclair')
c = Player('BYE', 'BYE')
t = Table(a,b)
tb1 = Table(c,a)
tb2 = Table(b,c)

print t
t.report_match(2,1)
t.lock_table()
print t.report_match(1,2)
print t.inverse_copy()
print tb1
print tb2
