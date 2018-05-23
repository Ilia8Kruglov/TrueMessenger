from datetime import datetime
from .config_common import *

FORMAT_ACTION = {FIELD_NAME: FIELD_ACTION, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 15}
FORMAT_ALERT = {FIELD_NAME: FIELD_ALERT, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 128}
FORMAT_ERROR = {FIELD_NAME: FIELD_ERROR, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 128}
FORMAT_RESPONSE = {FIELD_NAME: FIELD_RESPONSE, FIELD_VALUE: 000, FIELD_TYPE: int, FIELD_LENGTH: 3}
FORMAT_MESSAGE = {FIELD_NAME: FIELD_MESSAGE, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 1000}
FORMAT_TIME = {FIELD_NAME: FIELD_TIME, FIELD_VALUE: 20180101, FIELD_TYPE: str, FIELD_LENGTH: 50}
FORMAT_USER = {FIELD_NAME: FIELD_USER, FIELD_VALUE: '', FIELD_TYPE: dict, FIELD_LENGTH: 3}
FORMAT_MSG_TYPE = {FIELD_NAME: FIELD_MSG_TYPE, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 15}
FORMAT_SENDER = {FIELD_NAME: FIELD_SENDER, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 25}
FORMAT_RECEIVER = {FIELD_NAME: FIELD_RECEIVER, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 25}
FORMAT_ENCODING = {FIELD_NAME: FIELD_ENCODING, FIELD_VALUE: 'utf-8', FIELD_TYPE: str, FIELD_LENGTH: 8}
FORMAT_CONTACT_NAME = {FIELD_NAME: FIELD_CONTACT_NAME, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 24}
FORMAT_USERID = {FIELD_NAME: FIELD_USERID, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 24}
FORMAT_CONTACTS = {FIELD_NAME: FIELD_CONTACTS, FIELD_VALUE: '', FIELD_TYPE: str, FIELD_LENGTH: 1024}


class ProtocolDescriptor:

    def __init__(self, name, value, type_name, max_length):
        self.name = '_' + name
        self.type = type_name
        self.value = value
        self.max_length = max_length

    def __get__(self, instance, cls):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError('{}{} should be \'{}\' type.'.format(
                instance.__class__.__name__, self.name, self.type.__name__))

        try:
            value_length = len(value)
        except TypeError:
            value_length = len(str(value))

        if value_length > self.max_length:
            raise ValueError('Length of {}{}={} should not exceed {} symbols.'.format(
                instance.__class__.__name__, self.name, value, self.max_length))

        setattr(instance, self.name, value)


class JIMActionMessage:

    action = ProtocolDescriptor(**FORMAT_ACTION)
    msgtime = ProtocolDescriptor(**FORMAT_TIME)
    message = ProtocolDescriptor(**FORMAT_MESSAGE)
    msgtype = ProtocolDescriptor(**FORMAT_MSG_TYPE)
    user = ProtocolDescriptor(**FORMAT_USER)
    receiver = ProtocolDescriptor(**FORMAT_RECEIVER)
    sender = ProtocolDescriptor(**FORMAT_SENDER)
    encoding = ProtocolDescriptor(**FORMAT_ENCODING)
    contact_name = ProtocolDescriptor(**FORMAT_CONTACT_NAME)
    user_id = ProtocolDescriptor(**FORMAT_USERID)
    contacts = ProtocolDescriptor(**FORMAT_CONTACTS)

    __slots__ = {
        action.name,  msgtime.name, message.name, user.name, msgtype.name, sender.name, encoding.name,
        contact_name.name, user_id.name, contacts.name, receiver.name
    }

    user_fields = [FIELD_ACCOUNT_NAME, FIELD_PASSWORD, FIELD_STATUS]

    def __init__(self, **kwargs):
        dt = datetime.now()
        self.msgtime = str(dt.strftime("%b %d, %Y %I:%M %p"))
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def as_dict(self):
        attrs_dict = {}
        for attr in self.__slots__:
            try:
                val = (getattr(self, attr))
                attr = attr.lstrip('_')
                if attr not in attrs_dict.keys():
                    attrs_dict.update({attr: None})
                attrs_dict.update({attr: val})
            except AttributeError:
                pass
        return attrs_dict

    @staticmethod
    def presence(user, msgtype='status'):
        user = {key: value for key, value in user.items() if key in JIMActionMessage.user_fields}
        return JIMActionMessage(action=ACT_PRESENCE, user=user, msgtype=msgtype)

    @staticmethod
    def to_user(user, receiver, message):
        return JIMActionMessage(action=ACT_MSG, sender=user, receiver=receiver, message=message)

    @staticmethod
    def to_all_users(user, message, encoding='ascii'):
        return JIMActionMessage(action=ACT_MSG, sender=user, message=message, encoding=encoding)

    @staticmethod
    def add_contact(user, contact):
        return JIMActionMessage(action=ACT_ADD_CONTACT, user_id=user, contact_name=contact)

    @staticmethod
    def authenticate(user):
        user = {key: value for key, value in user.items() if key in JIMActionMessage.user_fields}
        return JIMActionMessage(action=ACT_AUTHENTICATE, user=user)

    @staticmethod
    def get_contacts(user):
        return JIMActionMessage(action=ACT_GET_CONTACTS, user_id=user)

    @staticmethod
    def contact_list(user, contacts):
        return JIMActionMessage(sender=user, action=ACT_CONTACT_LIST, message=contacts)

    @staticmethod
    def del_contact(user, contact):
        return JIMActionMessage(action=ACT_DEL_CONTACT, user_id=user, contact_name=contact)


