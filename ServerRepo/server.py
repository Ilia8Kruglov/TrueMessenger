from select import select
from socket import socket, AF_INET, SOCK_STREAM
from .server_log_config import logger
from jim.utils import *
from jim.jim_protocol import JIMActionMessage, RESPONSE_OK, RESPONSE_ERROR
from .server_db_worker import ServerDBworker
from jim.config_common import *
import sys, os

sys.path.append(os.path.join(os.getcwd(), '..'))


class JIMHandler:

    @staticmethod
    def read_requests(r_clients, all_clients):
        requesters = {}
        for sock in r_clients:
            try:
                data = get_message(sock)
                requesters[sock] = data
                logger.info("Received message: \"{}\" to {}, {}".format(requesters[sock],
                                                                        sock.fileno(), sock.getpeername()))
            except:
                logger.info("Client {} {} disconnected" .format(sock.fileno(), sock.getpeername()))
                all_clients.remove(sock)
        return requesters

    @staticmethod
    def write_responses(data, w_client, all_clients):
        try:
            send_message(w_client, data)
            logger.info("Sending message: \"{}\" to {}, {}".format(data, w_client.fileno(), w_client.getpeername()))
        except:
            logger.info("Client {} {} disconnected".format(w_client.fileno(), w_client.getpeername()))
            w_client.close()
            all_clients.remove(w_client)


class JIMactions:

    @staticmethod
    def authenticate_user(client, message):
        with ServerDBworker() as store:
            username = message[FIELD_USER].get(FIELD_ACCOUNT_NAME)
            password = message[FIELD_USER].get(FIELD_PASSWORD)
            ip = client.getpeername()
            store.add_history(username, ip)
            return store.authenticate_user(username, password)

    @staticmethod
    def add_contact(message):
        with ServerDBworker() as store:
            owner = message.get(FIELD_USERID)
            contact = message.get(FIELD_CONTACT_NAME)
            return store.add_contact(owner, contact)

    @staticmethod
    def del_contact(message):
        with ServerDBworker() as store:
            owner = message.get(FIELD_USERID)
            contact = message.get(FIELD_CONTACT_NAME)
            return store.del_contact(owner, contact)

    @staticmethod
    def get_contacts(message):
        with ServerDBworker() as store:
            owner = message.get(FIELD_USERID)
            list_of_contacts = [str(contact) for contact in store.get_contacts(owner)]
            contacts = ', '.join(list_of_contacts)
            return JIMActionMessage.contact_list(owner, contacts).as_dict

    @staticmethod
    def user_exist(message):
        with ServerDBworker() as store:
            user = message.get('contact_name')
            return store.account_registered(user)

    @staticmethod
    def create_user():
        pass


class JIMserver:
    def __init__(self, ip, port):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server_address = (ip, int(port))
        self.handler = JIMHandler()
        self.start()

    def start(self):
        self.server.bind(self.server_address)
        self.server.listen(20)
        self.server.settimeout(0.2)
        clients = []
        logger.info("The chat server has started successfully")

        while True:
            try:
                conn, addr = self.server.accept()
            except OSError as e:
                pass
            else:
                logger.info("Received connection request from {}".format(addr))
                clients.append(conn)
            finally:
                wait = 0
                input_ready = []
                output_ready = []

                # Start chat between users
                try:
                    input_ready, output_ready, e = select(clients, clients, [], wait)
                except:
                    pass
                requests = self.handler.read_requests(input_ready, clients)

                for sock, data in requests.items():
                    userid = data.get(FIELD_USERID)
                    for w_client in output_ready:
                        processing = JIMactions()
                        # Authenticating a user
                        if data.get(FIELD_ACTION) == ACT_AUTHENTICATE:
                            if processing.authenticate_user(w_client, data):
                                logger.info("User {} is authenticated".format(data[FIELD_USER].get(FIELD_ACCOUNT_NAME)))
                                send_message(conn, RESPONSE_OK.as_dict)
                            else:
                                logger.info("User {} has provided wrong credentials"
                                            .format(data[FIELD_USER].get(FIELD_ACCOUNT_NAME)))
                                send_message(conn, RESPONSE_ERROR.as_dict)
                                clients.remove(conn)
                                conn.close()
                                break

                        # Sending contacts
                        elif data.get(FIELD_ACTION) == ACT_GET_CONTACTS:
                            contacts = processing.get_contacts(data)
                            send_message(conn, contacts)

                        # Deleting a contact
                        elif data.get(FIELD_ACTION) == ACT_DEL_CONTACT:
                            if processing.del_contact(data):
                                pass
                            else:
                                logger.info('The contact has already been deleted')

                        # Adding contact
                        elif data.get(FIELD_ACTION) == ACT_ADD_CONTACT:
                            if processing.user_exist(data):
                                send_message(conn, RESPONSE_OK.as_dict)
                                logger.info('{} is checking: {} is registered'
                                            .format(userid, data.get('contact_name').upper()))
                            else:
                                send_message(conn, RESPONSE_ERROR.as_dict)
                                logger.info('{} is checking: {} is not registerd'
                                            .format(userid, data.get('contact_name').upper()))

                        # Resending normal messages to other user
                        elif data.get(FIELD_ACTION) == ACT_MSG:
                            self.handler.write_responses(data, w_client, clients)


if __name__ == "__main__":
    server = JIMserver('127.0.0.1', '8888')



