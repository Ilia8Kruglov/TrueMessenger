# JIM client
# The client module provides TCP initialization with a server
# and connection to the local client DB
# Client - Server asymmetric encryption is being performed for all messages


import json
from os import path
from socket import socket, AF_INET, SOCK_STREAM
from queue import Queue
from .jim.jim_protocol import JIMActionMessage
from .jim.config_common import *
from .jim.utils import send_message, get_message
from .client_db_worker import ClientDBworker
from .security.encryption import load_key


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
    folder = path.dirname(path.abspath(__file__))
    publicKeyPath = path.join(folder, 'security', 'id_rsa_server.pub')
    privateKeyPath = path.join(folder, 'security', 'id_rsa_client')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.address = ('localhost', 9999)
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.storage = LocalStorage(username)
        self.receiver = None
        self.received_encr_data = None
        self.connected = False
        self.publicKey = load_key(self.publicKeyPath)
        self.privateKey = load_key(self.privateKeyPath)
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
        send_message(self.tcp_socket, JIMrequestAdd, self.publicKey)
        response = get_message(self.tcp_socket, self.privateKey)
        if response[FIELD_RESPONSE] == CODE_OK:
            return True
        return False

    def del_contact(self, contact):
        return self.storage.del_contact(contact)

    def authenticate_request(self):
        JIMrequestAuth = JIMActionMessage.authenticate(self.user_auth).as_dict
        if self.connected:
            send_message(self.tcp_socket, JIMrequestAuth, self.publicKey)
            auth_response = get_message(self.tcp_socket, self.privateKey)
            if auth_response[FIELD_RESPONSE] == CODE_OK:
                return True
        return False

    @staticmethod
    def p2p_jim_format(sender, receiver, text):
        return JIMActionMessage.to_user(sender, receiver, text).as_dict

    def get_contacts(self):
        return self.storage.get_contacts()

    def gui_send_messages(self, receiver, text):
            message = self.p2p_jim_format(self.username, receiver, text)
            if self.connected:
                send_message(self.tcp_socket, message, self.publicKey)

    def receive_message(self):
        while self.connected:
            try:
                self.received_encr_data = get_message(self.tcp_socket, self.privateKey)
                if self.received_encr_data:
                    json_data = json.dumps(self.received_encr_data)
                    return json_data
                else:
                    break

            except ConnectionError:
                break

    def close_session(self):
        self.tcp_socket.close()


if __name__ == '__main__':
    client = Client(username='test', password='test')



