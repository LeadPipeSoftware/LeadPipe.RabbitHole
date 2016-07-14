import json
import re
import os.path


class RabbitMQMessageHelper(object):
    """Provides helper functions for RabbitMQ messages.
    """

    def __init__(self, configuration, console, logger):
        self._configuration = configuration
        self._console = console
        self._logger = logger

    def save_rabbit_messages_to_file(self, messages, save_file, simulate=False):
        """Saves RabbitMQ messages to a file in JSON format.

        :param messages: The messages to save.
        :param save_file: The name of the file to save the messages to.
        :param simulate: If True, simulates the action.
        :return:
        """

        if simulate:
            self._console.write_simulated_update('Saving messages to {0}'.format(save_file))
        else:
            if messages:
                with open(save_file, 'w') as file_to_save:
                    if len(messages) > 1:
                        file_to_save.write('[')
                    saved_count = 0
                    for message in messages:
                        self._console.write_update('Saving {0} messages to {1}'.format(len(messages), save_file))
                        file_to_save.write(json.dumps(message, indent=2))
                        saved_count += 1
                        if saved_count < len(messages):
                            file_to_save.write(',\n')
                    if len(messages) > 1:
                        file_to_save.write(']')

            else:
                self._console.write_error('No messages found!')

    def get_rabbit_messages_from_file(self, message_file_name, simulate=False, verbose=False):
        """Gets messages from a JSON file.

        :param message_file_name: The full path and name of the JSON file containing the message.
        :param simulate: If True, simulates the action.
        :param verbose: If True, enable verbose output.
        :return: The message contained in the file.
        """

        if simulate:
            self._console.write_simulated_update('Getting messages from {0}\033[0m'.format(message_file_name))
        else:
            self._console.write_update('Getting messages from {0}'.format(message_file_name))

            if not os.path.isfile(message_file_name):
                self._console.write_error('{0} not found!'.format(message_file_name))
                raise IOError()

            try:
                with open(message_file_name) as json_data:
                    d = json.load(json_data)
                    return [d]
            except:
                return None

    def get_rabbit_message_files_in_folder(self, folder_name):
        """Gets messages from a folder.
        :param folder_name: The name of the folder to search.
        :return: The list of files.
        """

        files = os.listdir(folder_name)

        all_files = []

        for f in files:
            all_files.append(os.path.join(folder_name, f))

        return all_files

    def get_source_queue(self, message):
        """Gets the source queue from a message.

        :param message: The message as a JSON string.
        :return: The name of the source queue.
        """

        source_queue = None

        for source_queue_field in self._configuration.source_queue_fields:

            source_queue_matches = self.get_dictionary_field_values(message, source_queue_field)
            if source_queue_matches and len(source_queue_matches) > 0:
                source_queue = source_queue_matches[0]
                self._logger.debug('Determined the source queue to be {0}'.format(source_queue))
                pass

        return source_queue

    def scrub_message(self, message, elements_to_delete):
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
                self.scrub_message(value, elements_to_delete)

        return message

    def get_dictionary_field_values(self, search_dict, field):
        """Gets a list of dictionary field values from a nested dictionary.

        :param search_dict: The dictionary to search.
        :param field: The field to search for.
        :return: A list of matching field values.
        """

        fields_found = []

        for key, value in search_dict.iteritems():

            if key == field:
                fields_found.append(value)

            elif isinstance(value, dict):
                results = self.get_dictionary_field_values(value, field)
                for result in results:
                    fields_found.append(result)

            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        more_results = self.get_dictionary_field_values(item, field)
                        for another_result in more_results:
                            fields_found.append(another_result)

        return fields_found

    def get_path_from_dictionary(self, dct, path):
        """Gets a nested property from a dictionary

        :param dct: The dictionary to search.
        :param path: The path to search (ex: 'Field1.Field2.Field3').
        """

        try:
            for i, p in re.findall(r'(\d+)|(\w+)', path):
                dct = dct[p or int(i)]
            return dct
        except KeyError:
            return None
