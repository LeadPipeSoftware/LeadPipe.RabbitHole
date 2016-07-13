from __future__ import print_function

import base64
import ConfigParser
import os
import sys

from RabbitHole import __program_name__

print = lambda x: sys.stdout.write("%s\n" % x)


class Configuration(object):
    """This class represents the application configuration.
    """

    def __init__(self, command_line_arguments):
        self._command_line_arguments = command_line_arguments

        self._rabbit_host_url = None
        self._rabbit_host_port = None
        self._rabbit_username = None
        self._rabbit_password = None
        self._rabbit_vhost = None
        self._source_queue_header_key = None
        self._message_headers_to_remove = None
        self._simulate = None
        self._verbose = None
        self._silent = None
        self._max_threads = None

        self._config_file = None
        self._ignore_config_file = True

        try:
            self._config_file = ConfigParser.ConfigParser()

            config_file_name = '.' + __program_name__ + 'config'
            user_config_file_name = os.path.join(os.path.expanduser('~'), config_file_name)

            if os.path.isfile(user_config_file_name):
                self._config_file.read(user_config_file_name)
            elif os.path.isfile(config_file_name):
                self._config_file.read(config_file_name)
            self._ignore_config_file = False
        except ConfigParser.Error, err:
            if not self._silent:
                print('\033[1;31;40m+ ERROR: \033[0mUnable to parse the {0} file. {1}'.format(config_file_name, err))
        except IOError, err:
            if not self._silent:
                print('\033[1;31;40m+ ERROR: \033[0mUnable to open the {0} file. {1}'.format(config_file_name, err))

    @property
    def using_config_file(self):
        return not self._ignore_config_file

    @property
    def command_line_arguments(self):
        return self._command_line_arguments

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
    def source_queue_header_key(self):
        if self._source_queue_header_key is None:

            config_file_value = None
            if self._ignore_config_file is False:
                if self._config_file.has_option('Messages', 'SourceQueueHeaderKey'):
                    config_file_value = self._config_file.get('Messages', 'SourceQueueHeaderKey')

            if hasattr(self.command_line_arguments,
                       'source_queue_header_key') and self.command_line_arguments.source_queue_header_key is not None:
                self.source_queue_header_key = self.command_line_arguments.source_queue_header_key
            elif config_file_value is not None:
                self.source_queue_header_key = config_file_value
            else:
                self.source_queue_header_key = 'NServiceBus.FailedQ'

        return self._source_queue_header_key

    @source_queue_header_key.setter
    def source_queue_header_key(self, value):
        self._source_queue_header_key = value

    @property
    def message_headers_to_remove(self):
        if self._message_headers_to_remove is None:

            # Define the headers to strip out before replaying a message...
            nservicebus_runtime_headers = [
                'NServiceBus.FLRetries',
                'NServiceBus.Retries']
            nservicebus_diagnostic_headers = [
                '$.diagnostics.originating.hostid',
                '$.diagnostics.hostdisplayname',
                '$.diagnostics.hostid',
                '$.diagnostics.license.expired']
            nservicebus_audit_headers = [
                'NServiceBus.Version',
                'NServiceBus.TimeSent',
                'NServiceBus.EnclosedMessageTypes',
                'NServiceBus.ProcessingStarted',
                'NServiceBus.ProcessingEnded',
                'NServiceBus.OriginatingAddress',
                'NServiceBus.ProcessingEndpoint',
                'NServiceBus.ProcessingMachine']
            nservicebus_error_headers = ['NServiceBus.FailedQ']

            config_file_value = None
            if self._ignore_config_file is False:
                if self._config_file.has_option('Messages', 'MessageHeadersToRemove'):
                    config_file_value = self._config_file.get('Messages', 'MessageHeadersToRemove')

            if hasattr(self.command_line_arguments,
                       'message_headers_to_remove') and self.command_line_arguments.message_headers_to_remove is not None:
                self.message_headers_to_remove = self.command_line_arguments.message_headers_to_remove
            elif config_file_value is not None:
                self.message_headers_to_remove = config_file_value.split(',')  # Careful!
            else:
                self.message_headers_to_remove = nservicebus_runtime_headers + nservicebus_diagnostic_headers + nservicebus_audit_headers + nservicebus_error_headers

        return self._message_headers_to_remove

    @message_headers_to_remove.setter
    def message_headers_to_remove(self, value):
        self._message_headers_to_remove = value

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
    def silent(self):
        if self._silent is None:

            config_file_value = None
            if self._ignore_config_file is False:
                if self._config_file.has_option('General', 'Silent'):
                    config_file_value = self._config_file.getboolean('General', 'Silent')

            if hasattr(self.command_line_arguments, 'silent') and self.command_line_arguments.silent is not None:
                self.silent = self.command_line_arguments.silent
            elif config_file_value is not None:
                self.silent = config_file_value
            else:
                self.silent = False

        return self._silent

    @silent.setter
    def silent(self, value):
        self._silent = value

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
