# http://devarea.com/python-cryptographic-api/#.WwLBGci-m8U

from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import MD5


def generate_keys(key_length):
    random_gen = Random.new().read
    key = RSA.generate(key_length, random_gen)
    publicKey = key.publickey()
    with open('id_rsa', 'w', encoding="utf-8") as privateKeyFile:
        privateKeyEncoded = key.exportKey()
        privateKey = privateKeyEncoded.decode()
        privateKeyFile.write(privateKey)
    with open('id_rsa.pub', 'w', encoding="utf-8") as publicKeyFile:
        publicKeyEncoded = publicKey.exportKey()
        privateKeyDecoded = publicKeyEncoded.decode()
        publicKeyFile.write(privateKeyDecoded)


def load_key(file):
    with open(file, 'r') as KeyFile:
        return RSA.importKey(KeyFile.read())


def encrypt(data, publicKey):
    encodedData = data.encode()
    encdata = publicKey.encrypt(encodedData, 10)
    return encdata[0]


def decrypt(data, privateKey):
    decdata = privateKey.decrypt(data)
    decodedData = decdata.decode()
    return decodedData


def check_integrity():
    pass


if __name__ == '__main__':
    # generate_keys(2048)
    publicKey = load_key('id_rsa-server.pub')
    privateKey = load_key('id_rsa')

    msg = "hello python"
    encr = encrypt(msg, publicKey)
    # print(encr)
    print(decrypt(encr, privateKey))
