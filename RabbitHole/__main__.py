"""RabbitHole: RabbitHole is a RabbitMQ message utility."""

from __future__ import print_function

import argparse
import os
import sys
import threading

import RabbitHole.message as msg
import RabbitHole.rabbitmq as rabbit

PROGRAM_NAME = 'RabbitHole'
PROGRAM_VERSION = '1.0.0'

AUTHORIZATION_STRING_GUEST = 'Basic Z3Vlc3Q6Z3Vlc3Q='  # guest/guest
AUTHORIZATION_STRING_RABBIT = 'Basic cmFiYml0OnJhYmJpdA=='  # rabbit/rabbit

DEFAULT_RABBITMQ_HOST_URL = 'http://localhost'
DEFAULT_RABBITMQ_PORT = 15672
DEFAULT_RABBITMQ_VHOST = '%2F'


def main(args=None):
    """The program entry point."""

    global PARSED_ARGS
    PARSED_ARGS = parse_command_line_arguments()

    display_welcome()

    if PARSED_ARGS.command == 'snag':
        snag()
    elif PARSED_ARGS.command == 'replay':
        replay()
    elif PARSED_ARGS.command == 'queue':
        if os.path.isfile(PARSED_ARGS.message_source_file):
            queue_file()
        elif os.path.isdir(PARSED_ARGS.message_source_file):
            queue_folder()
        else:
            print('\033[1;31;40m+ ERROR: \033[0m{0} is not a file or a folder!'.format(PARSED_ARGS.message_source_file))

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


