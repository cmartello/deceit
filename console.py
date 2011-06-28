from Tournament import Tournament
from Player import Player
from re import search


def get_event_info():
    """Gather basic event information.  Note that this isn't user-proofed
    at all yet."""

    name, regnum = '', -1

    while name == '':
        name = raw_input('event name ->')

    while regnum == -1:
        regnum = int(raw_input('registration # (0 for none)->'))

    # TODO - automatically add the year and month to the registration number
    return (name, regnum)


def get_players(sanctioned = False):
    """Query the user for a list of players by name and PIN.  Only ask for
    their PIN if the match is offically sanctioned.
    Again, there is no user-proofing here."""

    print 'Enter player names below (blank line to stop)'
    global EVENT

    username = 'nothing'
    userpin = 0
    while username != '':
        username = raw_input('name ->')

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
            userpin = int(raw_input('pin  ->'))
            EVENT.add_player(Player(firstname, lastname, userpin))
        elif sanctioned == False:
            EVENT.add_player(Player(firstname, lastname))



if __name__ == '__main__':
    info = get_event_info()
    EVENT = Tournament(info[0], info[1])
    get_players()

