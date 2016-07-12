import json
import requests
import sys

from RabbitHole.rabbitmq_message_helper import RabbitMQMessageHelper


class RabbitMQ(object):
    """Replays messages in a queue.
    """

    def __init__(self, configuration, console, logger):
        self._configuration = configuration
        self._console = console
        self._logger = logger
        self._rabbitmq_message_helper = RabbitMQMessageHelper(configuration, console, logger)

    # Define the headers to strip out before replaying a message...
    NSERVICEBUS_RUNTIME_HEADERS = [
        'NServiceBus.FLRetries',
        'NServiceBus.Retries']
    NSERVICEBUS_DIAGNOSTIC_HEADERS = [
        '$.diagnostics.originating.hostid',
        '$.diagnostics.hostdisplayname',
        '$.diagnostics.hostid',
        '$.diagnostics.license.expired']
    NSERVICEBUS_AUDIT_HEADERS = [
        'NServiceBus.Version',
        'NServiceBus.TimeSent',
        'NServiceBus.EnclosedMessageTypes',
        'NServiceBus.ProcessingStarted',
        'NServiceBus.ProcessingEnded',
        'NServiceBus.OriginatingAddress',
        'NServiceBus.ProcessingEndpoint',
        'NServiceBus.ProcessingMachine']
    NSERVICEBUS_ERROR_HEADERS = ['NServiceBus.FailedQ']

    def build_rabbit_get_url(self, rabbit_host_url, rabbit_host_port, rabbit_vhost, message_source_queue):
        """Builds the RabbitMQ GET URL.

        :param rabbit_host_url: The RabbitMQ host URL.
        :param rabbit_host_port: The RabbitMQ host port.
        :param rabbit_vhost: The RabbitMQ vhost.
        :param message_source_queue: The name of the RabbitMQ source queue.
        :return: A fully-constructed GET URL for RabbitMQ.
        """

        url = rabbit_host_url + ':' + str(
            rabbit_host_port) + '/api/queues/' + rabbit_vhost + '/' + message_source_queue + '/get'

        return url

    def build_rabbit_publish_url(self, rabbit_host_url, rabbit_host_port, rabbit_vhost, rabbit_destination_queue):
        """Builds the RabbitMQ publish URL.

        :param rabbit_host_url: The RabbitMQ host URL.
        :param rabbit_host_port: The RabbitMQ host port.
        :param rabbit_vhost: The RabbitMQ vhost.
        :param rabbit_destination_queue: The name of the RabbitMQ source queue.
        :return: A fully-constructed publish URL for RabbitMQ.
        """

        url = rabbit_host_url + ':' + str(
            rabbit_host_port) + '/api/exchanges/' + rabbit_vhost + '/' + rabbit_destination_queue + '/publish'

        return url

    def get_rabbit_messages_from_queue(self,
                                       message_count,
                                       rabbit_host_url,
                                       rabbit_host_port,
                                       rabbit_vhost,
                                       message_source_queue,
                                       rabbit_authorization_string,
                                       requeue=True,
                                       verbose=False):
        """Gets messages from a RabbitMQ queue.

        :param message_count: The number of messages to get.
        :param rabbit_host_url: The RabbitMQ host URL.
        :param rabbit_host_port: The RabbitMQ host port.
        :param rabbit_vhost: The RabbitMQ vhost.
        :param message_source_queue: The name of the RabbitMQ source queue.
        :param rabbit_authorization_string: The authorization string for the request header.
        :param requeue: If True, re-queues the message after getting it from the queue.
        :param verbose: If True, enable verbose output.
        :return: A list of the requested messages.
        """

        self._console.write_update('Getting messages from {0}...'.format(message_source_queue))

        rabbit_url = self.build_rabbit_get_url(rabbit_host_url, rabbit_host_port, rabbit_vhost, message_source_queue)

        if requeue:
            rabbit_request_data = {'count': message_count, 'requeue': 'true', 'encoding': 'auto'}
        else:
            rabbit_request_data = {'count': message_count, 'requeue': 'false', 'encoding': 'auto'}
        rabbit_request_json = json.dumps(rabbit_request_data)
        rabbit_request_headers = {'Content-type': 'application/json', 'Authorization': rabbit_authorization_string}

        rabbit_response = requests.post(rabbit_url, data=rabbit_request_json, headers=rabbit_request_headers)

        if rabbit_response.status_code != 200:
            self._console.write_error('[{0}]{1}'.format(rabbit_response.status_code, rabbit_response.text))
            sys.exit(1)

        return rabbit_response.json()

    def publish_messages(self,
                         messages,
                         rabbit_host_url,
                         rabbit_host_port,
                         rabbit_vhost,
                         rabbit_authorization_string,
                         destination_queue=None,
                         simulate=False,
                         verbose=False):
        """Publishes (or re-publishes) messages to RabbitMQ.

        :param messages: A list of the messages to publish.
        :param rabbit_host_url: The RabbitMQ host URL.
        :param rabbit_host_port: The RabbitMQ host port.
        :param rabbit_vhost: The RabbitMQ vhost.
        :param rabbit_authorization_string: The authorization string for the request header.
        :param destination_queue: The queue to publish to (if None, the messages will be re-published).
        :param simulate: If True, simulates the action.
        :param verbose: If True, enable verbose output.
        :return: The number of messages published.
        """

        if not messages:
            self._console.write_update('No messages to process!')
            return

        rabbit_request_headers = {'Content-type': 'application/json', 'Authorization': rabbit_authorization_string}

        processed_messages = 0

        for message in messages:

            processed_messages += 1

            if not destination_queue:
                destination_queue = msg.get_source_queue(message)

            self._console.write_update(
                '{0} of {1} - Publishing message to {2}'.format(processed_messages, len(messages), destination_queue))

            message = self._rabbitmq_message_helper.scrub_message(message, self.NSERVICEBUS_RUNTIME_HEADERS)
            message = self._rabbitmq_message_helper.scrub_message(message, self.NSERVICEBUS_DIAGNOSTIC_HEADERS)
            message = self._rabbitmq_message_helper.scrub_message(message, self.NSERVICEBUS_AUDIT_HEADERS)
            message = self._rabbitmq_message_helper.scrub_message(message, self.NSERVICEBUS_ERROR_HEADERS)

            rabbit_url = self.build_rabbit_publish_url(rabbit_host_url, rabbit_host_port, rabbit_vhost, destination_queue)

            json_message = json.dumps(message)

            self._console.write_update('The RabbitMQ URL is {0}'.format(rabbit_url))

            if simulate:
                self._console.write_simulated_update('[200] Success!')
            else:
                rabbit_response = requests.post(rabbit_url, data=json_message, headers=rabbit_request_headers)

                if rabbit_response.status_code != 200:
                    self._console.write_update('The RabbitMQ response was {0}'.format(rabbit_response.status_code))
                    self._console.write_error('[{0}]{1}'.format(rabbit_response.status_code, rabbit_response.text))
                    sys.exit(1)
                else:
                    self._console.write_update('[{0}] Success!'.format(rabbit_response.status_code))

        return processed_messages

    def is_json(self, message):
        try:
            json_object = json.loads(message)
        except ValueError, e:
            return False
        return True
