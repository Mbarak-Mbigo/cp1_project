#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.

Usage:
    amity create_room ( office | living ) <room_name>...
    amity add_person < person_name > < FELLOW | STAFF > [ wants_accommodation ]
    amity reallocate_person <person_identifier> <new_room_name>
    amity load_people <file>
    amity print_allocations [-o=filename]
    amity print_unallocated [-o=filename]
    print_available_space
    amity print_room <room_name>
    amity save_state [--db=sqlite_database]
    amity load_state <sqlite_database>
    amity (-i | --interactive)
    amity (-h | --help | --version)
Options:
    -i --interactive   Interactive Mode.
    -h --help          Show this screen and exit.
    -v --version       Show application version
    --wants_accommodation=<ac> accommodation for fellows [default:'N']

"""
# imports
import sys
import cmd
from docopt import docopt, DocoptExit
from pyfiglet import figlet_format
from termcolor import cprint

# local imports
from app.amity import Amity

docopt(__doc__, argv=None, help=True, version=0.1, options_first=False)


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive (cmd.Cmd):
    """Program interface."""

    intro = cprint(figlet_format('Amity', font='isometric3'), 'blue')
    print('\ntype help for a list of commands.\n')

    prompt = 'Amity-->>> '
    file = None
    amity = Amity()
    # load previous state
    amity.load_state()

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <type> <rooms>..."""
        self.amity.create_room(arg['<rooms>'], arg['<type>'])

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> <type>
        [--wants-accommodation='N']

        """
        name = arg['<first_name>'] + ' ' + arg['<last_name>']
        if not arg['--wants-accommodation']:
            self.amity.add_person(name, arg['<type>'], 'N')
        else:
            self.amity.add_person(name, arg['<type>'],
                                  arg['--wants-accommodation'])

    @docopt_cmd
    def do_allocate(self, arg):
        """Usage: allocate [--f=<firstname> --l=<lastname>]"""
        if arg['--f'] and arg['--l']:
            name = ' '.join([arg['--f'], arg['--l']])
            self.amity.allocate_room(name)
        else:
            if arg['--f'] or arg['--l']:
                cprint('If you are specifying a name, kindly provide'
                       '--f=<firstnam> and --l=lastname', 'red')
            else:
                self.amity.allocate_room()

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_identifier> <new_room_name>

        """
        self.amity.reallocate_person(arg['<person_identifier>'],
                                     arg['<new_room_name>'])

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people <file>

        """
        self.amity.load_people(arg['<file>'])

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=filename]

        """
        if not arg['--o']:
            self.amity.print_allocations()
        else:
            self.amity.print_allocations(arg['--o'])

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename]

        """
        if not arg['--o']:
            self.amity.print_unallocated()
        else:
            self.amity.print_unallocated(arg['--o'])

    @docopt_cmd
    def do_print_available_space(self, arg):
        """Usage: print_available_space"""
        self.amity.print_available_space()

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>

        """
        self.amity.print_room(arg['<room_name>'])

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db=sqlite_database]

        """
        if not arg['--db']:
            self.amity.save_state()
        else:
            self.amity.save_state(arg['--db'])

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state [--db=sqlite_database]

        """
        if not arg['--db']:
            self.amity.load_state()
        else:
            self.amity.load_state(arg['--db'])

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        cprint('Quiting amity... \nApplication exited successfully', 'white')
        exit()

    def do_q(self, arg):
        """Quits out of Interactive Mode."""

        cprint('Quiting amity... \nApplication exited successfully', 'white')
        exit()

opt = docopt(__doc__, sys.argv[1:])

# print(opt)

if opt['--interactive']:
    MyInteractive().cmdloop()

print(__doc__)
