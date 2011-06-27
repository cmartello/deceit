from Tournament import Tournament
from re import search


def get_event_info():
    """Gather basic event information.  Note that this isn't user-proofed
    at all yet."""

    name, regnum = '', -1

    while name == '':
        name = raw_input('event name ->')

    while regnum == -1:
        regnum == int(raw_input('registration # (0 for none)->'))

    # TODO - automatically add the year and month to the registration number
    return (name, regnum)


def get_players(sanctioned = False):
    """Query the user for a list of players by name and PIN.  Only ask for
    their PIN if the match is offically sanctioned."""
    pass


if __name__ == '__main__':
    info = get_event_info()
    event = Tournament(info[0], info[1])


