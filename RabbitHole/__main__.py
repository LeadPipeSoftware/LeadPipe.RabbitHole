"""RabbitHole: RabbitHole is a RabbitMQ message utility."""

from __future__ import print_function

import logging
import os
import sys
from timeit import default_timer as timer

from RabbitHole import __program_name__
from RabbitHole import __version__
from RabbitHole.command_line_arguments import CommandLineArguments
from RabbitHole.configuration import Configuration
from RabbitHole.console import Console
from RabbitHole.replay_command import ReplayCommand
from RabbitHole.snag_command import SnagCommand
from RabbitHole.queue_command import QueueCommand

print = lambda x: sys.stdout.write("%s\n" % x)


def main(args=None):
    """The program entry point."""

    # Get the command line args...
    command_line_arguments = CommandLineArguments()
    parsed_arguments = command_line_arguments.parsed_arguments

    # Set up logging...
    log_format = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
    if parsed_arguments.debug:
        logging.basicConfig(filename=__program_name__ + '.log', filemode='w', level=logging.DEBUG, format=log_format)
    else:
        logging.basicConfig(filename=__program_name__ + '.log', filemode='w', level=logging.INFO, format=log_format)
    logger = logging.getLogger(__name__)
    logger.info('{0} {1}'.format(__program_name__, __version__))
    logger.info('Debug mode: {0}'.format(parsed_arguments.debug))

    # Set the configuration...
    config = Configuration(logger, parsed_arguments)

    # Fire up the console...
    console = Console(config)

    console.display_welcome(__program_name__, __version__)

    start = timer()

    if config.command_line_arguments.command == 'snag':
        snag_command = SnagCommand(config, console, logger)
        snag_command.execute()
    elif config.command_line_arguments.command == 'replay':
        replay_command = ReplayCommand(config, console, logger)
        replay_command.execute()
    elif config.command_line_arguments.command == 'queue':
        queue_command = QueueCommand(config, console, logger)
        if os.path.isfile(config.command_line_arguments.message_source_file):
            queue_command.queue_file()
        elif os.path.isdir(config.command_line_arguments.message_source_file):
            queue_command.queue_folder()
        else:
            print('\033[1;31;40m+ ERROR: \033[0m{0} is not a file or a folder!'.format(
                config.command_line_arguments.message_source_file))

    end = timer()
    if not config.silent:
        # Make sure we didn't jack with the user's terminal colors
        print('\033[0;32;40m+ \033[0mDone in {0}!\033[0m\n'.format(end - start))
    # sys.exit()


if __name__ == "__main__":
    main()
    # try:
    #     main()
    # except KeyboardInterrupt:
    #     print('Cancelled by user')
    #     sys.exit(0)
    # except AttributeError:
    #     sys.exit(0)
    # except:
    #     print("Unexpected error: {0}".format(sys.exc_info()[0]))
    #     sys.exit(1)
