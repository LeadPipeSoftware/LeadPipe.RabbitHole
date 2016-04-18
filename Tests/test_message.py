
import pytest
from RabbitHole.message import get_rabbit_messages_from_file


def test_throw_exception_given_file_not_found():
    with pytest.raises(IOError):
        bad_file_name = 'blarg.json'
        get_rabbit_messages_from_file(bad_file_name)


# def test_two(self):
#     x = "hello"
#     assert hasattr(x, 'check')