def display_welcome():
    """Displays the program welcome message.

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

    if PARSED_ARGS.verbose:
        print('\033[0;36;40m   Host URL:\033[0m \033[0;37;40m{0}\033[0m'.format(PARSED_ARGS.rabbit_host_url))
        print('\033[0;36;40m       Port:\033[0m \033[0;37;40m{0}\033[0m'.format(PARSED_ARGS.rabbit_port))
        print('\033[0;36;40m      VHost:\033[0m \033[0;37;40m{0}\033[0m'.format(PARSED_ARGS.rabbit_vhost))
        print('\033[0;36;40mAuth String:\033[0m \033[0;37;40m{0}\033[0m'.format(PARSED_ARGS.rabbit_authorization_string))
        print('-' * 80)

    if PARSED_ARGS.simulate:
        print('Output in \033[0;35;40mthis color\033[0m indicates a simulated step!')
        print('-' * 80)


def snag():
    """Saves messages from a queue to a JSON-formatted file.

    :return:
    """

    if PARSED_ARGS.verbose:
        print('\033[0;36;40mMessage Count:\033[0m \033[0;37;40m{0}\033[0m'.format(PARSED_ARGS.message_count))
        print('\033[0;36;40m Source Queue:\033[0m \033[0;37;40m{0}\033[0m'.format(PARSED_ARGS.message_source_queue))
        print('\033[0;36;40m    Save File:\033[0m \033[0;37;40m{0}\033[0m'.format(PARSED_ARGS.save_file))
        print('-' * 80)

    messages = rabbit.get_rabbit_messages_from_queue(PARSED_ARGS.message_count,
                                                     PARSED_ARGS.rabbit_host_url,
                                                     PARSED_ARGS.rabbit_port,
                                                     PARSED_ARGS.rabbit_vhost,
                                                     PARSED_ARGS.message_source_queue,
                                                     PARSED_ARGS.rabbit_authorization_string,
                                                     True,
                                                     PARSED_ARGS.verbose)

    msg.save_rabbit_messages_to_file(messages, PARSED_ARGS.save_file, PARSED_ARGS.simulate)


def replay():
    """Replays messages in a queue.

    :return:
    """

    if PARSED_ARGS.verbose:
        print('\033[0;36;40m    Message Count:\033[0m \033[0;37;40m{0}\033[0m'.format(PARSED_ARGS.message_count))
        print('\033[0;36;40m     Source Queue:\033[0m \033[0;37;40m{0}\033[0m'.format(PARSED_ARGS.message_source_queue))
        print('\033[0;36;40mDestination Queue:\033[0m \033[0;37;40m{0}\033[0m'.format(PARSED_ARGS.rabbit_destination_queue))
        print('-' * 80)

    messages = rabbit.get_rabbit_messages_from_queue(PARSED_ARGS.message_count,
                                                     PARSED_ARGS.rabbit_host_url,
                                                     PARSED_ARGS.rabbit_port,
                                                     PARSED_ARGS.rabbit_vhost,
                                                     PARSED_ARGS.message_source_queue,
                                                     PARSED_ARGS.rabbit_authorization_string,
                                                     True,
                                                     PARSED_ARGS.verbose)

    rabbit.publish_messages(messages,
                            PARSED_ARGS.rabbit_host_url,
                            PARSED_ARGS.rabbit_port,
                            PARSED_ARGS.rabbit_vhost,
                            PARSED_ARGS.rabbit_authorization_string,
                            PARSED_ARGS.rabbit_destination_queue,
                            PARSED_ARGS.verbose,
                            PARSED_ARGS.simulate)


def queue_file():
    """Sends messages to a queue from a JSON-formatted file.

    :return:
    """

    if PARSED_ARGS.verbose:
        print('\033[0;36;40m      Source File:\033[0m \033[0;37;40m{0}\033[0m'.format(PARSED_ARGS.message_source_file))
        print('\033[0;36;40mDestination Queue:\033[0m \033[0;37;40m{0}\033[0m'.format(PARSED_ARGS.rabbit_destination_queue))
        print('-' * 80)

    messages = msg.get_rabbit_messages_from_file(PARSED_ARGS.message_source_file, PARSED_ARGS.verbose)

    rabbit.publish_messages(messages,
                            PARSED_ARGS.rabbit_host_url,
                            PARSED_ARGS.rabbit_port,
                            PARSED_ARGS.rabbit_vhost,
                            PARSED_ARGS.rabbit_authorization_string,
                            PARSED_ARGS.rabbit_destination_queue,
                            PARSED_ARGS.verbose,
                            PARSED_ARGS.simulate)


def queue_files(message_source_files):
    """Sends messages to a queue from a list of JSON-formatted files.

    :return:
    """

    # if PARSED_ARGS.verbose:
    #     print('\033[0;36;40m      Source File:\033[0m \033[0;37;40m{0}\033[0m'.format(message_source_file))
    #     print('\033[0;36;40mDestination Queue:\033[0m \033[0;37;40m{0}\033[0m'.format(PARSED_ARGS.rabbit_destination_queue))
    #     print('-' * 80)

    for message_source_file in message_source_files:
        messages = msg.get_rabbit_messages_from_file(message_source_file, PARSED_ARGS.verbose)
        rabbit.publish_messages(messages,
                                PARSED_ARGS.rabbit_host_url,
                                PARSED_ARGS.rabbit_port,
                                PARSED_ARGS.rabbit_vhost,
                                PARSED_ARGS.rabbit_authorization_string,
                                PARSED_ARGS.rabbit_destination_queue,
                                PARSED_ARGS.verbose,
                                PARSED_ARGS.simulate)


def queue_folder():
    """Sends messages to a queue from all JSON-formatted files in a folder.

        :return:
        """

    number_of_threads = 10

    message_files = msg.get_rabbit_message_files_in_folder(PARSED_ARGS.message_source_file)

    number_of_message_files_per_thread = len(message_files) // number_of_threads # Note floor division via // operator

    chunks = get_chunks(message_files, number_of_message_files_per_thread)

    print('\033[0;36;40m    Source Folder:\033[0m \033[0;37;40m{0}\033[0m'.format(PARSED_ARGS.message_source_file))
    print('\033[0;36;40mDestination Queue:\033[0m \033[0;37;40m{0}\033[0m'.format(PARSED_ARGS.rabbit_destination_queue))
    print('\033[0;36;40m       File Count:\033[0m \033[0;37;40m{0}\033[0m'.format(len(message_files)))
    print('\033[0;36;40m Max Thread Count:\033[0m \033[0;37;40m{0}\033[0m'.format(number_of_threads))
    print('\033[0;36;40m Files Per Thread:\033[0m \033[0;37;40m{0}\033[0m'.format(number_of_message_files_per_thread))
    print('-' * 80)

    thread_list = []

    # Build the threads...
    for chunk in chunks:
        t = threading.Thread(target=queue_files, args=(chunk,))
        thread_list.append(t)

    # Start the threads...
    for thread in thread_list:
        thread.start()

    # Join the threads (block the caller until every thread is done)...
    for thread in thread_list:
        thread.join()


def get_chunks(list_to_chunk, items_per_chunk):
    """Chunks a list into parts.

    :param list_to_chunk:
    :param items_per_chunk:
    :return:
    """

    # Declare some empty lists
    chunk = []
    chunks = []

    # Step through the data n elements at a time
    for x in range(0, len(list_to_chunk), items_per_chunk):
        # Extract n elements
        chunk = list_to_chunk[x:x + items_per_chunk]
        # Add them to list
        chunks.append(chunk)

    # Return the new list
    return chunks


if __name__ == "__main__":
    sys.exit(main())
