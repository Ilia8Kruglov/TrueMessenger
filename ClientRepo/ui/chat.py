# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Chat(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Chat")
        Dialog.resize(398, 350)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        Dialog.setFont(font)
        Dialog.setFocusPolicy(QtCore.Qt.StrongFocus)
        Dialog.setAcceptDrops(True)
        Dialog.setInputMethodHints(QtCore.Qt.ImhNone)
        Dialog.setModal(False)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 310, 401, 32))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnSendMsg = QtWidgets.QPushButton(self.layoutWidget)
        self.btnSendMsg.setMinimumSize(QtCore.QSize(200, 20))
        self.btnSendMsg.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnSendMsg.setFont(font)
        self.btnSendMsg.setAutoDefault(True)
        self.btnSendMsg.setDefault(True)
        self.btnSendMsg.setFlat(True)
        self.btnSendMsg.setObjectName("btnSendMsg")
        self.horizontalLayout.addWidget(self.btnSendMsg)
        self.txtChatMessages = QtWidgets.QTextEdit(Dialog)
        self.txtChatMessages.setGeometry(QtCore.QRect(0, 0, 398, 231))
        self.txtChatMessages.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.txtChatMessages.setObjectName("txtChatMessages")
        self.txtNewMessage = QtWidgets.QTextEdit(Dialog)
        self.txtNewMessage.setGeometry(QtCore.QRect(0, 230, 398, 80))
        self.txtNewMessage.setMinimumSize(QtCore.QSize(0, 40))
        self.txtNewMessage.setMaximumSize(QtCore.QSize(16777215, 80))
        self.txtNewMessage.setFrameShape(QtWidgets.QFrame.HLine)
        self.txtNewMessage.setFrameShadow(QtWidgets.QFrame.Plain)
        self.txtNewMessage.setLineWidth(1)
        self.txtNewMessage.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtNewMessage.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtNewMessage.setObjectName("txtNewMessage")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Chat"))
        self.btnSendMsg.setText(_translate("Dialog", "Send"))

