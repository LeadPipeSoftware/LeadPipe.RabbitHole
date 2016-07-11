"""Functions related to console output."""

from __future__ import print_function

    # Foreground    Code    Style       Code    Background  Code
    # ----------------------------------------------------------
    # Black         30      No effect   0       Black       40
    # Red       	31      Bold        1       Red         41
    # Green         32      Underline   4   	Green   	42
    # Yellow	    33	    Blink	    5	    Yellow	    43
    # Blue	        34	    Inverse	    7	    Blue	    44
    # Purple	    35	    Hidden	    8	    Purple	    45
    # Cyan	        36		                    Cyan	    46
    # White	        37                 			White	    47

def write_divider():
    """Writes a divider line to the console.
    """
    print('-' * 80)


def write_error(message):
    """Writes an error message to the console.

    :param message: The message to write.
    """
    print('\033[1;31;40m+ ERROR: \033[0m{0}'.format(message))


def write_keyvaluepair(key, value):
    """Writes a key and a value pair message to the console.

    :param key: The key value.
    :param value: The value.
    """
    print('\033[0;36;40m{0}:\033[0m \033[0;37;40m{1}\033[0m'.format(key, value))


def write_simulated_update(message):
    """Writes an update message to the console when simulating something.

    :param message: The message to write.
    """
    print('\033[0;32;40m+ \033[0;35;40m{0}\033[0m'.format(message))


def write_title(program_name, program_version):
    """Writes the program title to the console.

    :param program_name: The name of the program.
    :param program_version: The version of the program.
    """
    print('\033[0;33;40m{0} v{1}\033[0m'.format(program_name, program_version))
    write_divider


def write_update(message):
    """Writes an update message to the console.

    :param message: The message to write.
    """
    print('\033[0;32;40m+ \033[0m{0}'.format(message))
    