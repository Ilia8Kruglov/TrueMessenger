from os import path
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt, QThread, QSize
from PyQt5.QtGui import QIcon, QPixmap
from .client import Client
from .gui_handler import GuiListener
from .ui.chat import Ui_dlgChat
from os import listdir
from os.path import abspath, join, isdir, isfile
from .html_parser import HtmlToShortTag

client_folder_path = path.dirname(path.abspath(__file__))
contact_ui_path = path.join(client_folder_path, 'ui', 'contacts.ui')
chat_window_path = path.join(client_folder_path, 'ui', 'chat.ui')
login_window_path = path.join(client_folder_path, 'ui', 'login.ui')


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        uic.loadUi(contact_ui_path, self)


class ChatWindow(QtWidgets.QDialog):

    def __init__(self, controller, parent=None):
        self.controller = controller
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_dlgChat()
        self.ui.setupUi(self)
        # self.ui.smileButton.clicked.connect(self.smiles_bar)
        self.ui.smileButton.setMenu(self.get_smiles())
        self.ui.smileButton.clicked.connect(self.ui.smileButton.showMenu)

    def get_smiles(self):
        smiles_folder = join('ClientRepo', 'ui', 'images', 'smiles')
        if isdir(smiles_folder):
            _smiles = [name for name in listdir(abspath(smiles_folder)) if isfile(join(smiles_folder, name))]
            _menu = QtWidgets.QMenu()
            _layout = QtWidgets.QGridLayout()
            _menu.setLayout(_layout)
            _count = 0
            for row in range(5):
                for column in range(5):
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
        self.html_parser = HtmlToShortTag()
        self.main_window = MainWindow()
        self.chat_window = ChatWindow(self)
        self.login_window = LoginWindow(self, self.main_window)
        self.main_window.btnAdd.clicked.connect(self.add_contact)
        self.main_window.btnDel.clicked.connect(self.del_contact)
        self.main_window.lstContacts.itemDoubleClicked.connect(self.start_new_chat)
        self.chat_window.ui.btnSendMsg.clicked.connect(self.chat_handler)
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
            contacts_list = self.client.get_contacts()
            self.main_window.lstContacts.clear()
            for contact in contacts_list:
                self.main_window.lstContacts.addItem(contact.strip())

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
                elif new_contact and not self.main_window.lstContacts.findItems(new_contact, Qt.MatchExactly):
                    self.client.add_contact(new_contact)
                    self.main_window.lstContacts.addItem(new_contact)
                    self.main_window.lnContact.update()
                    self.main_window.lnContact.clear()
                    self.main_window.statusMessage.showMessage('Done', 2000)
                elif new_contact and self.main_window.lstContacts.findItems(new_contact, Qt.MatchExactly):
                    self.main_window.lnContact.clear()
                    self.main_window.statusMessage.showMessage('\'{}\' already in contact list'
                                                               .format(new_contact), 2000)

            except Exception as error:
                print(error)

    def del_contact(self):
        if self.authenticated:
            try:
                contact = self.main_window.lstContacts.currentItem()
                username = contact.text()
                self.main_window.lstContacts.takeItem(self.main_window.lstContacts.row(contact))
                self.client.del_contact(username)
                self.main_window.lnContact.update()
                del contact
                self.main_window.statusMessage.showMessage('\'{}\' has been deleted'.format(username), 2000)
            except Exception as error:
                print(error)

    def start_new_chat(self):
        if self.authenticated:
            sender = self.client.username
            receiver = self.main_window.lstContacts.currentItem().text()
            self.chat_window.setWindowTitle('TrueMessenger - {} in chat with {}'.format(sender, receiver))
            self.chat_window.exec()

    def chat_handler(self):
        if self.authenticated:
            text = self.chat_window.ui.txtNewMessage.toPlainText()
            self.html_parser.feed(self.chat_window.ui.txtNewMessage.toHtml())
            _message = self.html_parser.tagged_message
            print(_message)
            if _message:
                self.client.gui_send_messages(text.strip())
                self.chat_window.ui.txtChatMessages.append(_message)
                self.chat_window.ui.txtNewMessage.clear()

    def update_chat(self, data):
        try:
            self.chat_window.ui.txtChatMessages.append(data)

        except Exception as e:
            print(e)

    def update_toolbar(self):
        pass


if __name__ == "__main__":
    app = GuiController()