class JIMResponseMessage:
    alert = ProtocolDescriptor(**FORMAT_ALERT)
    error = ProtocolDescriptor(**FORMAT_ERROR)
    response = ProtocolDescriptor(**FORMAT_RESPONSE)
    response_time = ProtocolDescriptor(**FORMAT_TIME)

    __slots__ = {
        response.name, alert.name, error.name, response_time.name
    }

    def __init__(self, *args):
        if isinstance(args[0], list):
            pass
        elif isinstance(args[0], dict):
            for k, v in args[0].items():
                setattr(self, k, v)

    @property
    def as_dict(self):
        attrs_dict = {}
        for attr in self.__slots__:
            try:
                val = (getattr(self, attr))
                attr = attr.lstrip('_')
                if attr not in attrs_dict.keys():
                    attrs_dict.update({attr: None})
                attrs_dict.update({attr: val})
            except AttributeError:
                pass
        return attrs_dict


RESPONSE_OK = JIMResponseMessage({FIELD_RESPONSE: CODE_OK})
RESPONSE_ACCEPTED = JIMResponseMessage({FIELD_RESPONSE: CODE_ACCEPTED})
RESPONSE_ERROR = JIMResponseMessage({FIELD_RESPONSE: CODE_ERROR})


if __name__ == '__main__':
    user = {FIELD_ACCOUNT_NAME: 'user', FIELD_STATUS: 'Hey, Im here!', FIELD_PASSWORD: 'password'}
    print(JIMActionMessage.presence(user).as_dict)
    RESPONSE_OK = JIMResponseMessage({FIELD_RESPONSE: CODE_OK})
    RESPONSE_ERROR = JIMResponseMessage({FIELD_RESPONSE: CODE_ERROR})
    RESPONSE_ACCEPTED = JIMResponseMessage({FIELD_RESPONSE: CODE_ACCEPTED})
    # print(RESPONSE_OK.as_dict)
    # print(RESPONSE_ERROR.as_dict)
    # print(JIMActionMessage.to_all_users('Andrei', 'hello guys').as_dict)
    # print(JIMActionMessage.add_contact('Andrei', 'Vaysa').as_dict)
    # print(JIMActionMessage.authenticate(user).as_dict)
    # print(JIMActionMessage.get_contacts('Andrei').as_dict)
    # print(JIMActionMessage.contact_list('Andrei', 'Vasya, Anna').as_dict)
    # print(JIMActionMessage.del_contact('Andrei', 'Vasya').as_dict)

    print(JIMActionMessage.to_user('Andrei', 'Anna', 'hello guys').as_dict)


