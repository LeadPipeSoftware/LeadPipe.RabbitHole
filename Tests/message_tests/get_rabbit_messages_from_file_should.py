"""Unit tests for the get_rabbit_messages_from_file function."""

import json

import os
import pytest
from RabbitHole.rabbitmq_message_helper import get_rabbit_messages_from_file


def test_throw_exception_given_file_not_found():
    with pytest.raises(IOError):
        bad_file_name = 'blarg.json'
        get_rabbit_messages_from_file(bad_file_name)


def test_load_valid_json_from_file():
    test_file_name = 'testfile.json'
    test_data = {'ValueA': 1629,  'ValueB': 1675, 'ValueC': 2042}
    with open(test_file_name, "w") as outfile:
        json.dump(test_data, outfile, indent=4)
    result = get_rabbit_messages_from_file(test_file_name)
    os.remove(test_file_name)
    assert result[0] == test_data
