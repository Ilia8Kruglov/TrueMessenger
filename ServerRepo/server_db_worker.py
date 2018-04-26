from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from server_db_init import Connector
from datetime import datetime
from os import path

db_folder_path = path.dirname(path.abspath(__file__))
server_db = path.join(db_folder_path, 'server_db.sqlite')
Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String)
    info = Column(String)
    password = Column(String)

    def __init__(self, client):
        self.user_name = client.get('account_name')
        self.info = client.get('status')
        self.password = client.get('password')

    def __repr__(self):
        return self.user_name


class UserHistory(Base):
    __tablename__ = 'UserHistory'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    ip_address = Column(String)
    user_name = Column(String)
    user_id = Column(Integer, ForeignKey('User.user_id'))

    user = relationship("User", backref="history")

    def __init__(self, user_name, ip_address, user_id=None, date=datetime.now()):
        self.date = date
        self.ip_address = "{}:{}".format(ip_address[0], ip_address[1])
        self.user_name = user_name
        self.user_id = user_id

    def __repr__(self):
        activity = '[{}] {} {}'
        return activity.format(self.date, self.user_name, self.ip_address)


class ContactList(Base):
    __tablename__ = 'ContactList'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('User.user_id'))
    contact_name = Column(String)

    user = relationship("User", backref="contacts")

    def __init__(self, owner_id, contact_name):
        self.owner_id = owner_id
        self.contact_name = contact_name

    def __repr__(self):
        return self.contact_name   


class ServerDBworker(Connector):
    def __init__(self):
        self.db = server_db
        super().__init__(self.db)
        Base.metadata.create_all(self.engine)

    def create_user(self, user_dict):
        user = self.session.query(User).filter_by(user_name=user_dict.get('account_name')).first()
        # Checking if user doesn't exist
        if not user:
            new_user = User(user_dict)
            self.session.add(new_user)
        return True

    def add_history(self, user, ip_address):
        user_obj = self.session.query(User).filter_by(user_name=user).first()
        # Checking if user exists
        if user_obj:
            self.session.add(UserHistory(user, ip_address, user_obj.user_id))

    def add_contact(self, owner, contact):
        owner_obj = self.session.query(User).filter_by(user_name=owner).first()
        contact_obj = self.session.query(User).filter_by(user_name=contact).first()

        # Checking if users are registered
        if owner_obj and contact_obj:
            # Checking if interested row doesn't exist
            if not self.session.query(ContactList).filter(ContactList.contact_name == contact_obj.user_name,
                                                          ContactList.owner_id == owner_obj.user_id).first():
                self.session.add(ContactList(owner_obj.user_id, contact_obj.user_name))
                return True
            return False

    def del_contact(self, owner, contact):
        owner_obj = self.session.query(User).filter_by(user_name=owner).first()
        contact_obj = self.session.query(User).filter_by(user_name=contact).first()

        # Checking if interested row exists and getting the object of the row
        delete_query = self.session.query(ContactList).filter(ContactList.contact_name == contact_obj.user_name,
                                                              ContactList.owner_id == owner_obj.user_id).first()
        if delete_query:
            self.session.delete(delete_query)
            return True
        return False

    def get_contacts(self, owner, _count=False):
        owner_obj = self.session.query(User).filter_by(user_name=owner).first()

        if not _count:
            # Checking if users are registered
            if owner_obj:
                contacts = owner_obj.contacts
                return contacts
        else:
            if owner_obj:
                contacts = owner_obj.contacts
                contacts_count = len(contacts)
                return contacts_count

    def authenticate_user(self, user, password):
        user_obj = self.session.query(User).filter_by(user_name=user).first()
        if user_obj:
            if user_obj.password == password:
                return True
        return False

    def account_registered(self, username):
        username_obj = self.session.query(User).filter_by(user_name=username).first()
        if not username_obj:
            return False
        return True


if __name__ == "__main__":
    user_req1 = {'account_name': 'test', 'status': 'Hey, Im here!', 'password': 'f770e2b4fc70acd481d2d2d72dc97c41c3a16e352cf53df3bc5c60366d10ebf67e0d813adffa0ff9482b565abcb770433dc0dbc68aa19b29254a4bebb695c508d9074c27c84e4bb3e7734a23965e1397a8210192c709e5d587b98575b5709c0e2a311276460294b895ee1c422e9b057ec8db140df794d6dc5621968cef394293'}
    user_req2 = {'account_name': 'Anna', 'status': 'Hey, Im here!', 'password': '7e931ec9b4e3fee688b25ac848959dfe94a4d91d2bee65505d4c56965f8dd73038b4c09e70f1bcc2665c763c735a9dcc2aefa8961761c4fdb6ed53868fff44abac3fc7b7423d9349db77fc60e647f41539e684a6518cf0175c24cd50bd4e33aeacb0ea7e0311733e85f539fb85f43a568fe9a385d32f640de2a66898c8f719b5'}
    user_req3 = {'account_name': 'Valera', 'status': 'Hey, Im here!', 'password': '7e931ec9b4e3fee688b25ac848959dfe94a4d91d2bee65505d4c56965f8dd73038b4c09e70f1bcc2665c763c735a9dcc2aefa8961761c4fdb6ed53868fff44abac3fc7b7423d9349db77fc60e647f41539e684a6518cf0175c24cd50bd4e33aeacb0ea7e0311733e85f539fb85f43a568fe9a385d32f640de2a66898c8f719b5'}
    user_req4 = {'account_name': 'Alesya', 'status': 'Hey, Im here!', 'password': '7e931ec9b4e3fee688b25ac848959dfe94a4d91d2bee65505d4c56965f8dd73038b4c09e70f1bcc2665c763c735a9dcc2aefa8961761c4fdb6ed53868fff44abac3fc7b7423d9349db77fc60e647f41539e684a6518cf0175c24cd50bd4e33aeacb0ea7e0311733e85f539fb85f43a568fe9a385d32f640de2a66898c8f719b5'}
    add_contact_req1 = {'action': 'add_contact', 'time': '2018-03-24 16:57:08.502216',
                        'user_id': 'Alesya', 'contact_name': 'Vaysa'}

    with ServerDBworker() as store:
        store.create_user(user_req1)
        store.create_user(user_req2)
        store.create_user(user_req3)
        store.create_user(user_req4)
        store.add_history('Andrei', ('127.0.0.1', 65320))
        store.add_contact('Andrei', 'Valera')
        store.add_contact('Andrei', 'Andrei')
        store.add_contact('Andrei', 'Alesya')
        store.add_history('Anna', ('192.168.1.2', 5555))
        store.add_contact('Anna', 'Valera')
        store.add_contact('Anna', 'Andrei')
        store.add_contact('Anna', 'Alesya')
        store.add_contact('Anna', 'Alesha')
        print(store.get_contacts('Anna'))
        print(store.get_contacts('Anna', _count=True))
        print(store.authenticate_user('Andrei', 'userPwd'))
        # print(store.del_contact('Anna', 'Alesha'))

