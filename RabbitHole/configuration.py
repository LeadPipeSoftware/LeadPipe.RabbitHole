import argparse
import base64
import ConfigParser
import logging

import sys


class Configuration(object):
    """This class represents the application configuration.
    """

    def __init__(self, logger):
        self._logger = logger

        self._command_line_args = None

        self._rabbit_host_url = None
        self._rabbit_host_port = None
        self._rabbit_username = None
        self._rabbit_password = None
        self._rabbit_vhost = None
        self._simulate = None
        self._verbose = None
        self._max_threads = None

        try:
            self._config_file = ConfigParser.ConfigParser()
            self._ignore_config_file = False
            self._logger.info('A configuration file was found and will be used.')
        except:
            self._logger.warn('No configuration file was found. No problem, but thought you might want to know.')
            self._logger.warn("Configuration error: ", sys.exc_info()[0])
            self._ignore_config_file = True

    @property
    def command_line_args(self):
        if self._command_line_args is None:
            self._command_line_args = self._parse_command_line_arguments()  # Overwrite with the command line
        return self._command_line_args

    @property
    def enable_logging(self):
        if self._enable_logging is None:

            if self._ignore_config_file is False:
                if self._config_file.has_option('General', 'EnableLogging'):
                    config_file_value = self._config_file.getboolean('General', 'EnableLogging')

            if self.command_line_args.enable_logging is not None:
                self.enable_logging = self.command_line_args.enable_logging
            elif config_file_value is not None:
                self.enable_logging = config_file_value
            else:
                self.enable_logging = False

        return self._enable_logging

    @enable_logging.setter
    def enable_logging(self, value):
        self._enable_logging = value

    @property
    def rabbit_host_url(self):
        if self._rabbit_host_url is None:

            if self._ignore_config_file is False:
                if self._config_file.has_option('RabbitMQ', 'HostUrl'):
                    config_file_value = self._config_file.get('RabbitMQ', 'HostUrl')

            if self.command_line_args.rabbit_host_url is not None:
                self.rabbit_host_url = self.command_line_args.rabbit_host_url
            elif config_file_value is not None:
                self.rabbit_host_url = config_file_value
            else:
                self.rabbit_host_url = 'http://localhost'

        return self._rabbit_host_url

    @rabbit_host_url.setter
    def rabbit_host_url(self, value):
        self._rabbit_host_url = value

    @property
    def rabbit_host_port(self):
        if self._rabbit_host_port is None:

            if self._ignore_config_file is False:
                if self._config_file.has_option('RabbitMQ', 'HostPort'):
                    config_file_value = self._config_file.getint('RabbitMQ', 'HostPort')

            if self.command_line_args.rabbit_host_port is not None:
                self.rabbit_host_port = self.command_line_args.rabbit_host_port
            elif config_file_value is not None:
                self.rabbit_host_port = config_file_value
            else:
                self.rabbit_host_port = 15672

        return self._rabbit_host_port

    @rabbit_host_port.setter
    def rabbit_host_port(self, value):
        self._rabbit_host_port = value

    @property
    def rabbit_username(self):
        if self._rabbit_username is None:

            if self._ignore_config_file is False:
                if self._config_file.has_option('RabbitMQ', 'Username'):
                    config_file_value = self._config_file.get('RabbitMQ', 'Username')

            if self.command_line_args.rabbit_username is not None:
                self.rabbit_username = self.command_line_args.rabbit_username
            elif config_file_value is not None:
                self.rabbit_username = config_file_value
            else:
                self.rabbit_username = 'guest'

        return self._rabbit_username

    @rabbit_username.setter
    def rabbit_username(self, value):
        self._rabbit_username = value

    @property
    def rabbit_password(self):
        if self._rabbit_password is None:

            if self._ignore_config_file is False:
                if self._config_file.has_option('RabbitMQ', 'Password'):
                    config_file_value = self._config_file.get('RabbitMQ', 'Password')

            if self.command_line_args.rabbit_password is not None:
                self.rabbit_password = self.command_line_args.rabbit_password
            elif config_file_value is not None:
                self.rabbit_password = config_file_value
            else:
                self.rabbit_password = 'guest'

        return self._rabbit_password

    @rabbit_password.setter
    def rabbit_password(self, value):
        self._rabbit_password = value

    @property
    def rabbit_authorization_string(self):
        return base64.encodestring('%s:%s' % (self.rabbit_username, self.rabbit_password)).replace('\n', '')

    @property
    def rabbit_vhost(self):
        if self._rabbit_vhost is None:

            if self._ignore_config_file is False:
                if self._config_file.has_option('RabbitMQ', 'VHost'):
                    config_file_value = self._config_file.get('RabbitMQ', 'VHost')

            if self.command_line_args.rabbit_vhost is not None:
                self.rabbit_vhost = self.command_line_args.rabbit_vhost
            elif config_file_value is not None:
                self.rabbit_vhost = config_file_value
            else:
                self.rabbit_vhost = '%2F'  # The base64 encoding of a forward slash

        return self._rabbit_vhost

    @rabbit_vhost.setter
    def rabbit_vhost(self, value):
        self._rabbit_vhost = value

    @property
    def simulate(self):
        if self._simulate is None:

            if self._ignore_config_file is False:
                if self._config_file.has_option('General', 'Simulate'):
                    config_file_value = self._config_file.getboolean('General', 'Simulate')

            if self.command_line_args.simulate is not None:
                self.simulate = self.command_line_args.simulate
            elif config_file_value is not None:
                self.simulate = config_file_value
            else:
                self.simulate = False

        return self._simulate

    @simulate.setter
    def simulate(self, value):
        self._simulate = value

    @property
    def verbose(self):
        if self._verbose is None:

            if self._ignore_config_file is False:
                if self._config_file.has_option('General', 'Verbose'):
                    config_file_value = self._config_file.getboolean('General', 'Verbose')

            if self.command_line_args.verbose is not None:
                self.verbose = self.command_line_args.verbose
            elif config_file_value is not None:
                self.verbose = config_file_value
            else:
                self.verbose = False

        return self._verbose

    @verbose.setter
    def verbose(self, value):
        self._verbose = value

    @property
    def max_threads(self):
        if self._max_threads is None:

            if self._ignore_config_file is False:
                if self._config_file.has_option('General', 'max_threads'):
                    config_file_value = self._config_file.getint('General', 'MaxThreads')

            if self.command_line_args.max_threads is not None:
                self.max_threads = self.command_line_args.max_threads
            elif config_file_value is not None:
                self.max_threads = config_file_value
            else:
                self.max_threads = 1

        return self._max_threads

    @max_threads.setter
    def max_threads(self, value):
        self._max_threads = value

    def _parse_command_line_arguments(self):
        """Parses the command line arguments.

        :return: The parsed command line arguments.
        """

        parser = argparse.ArgumentParser(add_help=True, description='A RabbitMQ message utility.', version='1.0')

        # Common arguments
        parser.add_argument('-r', '--rabbit_host_url', help='the RabbitMQ host URL')
        parser.add_argument('-p', '--rabbit_port', type=int, help='the RabbitMQ port')
        parser.add_argument('-s', '--rabbit_vhost', help='the RabbitMQ vhost name')
        parser.add_argument('-z', '--rabbit_authorization_string',
                            help='the authorization string for the RabbitMQ request header')
        parser.add_argument('--simulate', action='store_true')
        parser.add_argument('--verbose', action='store_true')
        parser.add_argument('--max_threads', type=int, help='the maximum number of threads to use')

        subparsers = parser.add_subparsers(help='commands', dest='command')

        # Snag command
        snag_parser = subparsers.add_parser('snag',
                                            help='Snags messages from a queue and saves them to a JSON-formatted file')

        snag_parser.add_argument('-q', '--message_source_queue', required=True,
                                 help='The name of the RabbitMQ source queue to get the messages from')
        snag_parser.add_argument('-m', '--message_count', required=True, help='The number of messages to requeue')
        snag_parser.add_argument('-a', '--save_file', required=True,
                                 help='the file to save the JSON message to - PREVENTS RE-QUEUEING')

        # Replay command
        replay_parser = subparsers.add_parser('replay', help='Replays messages in a queue')

        replay_parser.add_argument('-q', '--message_source_queue', required=True,
                                   help='The name of the RabbitMQ source queue to get the messages from')
        replay_parser.add_argument('-m', '--message_count', required=True, help='The number of messages to requeue')
        replay_parser.add_argument('-d', '--rabbit_destination_queue', required=True,
                                   help='The name of the RabbitMQ destination queue')

        # Queue command
        queue_parser = subparsers.add_parser('queue', help='Sends messages to a queue from a JSON-formatted file')

        queue_parser.add_argument('-d', '--rabbit_destination_queue', required=True,
                                  help='The name of the RabbitMQ destination queue')
        queue_parser.add_argument('-f', '--message_source_file', required=True,
                                  help='the message source file or folder')

        # Parse the arguments
        # argparse does a sys.exit when the user does something like ask for help (-h) and since we don't consider
        # that an exception, we're swallowing it so the global error handler doesn't catch it.
        try:
            return parser.parse_args()
        except SystemExit:
            return None
