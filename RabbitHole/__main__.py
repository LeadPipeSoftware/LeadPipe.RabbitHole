"""RabbitHole: RabbitHole is a RabbitMQ message utility."""

from __future__ import print_function

import argparse
import sys

import message as msg
import rabbitmq as rabbit

PROGRAM_NAME = 'RabbitHole'
PROGRAM_VERSION = '1.0.0'

AUTHORIZATION_STRING_GUEST = 'Basic Z3Vlc3Q6Z3Vlc3Q='  # guest/guest
AUTHORIZATION_STRING_RABBIT = 'Basic cmFiYml0OnJhYmJpdA=='  # rabbit/rabbit

DEFAULT_RABBITMQ_HOST_URL = 'http://localhost'
DEFAULT_RABBITMQ_PORT = 15672
DEFAULT_RABBITMQ_VHOST = '%2F'


def main(args=None):
    """The program entry point."""

    args = parse_command_line_arguments()

    display_welcome(args)

    if args.command == 'snag':
        snag(args)
    elif args.command == 'replay':
        replay(args)
    elif args.command == 'queue':
        queue(args)

    print('\033[0;32;40m+ \033[0mDone!\033[0m\n')  # Make sure we didn't jack with the user's terminal colors
    sys.exit()


def parse_command_line_arguments():
    """Parses the command line arguments.

    :return: The parsed command line arguments.
    """

    parser = argparse.ArgumentParser(add_help=True, description='A RabbitMQ message utility.', version='1.0')

    # Common arguments
    parser.add_argument('-r', '--rabbit_host_url', default=DEFAULT_RABBITMQ_HOST_URL, help='the RabbitMQ host URL')
    parser.add_argument('-p', '--rabbit_port', type=int, default=DEFAULT_RABBITMQ_PORT, help='the RabbitMQ port')
    parser.add_argument('-s', '--rabbit_vhost', default=DEFAULT_RABBITMQ_VHOST, help='the RabbitMQ vhost name')
    parser.add_argument('-z',
                        '--rabbit_authorization_string',
                        default=AUTHORIZATION_STRING_GUEST,
                        help='the authorization string for the RabbitMQ request header')
    parser.add_argument('--simulate', action='store_true')
    parser.add_argument('--verbose', action='store_true')

    subparsers = parser.add_subparsers(help='commands', dest='command')

    # Snag command
    snag_parser = subparsers.add_parser('snag',
                                        help='Snags messages from a queue and saves them to a JSON-formatted file')

    snag_parser.add_argument('-q',
                             '--message_source_queue',
                             required=True,
                             help='The name of the RabbitMQ source queue to get the messages from')
    snag_parser.add_argument('-m', '--message_count', required=True, help='The number of messages to requeue')
    snag_parser.add_argument('-a',
                             '--save_file',
                             required=True,
                             help='the file to save the JSON message to - PREVENTS RE-QUEUEING')

    # Replay command
    replay_parser = subparsers.add_parser('replay', help='Replays messages in a queue')

    replay_parser.add_argument('-q',
                               '--message_source_queue',
                               required=True,
                               help='The name of the RabbitMQ source queue to get the messages from')
    replay_parser.add_argument('-m', '--message_count', required=True, help='The number of messages to requeue')
    replay_parser.add_argument('-d',
                               '--rabbit_destination_queue',
                               required=True,
                               help='The name of the RabbitMQ destination queue')

    # Queue command
    queue_parser = subparsers.add_parser('queue', help='Sends messages to a queue from a JSON-formatted file')

    queue_parser.add_argument('-d',
                              '--rabbit_destination_queue',
                              required=True,
                              help='The name of the RabbitMQ destination queue')
    queue_parser.add_argument('-f', '--message_source_file', required=True, help='the message source file')

    # Parse the arguments
    return parser.parse_args()


