from socket import socket, AF_INET, SOCK_STREAM
from jim.jim_protocol import JIMActionMessage
from jim.config_common import *
from jim.utils import send_message, get_message
from queue import Queue
from .client_secure import *
from .client_db_worker import ClientDBworker
import sys
import json


class LocalStorage:
    ''' Interaction with local DB '''

    def __init__(self, user):
        self.user = user

    def add_contact(self, contact):

        with ClientDBworker(self.user) as store:
            return store.add_contact(contact)

    def get_contacts(self):
        with ClientDBworker(self.user) as store:
            return store.get_contacts

    def del_contact(self, contact):
        with ClientDBworker(self.user) as store:
            return store.del_contact(contact)


class Client:
    def __init__(self, username, password):
        self.username = username
        self.password = create_strong_hash(password)
        self.address = ('localhost', 8888)
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.storage = LocalStorage(username)
        self.receiver = None
        self.received_data = None
        self.connected = False
        self.request_queue = Queue()
        self.user_presence = {FIELD_ACCOUNT_NAME: self.username, FIELD_STATUS: 'Hey there!'}
        self.user_auth = {FIELD_ACCOUNT_NAME: self.username, FIELD_STATUS: 'Authenticating',
                          FIELD_PASSWORD: self.password}

        self.start()
        self.authenticate = self.authenticate_request()

    def start(self):
        self.tcp_socket.connect(self.address)
        self.connected = True

    def create_presence(self):
        presence = JIMActionMessage.presence(self.user_presence).as_dict
        return presence

    def add_contact(self, contact):
        if self.user_exist(contact):
            return self.storage.add_contact(contact)
        return False

    def user_exist(self, contact):
        JIMrequestAdd = JIMActionMessage.add_contact(self.username, contact).as_dict
        send_message(self.tcp_socket, JIMrequestAdd)
        response = get_message(self.tcp_socket)
        if response[FIELD_RESPONSE] == CODE_OK:
            return True
        return False

    def del_contact(self, contact):
        return self.storage.del_contact(contact)

    def authenticate_request(self):
        request = JIMActionMessage.authenticate(self.user_auth).as_dict
        if self.connected:
            self.tcp_socket.send(json.dumps(request).encode('ascii'))
            auth_response = get_message(self.tcp_socket)
            if auth_response[FIELD_RESPONSE] == CODE_OK:
                return True
        return False

    def create_message(self, text):
        return JIMActionMessage.to_all_users(self.username, text).as_dict

    def get_contacts(self):
        return self.storage.get_contacts()

    def gui_send_messages(self, text):
            message = self.create_message(text)
            if self.connected:
                self.tcp_socket.send(json.dumps(message).encode('ascii'))

    def receive_message(self):

        while self.connected:
            try:
                self.received_data = self.tcp_socket.recv(1024)
                if self.received_data:
                    json_data = json.loads(json.dumps(self.received_data.decode('ascii')))
                    return json_data
                else:
                    break

            except ConnectionError:
                break

    def close_session(self):
        self.tcp_socket.close()


if __name__ == '__main__':
    try:
        username = sys.argv[1]
    except IndexError:
        username = 'Andrei'

    try:
        password = sys.argv[2]
    except IndexError:
        password = 'test'

    try:
        ip = sys.argv[3]
    except IndexError:
        ip = 'localhost'

    try:
        port = sys.argv[4]
    except IndexError:
        port = 10000

    client = Client(username, password)



