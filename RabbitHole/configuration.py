import base64
import ConfigParser

import sys


class Configuration(object):
    """This class represents the application configuration.
    """

    def __init__(self, logger, command_line_arguments):
        self._logger = logger
        self._command_line_arguments = command_line_arguments

        self._rabbit_host_url = None
        self._rabbit_host_port = None
        self._rabbit_username = None
        self._rabbit_password = None
        self._rabbit_vhost = None
        self._simulate = None
        self._verbose = None
        self._max_threads = None

        self._config_file = None
        self._ignore_config_file = False

        try:
            self._config_file = ConfigParser.ConfigParser()
            self._config_file.read('.rabbitholeconfig')
            self._logger.info('A .rabbitholeconfig file was found and will be used.')
        except:
            self._logger.info("An error occurred reading the .rabbitholeconfig file: ", sys.exc_info()[0])
            self._ignore_config_file = True

    @property
    def command_line_arguments(self):
        return self._command_line_arguments

    @property
    def enable_logging(self):
        if self._enable_logging is None:

            config_file_value = None
            if self._ignore_config_file is False:
                if self._config_file.has_option('General', 'EnableLogging'):
                    config_file_value = self._config_file.getboolean('General', 'EnableLogging')

            if hasattr(self.command_line_arguments,
                       'enable_logging') and self.command_line_arguments.enable_logging is not None:
                self.enable_logging = self.command_line_arguments.enable_logging
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

            config_file_value = None
            if self._ignore_config_file is False:
                if self._config_file.has_option('RabbitMQ', 'HostUrl'):
                    config_file_value = self._config_file.get('RabbitMQ', 'HostUrl')

            if hasattr(self.command_line_arguments,
                       'rabbit_host_url') and self.command_line_arguments.rabbit_host_url is not None:
                self.rabbit_host_url = self.command_line_arguments.rabbit_host_url
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

            config_file_value = None
            if self._ignore_config_file is False:
                if self._config_file.has_option('RabbitMQ', 'HostPort'):
                    config_file_value = self._config_file.getint('RabbitMQ', 'HostPort')

            if hasattr(self.command_line_arguments,
                       'rabbit_host_port') and self.command_line_arguments.rabbit_host_port is not None:
                self.rabbit_host_port = self.command_line_arguments.rabbit_host_port
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

            config_file_value = None
            if self._ignore_config_file is False:
                self._logger.info('Config file is being used.')
                if self._config_file.has_option('RabbitMQ', 'Username'):
                    config_file_value = self._config_file.get('RabbitMQ', 'Username')

            if hasattr(self.command_line_arguments,
                       'rabbit_username') and self.command_line_arguments.rabbit_username is not None:
                self.rabbit_username = self.command_line_arguments.rabbit_username
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

            config_file_value = None
            if self._ignore_config_file is False:
                if self._config_file.has_option('RabbitMQ', 'Password'):
                    config_file_value = self._config_file.get('RabbitMQ', 'Password')

            if hasattr(self.command_line_arguments,
                       'rabbit_password') and self.command_line_arguments.rabbit_password is not None:
                self.rabbit_password = self.command_line_arguments.rabbit_password
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
        self._logger.info('User: {0}, Pass: {1}'.format(self.rabbit_username, self.rabbit_password))
        encoded_value = base64.encodestring('%s:%s' % (self.rabbit_username, self.rabbit_password)).replace('\n', '')
        return 'Basic {0}'.format(encoded_value)

    @property
    def rabbit_vhost(self):
        if self._rabbit_vhost is None:

            config_file_value = None
            if self._ignore_config_file is False:
                if self._config_file.has_option('RabbitMQ', 'VHost'):
                    config_file_value = self._config_file.get('RabbitMQ', 'VHost')

            if hasattr(self.command_line_arguments,
                       'rabbit_vhost') and self.command_line_arguments.rabbit_vhost is not None:
                self.rabbit_vhost = self.command_line_arguments.rabbit_vhost
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

            config_file_value = None
            if self._ignore_config_file is False:
                if self._config_file.has_option('General', 'Simulate'):
                    config_file_value = self._config_file.getboolean('General', 'Simulate')

            if hasattr(self.command_line_arguments, 'simulate') and self.command_line_arguments.simulate is not None:
                self.simulate = self.command_line_arguments.simulate
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

            config_file_value = None
            if self._ignore_config_file is False:
                if self._config_file.has_option('General', 'Verbose'):
                    config_file_value = self._config_file.getboolean('General', 'Verbose')

            if hasattr(self.command_line_arguments, 'verbose') and self.command_line_arguments.verbose is not None:
                self.verbose = self.command_line_arguments.verbose
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

            config_file_value = None
            if self._ignore_config_file is False:
                if self._config_file.has_option('General', 'max_threads'):
                    config_file_value = self._config_file.getint('General', 'MaxThreads')

            if hasattr(self.command_line_arguments,
                       'max_threads') and self.command_line_arguments.max_threads is not None:
                self.max_threads = self.command_line_arguments.max_threads
            elif config_file_value is not None:
                self.max_threads = config_file_value
            else:
                self.max_threads = 1

        return self._max_threads

    @max_threads.setter
    def max_threads(self, value):
        self._max_threads = value
