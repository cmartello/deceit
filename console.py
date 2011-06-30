"""The console-based user interface for DeCeIt."""

from Tournament import Tournament, table_sort, number_rounds
from Player import Player
from re import search


def list_tables(tournament, showall=False):
    """Lists the tables that are still playing in the event.  If all
    is True, it will instead list all tables.
    Deprecated -- Will be moved to console UI."""

    if tournament.round < 1:
        return -1

    if showall == True:
        for tnum in xrange(1, len(tournament.tables[tournament.round])):
            print '%3d' % tnum, tournament.tables[tournament.round][tnum]
    elif showall == False:
        for tnum in xrange(1, len(tournament.tables[tournament.round])):
            if tournament.tables[tournament.round][tnum].status == 'Active':
                print '%3d' % tnum, tournament.tables[tournament.round][tnum]


def list_pairings(tournament):
    """Prints out a list of all pairings with tables duplicated so that
    players can find their proper table easier.
    Deprecated -- Will be moved to console UI."""

    atables = tournament.tables[tournament.round][1:]
    btables = [atables[x].inverse_copy() for x in xrange(len(atables))]
    for count in xrange(len(atables)):
        atables[count].number = count + 1
        btables[count].number = count + 1
    all_tables = atables + btables
    all_tables.sort(table_sort)
    for table in all_tables:
        print '%3d' % table.number, table


def get_event_info():
    """Gather basic event information.  Note that this isn't user-proofed
    at all yet."""

    name, regnum = '', -1

    while name == '':
        name = raw_input('event name -> ')

    while regnum == -1:
        regnum = int(raw_input('registration # (0 for none)->'))

    # TODO - automatically add the year and month to the registration number
    return (name, regnum)


def get_players(sanctioned=False):
    """Query the user for a list of players by name and PIN.  Only ask for
    their PIN if the match is offically sanctioned.
    Again, there is no user-proofing here.
    TODO - make this work with a Tournament object passed to it.
    TODO - user-proof the input."""

    print 'Enter player names below (blank line to stop)'   

    username = 'nothing'
    userpin = 0
    while username != '':
        username = raw_input('name -> ')

        if username == '':
            break

        # for names of the form "John Smith"
        rex = search('(\w+) (\w+)', username)
        if rex is not None:
            firstname, lastname = rex.group(1), rex.group(2)

        # for names of the form "Smith, John"
        rex = search('(\w+),( |)(\w+)', username)
        if rex is not None:
            firstname, lastname = rex.group(3), rex.group(1)

        # commit this stuff to the event
        if sanctioned == True:
            userpin = int(raw_input('pin  -> '))
            EVENT.add_player(Player(firstname, lastname, userpin))
        elif sanctioned == False:
            EVENT.add_player(Player(firstname, lastname))


if __name__ == '__main__':
    INFO = get_event_info()
    EVENT = Tournament(INFO[0], INFO[1])
    get_players()

    ROUNDS = number_rounds(len(EVENT.players))

    # main event-reporting loop
    while EVENT.round < ROUNDS:
        EVENT.start_round()

        ACTIVE = len(EVENT.active_tables())
        while ACTIVE > 0:
            CMD = raw_input('Round #%d (%d tables open) -> ' % \
                (EVENT.round, ACTIVE))
            if search('lt', CMD) is not None:
                list_tables(EVENT)
                continue
            if search('lat', CMD) is not None:
                list_tables(EVENT, True)
                continue
            if search('^r ', CMD) is not None:
                BROKEN = CMD.split(' ')
                if len(BROKEN) == 2:
                    # ask for results
                    pass
                if len(BROKEN) == 4:
                    # report as table broken[1] (broken[2]-broken[3])
                    EVENT.report_match(int(BROKEN[1]), int(BROKEN[2]), \
                        int(BROKEN[3]))
                    ACTIVE = len(EVENT.active_tables())
        EVENT.finish_round()
