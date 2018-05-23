from os import path
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QThread, QSize
from PyQt5.QtGui import QIcon, QFont, QPixmap
from os import listdir
from os.path import abspath, join, isdir, isfile
from datetime import datetime
from .client import Client
from .gui_handler import GuiListener
from .ui.chat import Ui_dlgChat
from .html_parser import HtmlToShortTag
from .config import *


client_folder_path = path.dirname(path.abspath(__file__))
contact_ui_path = path.join(client_folder_path, 'ui', 'contacts.ui')
login_window_path = path.join(client_folder_path, 'ui', 'login.ui')
dt = datetime.now()


class QCustomQWidget (QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QtWidgets.QVBoxLayout()
        self.textUpQLabel = QtWidgets.QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.allQHBoxLayout = QtWidgets.QHBoxLayout()
        self.iconQLabel = QtWidgets.QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        self.textUpQLabel.setStyleSheet('''
            color: rgb(0, 0, 255);
            font-size: 16pt;
        ''')

    def setText (self, text):
        self.textUpQLabel.setText(text)

    def setIcon (self, imagePath):
        self.iconQLabel.setPixmap(QPixmap(imagePath))


class QCustomListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, text, parent = None):
        super(QCustomListWidgetItem, self).__init__(parent)
        self.text = text


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        uic.loadUi(contact_ui_path, self)


class ChatWindow(QtWidgets.QDialog):

    def __init__(self, controller, _sender, _receiver, parent=None):
        self.controller = controller
        self._sender = _sender
        self._receiver = _receiver
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_dlgChat(self)
        self.ui.setupUi(self)
        self.ui.smileButton.setMenu(self.get_smiles())
        self.ui.smileButton.clicked.connect(self.ui.smileButton.showMenu)
        self.ui.btnSendMsg.clicked.connect(self.controller.chat_handler)
        self.ui.bold.triggered.connect(self.set_text_format(self.ui.bold))
        self.ui.italic.triggered.connect(self.set_text_format(self.ui.italic))
        self.ui.underline.triggered.connect(self.set_text_format(self.ui.underline))
        self.ui.strike.triggered.connect(self.set_text_format(self.ui.strike))

    def get_smiles(self):
        smiles_folder = join('ClientRepo', 'ui', 'images', 'smiles')
        if isdir(smiles_folder):
            _smiles = [name for name in listdir(abspath(smiles_folder)) if isfile(join(smiles_folder, name))]
            _menu = QtWidgets.QMenu()
            _layout = QtWidgets.QGridLayout()
            _menu.setLayout(_layout)
            _count = 0
            for row in range(6):
                for column in range(8):
                    try:
                        _smile = join(smiles_folder, _smiles[_count])
                        _icon = QIcon(_smile)
                        _button = QtWidgets.QToolButton(self)
                        _button.setFixedSize(QSize(32, 32))
                        _button.setIcon(_icon)
                        _button.setIconSize(_button.size())
                        _button.setAutoRaise(True)
                        _layout.addWidget(_button, row, column)
                        _button.setToolTip(_smiles[_count].split('.')[0])
                        _button.clicked.connect(self.insert_smile(_smile, self.ui))
                        _count += 1
                    except IndexError:
                        break

            return _menu

        else:
            self.ui.smileButton.setEnabled(False)

    @staticmethod
    def insert_smile(smile, chat):
        def insert():
            chat.txtNewMessage.textCursor().insertImage(smile)
            chat.smileButton.menu().hide()
        return insert

    @staticmethod
    def insert_logo(logo, chat):
        def insert():
            chat.txtNewMessage.textCursor().insertImage(logo)
        return insert

    @staticmethod
    def set_text_format(button):
        def font_format():
            chat = button.parent()

            if button is chat.ui.bold and chat.ui.txtNewMessage.fontWeight() == QFont.Normal:
                chat.ui.txtNewMessage.setFontWeight(QFont.Black)
            elif button is chat.ui.bold and chat.ui.txtNewMessage.fontWeight() == QFont.Black:
                chat.ui.txtNewMessage.setFontWeight(QFont.Normal)
            elif button is chat.ui.italic:
                chat.ui.txtNewMessage.setFontItalic(not chat.ui.txtNewMessage.fontItalic())
            elif button is chat.ui.underline:
                chat.ui.txtNewMessage.setFontUnderline(not chat.ui.txtNewMessage.fontUnderline())
            elif button is chat.ui.strike:
                strike_fmt = chat.ui.txtNewMessage.currentCharFormat()
                strike_fmt.setFontStrikeOut(not strike_fmt.fontStrikeOut())
                chat.ui.txtNewMessage.setCurrentCharFormat(strike_fmt)
            if chat.ui.txtNewMessage.textCursor().selectedText():
                button.setChecked(not button.isChecked())

        return font_format


class LoginWindow(QtWidgets.QDialog):
    def __init__(self, controller, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        uic.loadUi(login_window_path, self)
        self.buttonBox.accepted.connect(controller.get_client)
        self.buttonBox.rejected.connect(self.parent().close)
        self.lnPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, QCloseEvent):
        self.parent().close()


