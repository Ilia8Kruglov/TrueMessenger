from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from .client_db_init import Connector
from os import path


db_folder_path = path.dirname(path.abspath(__file__))
Base = declarative_base()


class Contact(Base):
    __tablename__ = 'Contacts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    def __init__(self, contact_name):
        self.name = contact_name

    def __repr__(self):
        return self.name


class ClientDBworker(Connector):
    def __init__(self, username):
        self.db_name = '{}.sqlite'.format(username)
        self.db = path.join(db_folder_path, 'db',  self.db_name)
        super().__init__(self.db)
        Base.metadata.create_all(self.engine)

    def add_contact(self, contact):
        user = self.session.query(Contact).filter_by(name=contact).first()
        # Checking if user doesn't exist
        if not user:
            new_user = Contact(contact)
            self.session.add(new_user)
        return True

    def del_contact(self, contact):
        user = self.session.query(Contact).filter_by(name=contact).first()

        # Checking if interested row exists and getting the object of the row
        if user:
            delete_query = self.session.query(Contact).filter(Contact.name == user.name).first()
            if delete_query:
                self.session.delete(delete_query)
                return True
        return False

    @property
    def get_contacts(self):
        owner_obj = self.session.query(Contact)
        return [contact.name for contact in owner_obj]


if __name__ == "__main__":
    add_contact = 'Anna'
    add_contact2 = 'Valera'

    with ClientDBworker('Andrei') as store:
        store.add_contact(add_contact)
        store.add_contact(add_contact2)
        print(store.del_contact('Sergei'))
        print(store.get_contacts)