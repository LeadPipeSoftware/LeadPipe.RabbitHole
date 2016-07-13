from __future__ import print_function


class Console(object):
    """This class represents the console.
    """

    def __init__(self, configuration):
        self._configuration = configuration

    # Foreground    Code    Style       Code    Background  Code
    # ----------------------------------------------------------
    # Black         30      No effect   0       Black       40
    # Red       	31      Bold        1       Red         41
    # Green         32      Underline   4   	Green   	42
    # Yellow	    33	    Blink	    5	    Yellow	    43
    # Blue	        34	    Inverse	    7	    Blue	    44
    # Purple	    35	    Hidden	    8	    Purple	    45
    # Cyan	        36		                    Cyan	    46
    # White	        37                 			White	    47

    def display_welcome(self, program_name, program_version):
        """Displays the program welcome message.

        :param program_name: The name of the program.
        :param program_version: The version of the program.
        """

        if not self._configuration.silent:
            self.write_title(program_name, program_version)

            if self._configuration.verbose:
                self.write_keyvaluepair('  Config File', self._configuration.using_config_file)
                self.write_keyvaluepair('     Host URL', self._configuration.rabbit_host_url)
                self.write_keyvaluepair('         Port', self._configuration.rabbit_host_port)
                self.write_keyvaluepair('        VHost', self._configuration.rabbit_vhost)
                self.write_keyvaluepair('     Username', self._configuration.rabbit_username)
                self.write_keyvaluepair('     Password', self._configuration.rabbit_password)
                self.write_keyvaluepair('  Auth String', self._configuration.rabbit_authorization_string)
                self.write_divider()

            if self._configuration.simulate:
                print('Output in \033[0;35;40mthis color\033[0m indicates a simulated step!')
                self.write_divider()

    def write_divider(self):
        """Writes a divider line to the console.
        """
        if not self._configuration.silent:
            print('-' * 80)

    def write_error(self, message):
        """Writes an error message to the console.

        :param message: The message to write.
        """
        if not self._configuration.silent:
            print('\033[1;31;40m+ ERROR: \033[0m{0}'.format(message))

    def write_keyvaluepair(self, key, value):
        """Writes a key and a value pair message to the console.

        :param key: The key value.
        :param value: The value.
        """
        if not self._configuration.silent:
            print('\033[0;36;40m{0}:\033[0m \033[0;37;40m{1}\033[0m'.format(key, value))

    def write_simulated_update(self, message):
        """Writes an update message to the console when simulating something.

        :param message: The message to write.
        """
        if not self._configuration.silent:
            print('\033[0;32;40m+ \033[0;35;40m{0}\033[0m'.format(message))

    def write_title(self, program_name, program_version):
        """Writes the program title to the console.

        :param program_name: The name of the program.
        :param program_version: The version of the program.
        """
        if not self._configuration.silent:
            print('\033[0;33;40m{0} v{1}\033[0m'.format(program_name, program_version))
            self.write_divider()

    def write_update(self, message):
        """Writes an update message to the console.

        :param message: The message to write.
        """
        if not self._configuration.silent:
            print('\033[0;32;40m+ \033[0m{0}'.format(message))