class GuiController:
    app = QtWidgets.QApplication([])

    def __init__(self):
        self.client = None
        self.thread = None
        self.username = None
        self.password = None
        self.GuiListener = None
        self.authenticated = None
        self.receiver = None
        self.receiver_room = None
        self.chat_window = None
        self.rooms = set()
        self.contacts_list = []
        self.html_parser = HtmlToShortTag()
        self.main_window = MainWindow()
        self.login_window = LoginWindow(self, self.main_window)
        self.main_window.btnAdd.clicked.connect(self.add_contact)
        self.main_window.btnDel.clicked.connect(self.del_contact)
        self.main_window.lstContacts.itemDoubleClicked.connect(self.start_new_chat)
        self.run()

    def run(self):
        self.login_window.show()
        self.app.exec_()

    def get_client(self):
        self.username = self.login_window.lnLogin.text()
        self.password = self.login_window.lnPassword.text()
        if self.username:
            self.authenticate()
        else:
            self.run()

    def connect(self):
        self.load_contacts()
        self.main_window.setWindowTitle('Signed as {}'.format(self.client.username))
        self.GuiListener = GuiListener(self.client, self.client.request_queue)
        self.GuiListener.gotData.connect(self.update_chat)
        self.thread = QThread()
        self.GuiListener.moveToThread(self.thread)
        self.thread.started.connect(self.GuiListener.get_message)
        self.thread.start()
        self.main_window.show()

    def authenticate(self):
        self.client = Client(self.username, self.password)
        if self.client.authenticate:
            self.authenticated = True
            self.connect()
        else:
            self.run()

    def load_contacts(self):
        if self.authenticated:
            self.contacts_list = self.client.get_contacts()
            self.main_window.lstContacts.clear()
            for contact in self.contacts_list:
                icon = 'ClientRepo/ui/images/icons/list_default_image'
                myQCustomQWidget = self.contact_widget(icon, contact)
                myQListWidgetItem = QCustomListWidgetItem(contact, self.main_window.lstContacts)
                myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
                self.chat_window = ChatWindow(self, contact, self.username)
                self.rooms.add(self.chat_window)
                self.main_window.lstContacts.addItem(myQListWidgetItem)
                self.main_window.lstContacts.setItemWidget(myQListWidgetItem, myQCustomQWidget)

    @staticmethod
    def contact_widget(icon, contact):
        widget = QCustomQWidget()
        widget.setText(contact.strip())
        widget.setIcon(icon)
        return widget

    def add_contact(self):
        if self.authenticated:
            try:
                new_contact = self.main_window.lnContact.text()
                if not new_contact:
                    self.main_window.statusMessage.showMessage('Please provide a contact name', 2000)
                elif not self.client.add_contact(new_contact):
                    self.main_window.statusMessage.showMessage('\'{}\' is not registered'
                                                               .format(new_contact), 2000)
                    self.main_window.lnContact.clear()
                elif new_contact and new_contact in self.contacts_list:
                    self.main_window.lnContact.clear()
                    self.main_window.statusMessage.showMessage('\'{}\' already in contact list'
                                                               .format(new_contact), 2000)
                elif new_contact and not new_contact in self.contacts_list:
                    icon = 'ClientRepo/ui/images/icons/list_default_image'
                    self.chat_window = ChatWindow(self, new_contact, self.username)
                    myQCustomQWidget = self.contact_widget(icon, new_contact.strip())
                    newContactItem = QCustomListWidgetItem(new_contact, self.main_window.lstContacts)
                    newContactItem.setSizeHint(myQCustomQWidget.sizeHint())
                    self.client.add_contact(new_contact)
                    self.main_window.lstContacts.addItem(newContactItem)
                    self.main_window.lstContacts.setItemWidget(newContactItem, myQCustomQWidget)
                    self.main_window.lnContact.update()
                    self.main_window.lnContact.clear()
                    self.rooms.add(self.chat_window)
                    self.main_window.statusMessage.showMessage('Done', 2000)
                else:
                    pass

            except Exception as error:
                print(error)

    def del_contact(self):
        if self.authenticated:
            try:
                contact = self.main_window.lstContacts.currentItem()
                username = contact.text
                self.main_window.lstContacts.takeItem(self.main_window.lstContacts.row(contact))
                self.client.del_contact(username)
                self.main_window.lnContact.update()
                del contact
                self.contacts_list.remove(username)
                self.main_window.statusMessage.showMessage('\'{}\' has been deleted'.format(username), 2000)
            except Exception as error:
                print(error)

    def start_new_chat(self):
        if self.authenticated:
            sender = self.client.username
            self.receiver = self.main_window.lstContacts.currentItem().text
            self.receiver_room = self.chat_room_gateway(self.receiver)
            self.receiver_room.setWindowTitle('TrueMessenger - {} in chat with {}'.format(sender, self.receiver))
            self.receiver_room.exec()

    def chat_handler(self):
        if self.authenticated:
            self.html_parser.feed(self.receiver_room.ui.txtNewMessage.toHtml())
            _message = self.html_parser.tagged_message
            msg_to_displ = outgoing_new_msg_table.format(str(dt.strftime("%b %d, %Y %I:%M %p")),
                                                self.default_user_logo(),
                                                self.username, _message)
            if _message:
                self.client.gui_send_messages(self.receiver, _message)
                self.receiver_room.ui.txtChatMessages.append(msg_to_displ)
                self.receiver_room.ui.txtNewMessage.clear()

    def update_chat(self, msg):
        try:
            if msg['action'] == 'msg' and msg['to'] == self.username:
                text_msg = incoming_new_msg_table.format(msg.get('time'), self.default_user_logo(),
                                                msg.get('from'), msg.get('message'))
                _from_user = msg.get('from')
                recevier_room_input = self.chat_room_gateway(_from_user)
                recevier_room_input.ui.txtChatMessages.append(text_msg)
        except Exception as e:
            print(e)

    def chat_room_gateway(self, _from_user):
        recevier_room = [room for room in self.rooms if _from_user == room._sender]
        return recevier_room[0]

    @staticmethod
    def default_user_logo():
        logo_folder = join('ClientRepo', 'ui', 'images', 'icons')
        _logoPath = join(logo_folder, 'default_profile.png')
        _defaultLogo = '<img src="{}"/>'.format(_logoPath)
        return _defaultLogo


if __name__ == "__main__":
    app = GuiController()



