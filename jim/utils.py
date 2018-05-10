import json



def dict_to_bytes(dictionary):
    if isinstance(dictionary, dict):
        jmessage = json.dumps(dictionary)
        emessage = jmessage.encode('ascii')
    else:
        raise TypeError
    return emessage


def bytes_to_dict(emessage):
    if isinstance(emessage, bytes):
        message = emessage.decode('ascii')
        jmessage = json.loads(message)
    else:
        raise TypeError
    return jmessage


def send_message(sock, message):
    request = dict_to_bytes(message)
    sock.send(request)


def get_message(client):
    eresponse = client.recv(40960000)
    response = bytes_to_dict(eresponse)
    return response