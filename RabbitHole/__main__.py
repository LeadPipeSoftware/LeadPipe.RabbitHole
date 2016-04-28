"""RabbitHole: RabbitHole is a RabbitMQ message utility."""

from __future__ import print_function

import argparse
import os
from Queue import Queue
import sys
import threading
from timeit import default_timer as timer

import RabbitHole.message as msg
import RabbitHole.rabbitmq as rabbit

print = lambda x: sys.stdout.write("%s\n" % x)

PROGRAM_NAME = 'RabbitHole'
PROGRAM_VERSION = '1.0.0'

AUTHORIZATION_STRING_GUEST = 'Basic Z3Vlc3Q6Z3Vlc3Q='  # guest/guest
AUTHORIZATION_STRING_RABBIT = 'Basic cmFiYml0OnJhYmJpdA=='  # rabbit/rabbit

DEFAULT_MAX_THREADS = 512
DEFAULT_RABBITMQ_HOST_URL = 'http://localhost'
DEFAULT_RABBITMQ_PORT = 15672
DEFAULT_RABBITMQ_VHOST = '%2F'


def main(args=None):
    """The program entry point."""

    global PARSED_ARGS
    PARSED_ARGS = parse_command_line_arguments()

    display_welcome()

    start = timer()

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

    end = timer()
    print('\033[0;32;40m+ \033[0mDone in {0}!\033[0m\n'.format(end - start))  # Make sure we didn't jack with the user's terminal colors
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
    parser.add_argument('--max_threads', default=DEFAULT_MAX_THREADS, help='the maximum number of threads to use')

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
    queue_parser.add_argument('-f', '--message_source_file', required=True, help='the message source file or folder')

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


def queue_file_on_thread(thread_queue):
    """Sends messages to a queue from a JSON-formatted file.

    :return:
    """

    # Yes, we're putting ourselves in an infinite loop. This should be executed by a daemon thread which will only then
    # exit when the main thread ends.
    while True:
        message_source_file = thread_queue.get()

        messages = msg.get_rabbit_messages_from_file(message_source_file, PARSED_ARGS.verbose)

        rabbit.publish_messages(messages,
                                PARSED_ARGS.rabbit_host_url,
                                PARSED_ARGS.rabbit_port,
                                PARSED_ARGS.rabbit_vhost,
                                PARSED_ARGS.rabbit_authorization_string,
                                PARSED_ARGS.rabbit_destination_queue,
                                True,
                                PARSED_ARGS.simulate)

        thread_queue.task_done()


def queue_folder():
    """Sends messages to a queue from all JSON-formatted files in a folder.

        :return:
        """

    global THREAD_QUEUE

    THREAD_QUEUE = Queue(maxsize=0)

    number_of_threads = PARSED_ARGS.max_threads

    message_files = msg.get_rabbit_message_files_in_folder(PARSED_ARGS.message_source_file)

    for message_file in message_files:
        THREAD_QUEUE.put(message_file)

    print('\033[0;36;40m    Source Folder:\033[0m \033[0;37;40m{0}\033[0m'.format(PARSED_ARGS.message_source_file))
    print('\033[0;36;40mDestination Queue:\033[0m \033[0;37;40m{0}\033[0m'.format(PARSED_ARGS.rabbit_destination_queue))
    print('\033[0;36;40m       File Count:\033[0m \033[0;37;40m{0}\033[0m'.format(len(message_files)))
    print('\033[0;36;40m       Queue Size:\033[0m \033[0;37;40m{0}\033[0m'.format(THREAD_QUEUE.qsize()))
    print('\033[0;36;40m Max Thread Count:\033[0m \033[0;37;40m{0}\033[0m'.format(number_of_threads))
    print('-' * 80)

    thread_list = []

    # Build the threads
    for i in range(number_of_threads):
        worker = threading.Thread(target=queue_file_on_thread, args=(THREAD_QUEUE,))
        worker.setDaemon(True)
        thread_list.append(worker)

    # Start the threads
    for i in thread_list:
        i.start()

    # Wait for the queue to be empty
    THREAD_QUEUE.join()


def get_chunks(list_to_chunk, items_per_chunk):
    """Chunks a list into parts.

    :param list_to_chunk:
    :param items_per_chunk:
    :return:
    """

    chunks = []

    for x in range(0, len(list_to_chunk), items_per_chunk):
        chunk = list_to_chunk[x:x + items_per_chunk]
        chunks.append(chunk)

    return chunks


if __name__ == "__main__":
    sys.exit(main())
