"""Functions related to RabbitMQ."""

import json
import requests
import sys

import message as msg

# Define the headers to strip out before replaying a message...
nservicebus_runtime_headers = ['NServiceBus.FLRetries', 'NServiceBus.Retries']
nservicebus_diagnostic_headers = ['$.diagnostics.originating.hostid', '$.diagnostics.hostdisplayname',
                                  '$.diagnostics.hostid', '$.diagnostics.license.expired']
nservicebus_audit_headers = ['NServiceBus.Version', 'NServiceBus.TimeSent', 'NServiceBus.EnclosedMessageTypes',
                             'NServiceBus.ProcessingStarted', 'NServiceBus.ProcessingEnded',
                             'NServiceBus.OriginatingAddress', 'NServiceBus.ProcessingEndpoint',
                             'NServiceBus.ProcessingMachine']
nservicebus_error_headers = ['NServiceBus.FailedQ']


def build_rabbit_get_url(rabbit_host_url, rabbit_port, rabbit_vhost, message_source_queue):
    """Builds the RabbitMQ GET URL.

    :param rabbit_host_url: The RabbitMQ host URL.
    :param rabbit_port: The RabbitMQ host port.
    :param rabbit_vhost: The RabbitMQ vhost.
    :param message_source_queue: The name of the RabbitMQ source queue.
    :return: A fully-constructed GET URL for RabbitMQ.
    """

    url = rabbit_host_url + ':' + str(rabbit_port) + '/api/queues/' + rabbit_vhost + '/' + message_source_queue + '/get'

    return url


def build_rabbit_publish_url(rabbit_host_url, rabbit_port, rabbit_vhost, rabbit_destination_queue):
    """Builds the RabbitMQ publish URL.

    :param rabbit_host_url: The RabbitMQ host URL.
    :param rabbit_port: The RabbitMQ host port.
    :param rabbit_vhost: The RabbitMQ vhost.
    :param rabbit_destination_queue: The name of the RabbitMQ source queue.
    :return: A fully-constructed publish URL for RabbitMQ.
    """

    url = rabbit_host_url + ':' + str(
        rabbit_port) + '/api/exchanges/' + rabbit_vhost + '/' + rabbit_destination_queue + '/publish'

    return url


def get_rabbit_messages_from_queue(message_count, rabbit_host_url, rabbit_port, rabbit_vhost, message_source_queue,
                                   rabbit_authorization_string, verbose=False):
    """Gets messages from a RabbitMQ queue.

    :param message_count: The number of messages to get.
    :param rabbit_host_url: The RabbitMQ host URL.
    :param rabbit_port: The RabbitMQ host port.
    :param rabbit_vhost: The RabbitMQ vhost.
    :param message_source_queue: The name of the RabbitMQ source queue.
    :param rabbit_authorization_string: The authorization string for the request header.
    :param verbose: If True, prints verbose messages.
    :return: A list of the requested messages.
    """

    print '\033[0;32;40m+ \033[0m Getting messages from {0}...'.format(message_source_queue)

    rabbit_url = build_rabbit_get_url(rabbit_host_url, rabbit_port, rabbit_vhost, message_source_queue)
    rabbit_request_data = {'count': message_count, 'requeue': 'false', 'encoding': 'auto'}
    rabbit_request_json = json.dumps(rabbit_request_data)
    rabbit_request_headers = {'Content-type': 'application/json', 'Authorization': rabbit_authorization_string}

    rabbit_response = requests.post(rabbit_url, data=rabbit_request_json, headers=rabbit_request_headers)

    if rabbit_response.status_code != 200:
        print '\033[1;31;40m+ ERROR: \033[0m[{0}]{1}'.format(rabbit_response.status_code, rabbit_response.text)
        sys.exit(1)

    return rabbit_response.json()


def publish_messages(messages, rabbit_host_url, rabbit_port, rabbit_vhost, rabbit_authorization_string,
                     destination_queue=None, verbose=False, simulate=False):
    """Publishes (or re-publishes) messages to RabbitMQ.

    :param messages: A list of the messages to publish.
    :param rabbit_host_url: The RabbitMQ host URL.
    :param rabbit_port: The RabbitMQ host port.
    :param rabbit_vhost: The RabbitMQ vhost.
    :param rabbit_authorization_string: The authorization string for the request header.
    :param destination_queue: The queue to publish to (if None, the messages will be re-published).
    :param verbose: If True, prints verbose messages.
    :param simulate: If True, simulates the action.
    :return: The number of messages published.
    """

    if not messages:
        print '\033[0;32;40m+ \033[0m No messages to process!'
        return

    rabbit_request_headers = {'Content-type': 'application/json', 'Authorization': rabbit_authorization_string}

    if verbose:
        print '\033[0;32;40m+ \033[0mThe headers are {0}'.format(rabbit_request_headers)

    processed_messages = 0

    for message in messages:

        processed_messages += 1

        if destination_queue is None:
            destination_queue = msg.get_source_queue(message)

        print '\033[0;32;40m+ \033[0m{0} of {1} - Requeueing message to {2}'.format(processed_messages, len(messages),
                                                                                    destination_queue)

        message = msg.scrub_message(message, nservicebus_runtime_headers)
        message = msg.scrub_message(message, nservicebus_diagnostic_headers)
        message = msg.scrub_message(message, nservicebus_audit_headers)
        message = msg.scrub_message(message, nservicebus_error_headers)

        rabbit_url = build_rabbit_publish_url(rabbit_host_url, rabbit_port, rabbit_vhost, destination_queue)

        json_message = json.dumps(message)

        if verbose:
            print '\033[0;32;40m+ \033[0mThe RabbitMQ URL is {0}'.format(rabbit_url)

        if simulate:
            print '\033[0;32;40m+ \033[0;35;40m[200] Success!\033[0m'
        else:
            rabbit_response = requests.post(rabbit_url, data=json_message, headers=rabbit_request_headers)

            if rabbit_response.status_code != 200:
                print '\033[0;32;40m+ \033[0mThe RabbitMQ response was {0}'.format(rabbit_response.status_code)
                print '\033[1;31;40m+ ERROR: \033[0m[{0}]{1}'.format(rabbit_response.status_code, rabbit_response.text)
                sys.exit(1)
            else:
                print '\033[0;32;40m+ \033[0m[{0}] Success!'.format(rabbit_response.status_code)

    return processed_messages
