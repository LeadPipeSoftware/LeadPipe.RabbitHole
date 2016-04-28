"""Functions related to RabbitMQ."""

from __future__ import print_function

import json
import sys

import os.path

print = lambda x: sys.stdout.write("%s\n" % x)

def save_rabbit_messages_to_file(messages, save_file, silent=False, simulate=False):
    """Saves RabbitMQ messages to a file in JSON format.

    :param messages: The messages to save.
    :param save_file: The name of the file to save the messages to.
    :param silent: If True, silences output.
    :param simulate: If True, simulates the action.
    :return:
    """

    if simulate:
        if not silent:
            print('\033[0;32;40m+ \033[0;35;40mSaving messages to {0}\033[0m'.format(save_file))
    else:
        if messages:
            with open(save_file, 'w') as file_to_save:
                for message in messages:
                    if not silent:
                        print('\033[0;32;40m+ \033[0mSaving {0} messages to {1}'.format(len(messages), save_file))
                    file_to_save.write(json.dumps(message, indent=2))
        else:
            if not silent:
                print('\033[1;31;40m+ ERROR: \033[0mNo messages found!')


def get_rabbit_messages_from_file(message_file_name, silent=False, simulate=False):
    """Gets messages from a JSON file.

    :param message_file_name: The full path and name of the JSON file containing the message.
    :param silent: If True, silences output.
    :param simulate: If True, simulates the action.
    :return: The message contained in the file.
    """

    if simulate:
        if not silent:
            print('\033[0;32;40m+ \033[0;35;40mGetting messages from {0}\033[0m'.format(message_file_name))
    else:
        if not silent:
            print('\033[0;32;40m+ \033[0mGetting messages from {0}'.format(message_file_name))

        if not os.path.isfile(message_file_name):
            if not silent:
                print('\033[1;31;40m+ ERROR: \033[0m{0} not found!'.format(message_file_name))
            raise IOError()

        try:
            with open(message_file_name) as json_data:
                d = json.load(json_data)
                return [d]
        except:
            return None


def get_rabbit_message_files_in_folder(folder_name):
    """Gets messages from a folder.
    :param folder_name: The name of the folder to search.
    :return: The list of files.
    """

    files = os.listdir(folder_name)

    all_files = []

    for file in files:
        all_files.append(os.path.join(folder_name, file))

    return all_files


def get_source_queue(message):
    """Gets the source queue from a message.

    :param message: The message as a JSON string.
    :return: The name of the source queue.
    """

    source_queue = None

    try:
        source_queue = message['properties']['headers']['NServiceBus.FailedQ']
    except KeyError:
        raise ValueError('The source queue could not be determined!')

    return source_queue.split('@', 1)[0]


def scrub_message(message, elements_to_delete):
    """Scrubs the unnecessary header information out of a RabbitMQ message.

    :param message: The RabbitMQ message in JSON format.
    :param elements_to_delete: A list of keys identifying the elements to delete.
    :return: The scrubbed message.
    """

    # NOTE: This whole function is really nothing more than a generic way to remove keys from a dictionary.

    for element_to_delete in elements_to_delete:

        try:
            del message[element_to_delete]
        except KeyError:
            pass

    for value in message.values():
        if isinstance(value, dict):
            scrub_message(value, elements_to_delete)

    return message
