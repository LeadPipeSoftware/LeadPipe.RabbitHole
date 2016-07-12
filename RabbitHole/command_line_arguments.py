import argparse


class CommandLineArguments(object):
    """This class represents the command line arguments.
    """

    def __init__(self):
        self._parsed_arguments = self._parse_command_line_arguments()

    @property
    def parsed_arguments(self):
        return self._parsed_arguments

    def _parse_command_line_arguments(self):
        """Parses the command line arguments.

        :return: The parsed command line arguments.
        """

        parser = argparse.ArgumentParser(add_help=True, description='A RabbitMQ message utility.', version='1.0')

        # Common arguments
        parser.add_argument('-r',
                            '--rabbit_host_url',
                            help='the RabbitMQ host URL')
        parser.add_argument('-p',
                            '--rabbit_host_port',
                            type=int,
                            help='the RabbitMQ port')
        parser.add_argument('-s',
                            '--rabbit_vhost',
                            help='the RabbitMQ vhost name')
        parser.add_argument('-z',
                            '--rabbit_authorization_string',
                            help='the authorization string for the RabbitMQ request header')
        parser.add_argument('--simulate',
                            action='store_true')
        parser.add_argument('--verbose',
                            action='store_true')
        parser.add_argument('--silent',
                            action='store_true')
        parser.add_argument('--max_threads',
                            type=int,
                            help='the maximum number of threads to use')
        parser.add_argument('--debug',
                            action='store_true')

        subparsers = parser.add_subparsers(help='commands', dest='command')

        # Snag command
        snag_parser = subparsers.add_parser('snag',
                                            help='Saves a copy of messages in a queue as a JSON file')

        snag_parser.add_argument('-q',
                                 '--message_source_queue',
                                 required=True,
                                 help='The name of the RabbitMQ source queue to get the messages from')
        snag_parser.add_argument('-m',
                                 '--message_count',
                                 required=True,
                                 help='The number of messages to requeue')
        snag_parser.add_argument('-a',
                                 '--save_file',
                                 required=True,
                                 help='the file to save the JSON message to - PREVENTS RE-QUEUEING')

        # Replay command
        replay_parser = subparsers.add_parser('replay', help='Returns messages to their source queue')

        replay_parser.add_argument('-q',
                                   '--message_source_queue',
                                   required=True,
                                   help='The name of the RabbitMQ source queue to get the messages from')
        replay_parser.add_argument('-m',
                                   '--message_count',
                                   required=True,
                                   help='The number of messages to requeue')

        # Queue command
        queue_parser = subparsers.add_parser('queue',
                                             help='Sends messages to a queue from a JSON file')

        queue_parser.add_argument('-d',
                                  '--rabbit_destination_queue',
                                  required=True,
                                  help='The name of the RabbitMQ destination queue')
        queue_parser.add_argument('-f',
                                  '--message_source_file',
                                  required=True,
                                  help='the message source file or folder')

        # Shuttle command
        shuttle_parser = subparsers.add_parser('shuttle',
                                               help='Gets messages from a queue and puts them on another queue')

        shuttle_parser.add_argument('-q',
                                    '--message_source_queue',
                                    required=True,
                                    help='The name of the RabbitMQ source queue to get the messages from')
        shuttle_parser.add_argument('-m',
                                    '--message_count',
                                    required=True,
                                    help='The number of messages to requeue')
        shuttle_parser.add_argument('-d',
                                    '--rabbit_destination_queue',
                                    required=True,
                                    help='The name of the RabbitMQ destination queue')

        # Parse the arguments
        # argparse does a sys.exit when the user does something like ask for help (-h) and since we don't consider
        # that an exception, we're swallowing it so the global error handler doesn't catch it.
        # try:
        #     return parser.parse_args()
        # except SystemExit:
        #     return None
        return parser.parse_args()
