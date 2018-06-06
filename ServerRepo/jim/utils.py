import json
from ServerRepo.security.encryption import decrypt, load_key, encrypt

def dict_to_str(dictionary):
    if isinstance(dictionary, dict):
        jmessage = json.dumps(dictionary)
    else:
        raise TypeError
    return jmessage


def str_to_dict(message):
    if isinstance(message, str):
        jmessage = json.loads(message)
    else:
        raise TypeError
    return jmessage


def send_message(sock, message, publicKey):
    request = dict_to_str(message)
    encrRequest = encrypt(request, publicKey)
    sock.send(encrRequest)


def get_message(client, privateKey):
    eresponse = client.recv(40960000)
    response = decrypt(eresponse, privateKey)
    toDict = str_to_dict(response)
    return toDict