import hashlib
import binascii


def verify_hash(passwd):
    salt = b'5gs'
    digest = hashlib.pbkdf2_hmac('sha256', passwd.encode(), salt, 10000, dklen=128)
    hexdigest = binascii.hexlify(digest).decode('utf-8')
    return hexdigest


passwd = verify_hash('test')
print(passwd)
