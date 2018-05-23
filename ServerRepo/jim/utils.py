import json


# def decrypt_msg(text):
#     print(text)
#     privateKeyPath = path.join('ServerRepo', 'security', 'id_rsa')
#     privateKey = load_key(privateKeyPath)
#     print(privateKey.exportKey())
#     decrText = decrypt(text, privateKey)
#     return decrText
#
#
# def encrypt_msg(text):
#     publicKeyPath = path.join('ServerRepo', 'security', 'id_rsa-client.pub')
#     publicKey = load_key(publicKeyPath)
#     encrText = encrypt(text, publicKey)
#     return encrText


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