def display_welcome(args):
    """Displays the program welcome message.

    :param args: The command line arguments.
    :return:
    """

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

    print('\033[0;33;40m{0} v{1}\033[0m'.format(PROGRAM_NAME, PROGRAM_VERSION))
    print('-' * 80)

    if args.verbose:
        print('\033[0;36;40m   Host URL:\033[0m \033[0;37;40m{0}\033[0m'.format(args.rabbit_host_url))
        print('\033[0;36;40m       Port:\033[0m \033[0;37;40m{0}\033[0m'.format(args.rabbit_port))
        print('\033[0;36;40m      VHost:\033[0m \033[0;37;40m{0}\033[0m'.format(args.rabbit_vhost))
        print('\033[0;36;40mAuth String:\033[0m \033[0;37;40m{0}\033[0m'.format(args.rabbit_authorization_string))
        print('-' * 80)

    if args.simulate:
        print('Output in \033[0;35;40mthis color\033[0m indicates a simulated step!')
        print('-' * 80)


def snag(args):
    """Saves messages from a queue to a JSON-formatted file.

    :param args: The command line arguments.
    :return:
    """

    if args.verbose:
        print('\033[0;36;40mMessage Count:\033[0m \033[0;37;40m{0}\033[0m'.format(args.message_count))
        print('\033[0;36;40m Source Queue:\033[0m \033[0;37;40m{0}\033[0m'.format(args.message_source_queue))
        print('\033[0;36;40m    Save File:\033[0m \033[0;37;40m{0}\033[0m'.format(args.save_file))
        print('-' * 80)

    if args.simulate:
        print('\033[0;32;40m+ \033[0;35;40m(simulating)\033[0m Get {0} messages from {1}...'.format(args.message_count,
                                                                                                    args.message_source_queue))
        print(
        '\033[0;32;40m+ \033[0;35;40m(simulating)\033[0m Save RabbitMQ messages to {0}...'.format(args.save_file))
    else:
        messages = rabbit.get_rabbit_messages_from_queue(args.message_count,
                                                         args.rabbit_host_url,
                                                         args.rabbit_port,
                                                         args.rabbit_vhost,
                                                         args.message_source_queue,
                                                         args.rabbit_authorization_string,
                                                         True,
                                                         args.verbose)
        msg.save_rabbit_messages_to_file(messages, args.save_file)


def replay(args):
    """Replays messages in a queue.

    :param args: The command line arguments.
    :return:
    """

    if args.verbose:
        print('\033[0;36;40m    Message Count:\033[0m \033[0;37;40m{0}\033[0m'.format(args.message_count))
        print('\033[0;36;40m     Source Queue:\033[0m \033[0;37;40m{0}\033[0m'.format(args.message_source_queue))
        print('\033[0;36;40mDestination Queue:\033[0m \033[0;37;40m{0}\033[0m'.format(args.rabbit_destination_queue))
        print('-' * 80)

    if args.simulate:
        print('\033[0;32;40m+ \033[0;35;40m(simulating)\033[0m Get {0} messages from {1}...'.format(args.message_count,
                                                                                                    args.message_source_queue))
        print('\033[0;32;40m+ \033[0;35;40m(simulating)\033[0m Publish messages to {0}...'.format(
            args.rabbit_destination_queue))
    else:
        messages = rabbit.get_rabbit_messages_from_queue(args.message_count,
                                                         args.rabbit_host_url,
                                                         args.rabbit_port,
                                                         args.rabbit_vhost,
                                                         args.message_source_queue,
                                                         args.rabbit_authorization_string,
                                                         True,
                                                         args.verbose)
        rabbit.publish_messages(messages,
                                args.rabbit_host_url,
                                args.rabbit_port,
                                args.rabbit_vhost,
                                args.rabbit_authorization_string,
                                args.rabbit_destination_queue,
                                args.verbose)


def queue(args):
    """Sends messages to a queue from a JSON-formatted file.

    :param args: The command line arguments.
    :return:
    """

    if args.verbose:
        print('\033[0;36;40m      Source File:\033[0m \033[0;37;40m{0}\033[0m'.format(args.message_source_file))
        print('\033[0;36;40mDestination Queue:\033[0m \033[0;37;40m{0}\033[0m'.format(args.rabbit_destination_queue))
        print('-' * 80)

    messages = msg.get_rabbit_messages_from_file(args.message_source_file, args.verbose)
    rabbit.publish_messages(messages,
                            args.rabbit_host_url,
                            args.rabbit_port,
                            args.rabbit_vhost,
                            args.rabbit_authorization_string,
                            args.rabbit_destination_queue,
                            args.verbose,
                            args.simulate)


if __name__ == "__main__":
    sys.exit(main())
