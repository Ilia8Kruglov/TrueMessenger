from jim.utils import *
from socket import *


def test_dict_to_bytes():
    message = {
    'action': 'presence',
    'time': '1519817168.683862',
    }
    actual_result = dict_to_bytes(message)
    expected_result = b'{"action": "presence", "time": "1519817168.683862"}'
    assert actual_result == expected_result


def test_send_message():
    message = {
    'action': 'presence',
    'time': '1519820600.85518',
    }
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(('localhost', 7777))
    actual_result = send_message(client, message)
    client.close()
    expected_result = 50
    assert actual_result == expected_result


def test_get_message():
    request = {
    'action': 'presence',
    'time': 1519820600.85519,
    }

    client = socket(AF_INET, SOCK_STREAM)
    client.connect(('localhost', 7777))
    send_message(client, request)
    actual_result = get_message(client)
    client.close()
    expected_result = {'response': '200 OK'}
    assert actual_result == expected_result

