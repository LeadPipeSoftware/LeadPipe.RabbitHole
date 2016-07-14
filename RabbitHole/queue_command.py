import threading

from Queue import Queue

from RabbitHole.rabbitmq_message_helper import RabbitMQMessageHelper
from RabbitHole.rabbitmq import RabbitMQ


class QueueCommand(object):
    """Sends messages to a queue from a JSON file.
    """

    def __init__(self, configuration, console, logger):
        self._configuration = configuration
        self._console = console
        self._logger = logger
        self._rabbitmq_message_helper = RabbitMQMessageHelper(configuration, console, logger)
        self._rabbitmq = RabbitMQ(configuration, console, logger)

    def queue_file(self):
        """Sends messages to a queue from a JSON-formatted file.

        :return:
        """

        if self._configuration.verbose:
            self._console.write_keyvaluepair('      Source File',
                                             self._configuration.command_line_arguments.message_source_file)
            self._console.write_keyvaluepair('Destination Queue',
                                             self._configuration.command_line_arguments.rabbit_destination_queue)
            self._console.write_divider()

        messages = self._rabbitmq_message_helper.get_rabbit_messages_from_file(
            self._configuration.command_line_arguments.message_source_file,
            self._configuration.simulate,
            self._configuration.verbose)

        self._logger.debug('There were {0} messages in the file'.format(len(messages)))

        self._rabbitmq.publish_messages(messages,
                                        self._configuration.rabbit_host_url,
                                        self._configuration.rabbit_host_port,
                                        self._configuration.rabbit_vhost,
                                        self._configuration.rabbit_authorization_string,
                                        self._configuration.command_line_arguments.rabbit_destination_queue,
                                        self._configuration.simulate,
                                        self._configuration.verbose)

    def queue_folder(self):
        """Sends messages to a queue from all JSON-formatted files in a folder.

            :return:
            """

        global THREAD_QUEUE

        THREAD_QUEUE = Queue(maxsize=0)

        number_of_threads = self._configuration.max_threads

        message_files = self._rabbitmq_message_helper.get_rabbit_message_files_in_folder(
            self._configuration.command_line_arguments.message_source_file)

        for message_file in message_files:
            THREAD_QUEUE.put(message_file)

        self._console.write_keyvaluepair('    Source Folder',
                                         self._configuration.command_line_arguments.message_source_file)
        self._console.write_keyvaluepair('Destination Queue',
                                         self._configuration.command_line_arguments.rabbit_destination_queue)
        self._console.write_keyvaluepair('       File Count',
                                         len(message_files))
        self._console.write_keyvaluepair('       Queue Size',
                                         THREAD_QUEUE.qsize())
        self._console.write_keyvaluepair(' Max Thread Count',
                                         number_of_threads)
        self._console.write_divider()

        thread_list = []

        # Build the threads
        for i in range(number_of_threads):
            worker = threading.Thread(target=self._queue_file_on_thread, args=(THREAD_QUEUE,))
            worker.setDaemon(True)
            thread_list.append(worker)

        self._console.write_update(
            'Publishing {0} message files to {1}'.format(len(message_files),
                                                         self._configuration.command_line_arguments.rabbit_destination_queue))
        self._configuration.silent = True

        # Start the threads
        for i in thread_list:
            i.start()

        # Wait for the queue to be empty
        THREAD_QUEUE.join()

        self._configuration.silent = False

    def _queue_file_on_thread(self, thread_queue):
        """Sends messages to a queue from a JSON-formatted file.

        :return:
        """

        # Yes, we're putting ourselves in an infinite loop. This should be executed by a daemon thread which will only then
        # exit when the main thread ends.
        while True:
            message_source_file = thread_queue.get()

            messages = self._rabbitmq_message_helper.get_rabbit_messages_from_file(message_source_file,
                                                                                   self._configuration.simulate,
                                                                                   self._configuration.verbose)

            self._logger.debug('There were {0} messages in the file'.format(len(messages)))

            self._rabbitmq.publish_messages(messages,
                                            self._configuration.rabbit_host_url,
                                            self._configuration.rabbit_host_port,
                                            self._configuration.rabbit_vhost,
                                            self._configuration.rabbit_authorization_string,
                                            self._configuration.command_line_arguments.rabbit_destination_queue,
                                            self._configuration.simulate,
                                            self._configuration.verbose)

            thread_queue.task_done()

            # def _get_chunks(self, list_to_chunk, items_per_chunk):
            #     """Chunks a list into parts.

            #     :param list_to_chunk:
            #     :param items_per_chunk:
            #     :return:
            #     """

            #     chunks = []

            #     for x in range(0, len(list_to_chunk), items_per_chunk):
            #         chunk = list_to_chunk[x:x + items_per_chunk]
            #         chunks.append(chunk)

            #     return chunks
