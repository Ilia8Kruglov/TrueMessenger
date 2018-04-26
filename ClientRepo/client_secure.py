import hashlib
import binascii


def create_strong_hash(passwd):
    salt = b'5gs'
    digest = hashlib.pbkdf2_hmac('sha256', passwd.encode(), salt, 10000, dklen=128)
    hexdigest = binascii.hexlify(digest).decode()
    return hexdigest


if __name__ == '__main__':
    passwd = create_strong_hash('test')
    print(passwd)




