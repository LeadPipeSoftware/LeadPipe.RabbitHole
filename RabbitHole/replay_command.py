import RabbitHole.rabbitmq as rabbit


class ReplayCommand(object):
    """Replays messages in a queue.
    """

    def __init__(self, configuration, console, logger):
        self._configuration = configuration
        self._console = console
        self._logger = logger

    def execute(self):
        """Executes the command.

        :return:
        """

        if self._configuration.verbose:
            self._console.write_keyvaluepair('    Message Count',
                                             self._configuration.command_line_args.message_count)
            self._console.write_keyvaluepair('     Source Queue',
                                             self._configuration.command_line_args.message_source_queue)
            self._console.write_keyvaluepair('Destination Queue',
                                             self._configuration.command_line_args.rabbit_destination_queue)
            self._console.write_divider()

        messages = rabbit.get_rabbit_messages_from_queue(self._configuration.command_line_args.message_count,
                                                         self._configuration.rabbit_host_url,
                                                         self._configuration.rabbit_host_port,
                                                         self._configuration.rabbit_vhost,
                                                         self._configuration.command_line_args.message_source_queue,
                                                         self._configuration.rabbit_authorization_string,
                                                         True,
                                                         self._configuration.verbose)

        rabbit.publish_messages(messages,
                                self._configuration.rabbit_host_url,
                                self._configuration.rabbit_host_port,
                                self._configuration.rabbit_vhost,
                                self._configuration.rabbit_authorization_string,
                                self._configuration.command_line_args.rabbit_destination_queue,
                                self._configuration.simulate,
                                self._configuration.verbose)
