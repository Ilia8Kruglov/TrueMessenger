# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QTextCursor


class Ui_dlgChat(object):
    def __init__(self, controller):
        self.bold = None
        self.italic = None
        self.underline = None
        self.strike = None
        self.controller = controller
        self.default_user_logo = None

    def setupUi(self, dlgChat):
        dlgChat.setObjectName("dlgChat")
        dlgChat.resize(579, 409)
        dlgChat.setBaseSize(QtCore.QSize(700, 600))
        dlgChat.setWindowTitle("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":images/icons/chat1.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dlgChat.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(dlgChat)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.txtChatMessages = QtWidgets.QTextEdit(dlgChat)
        self.txtChatMessages.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.txtChatMessages.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.txtChatMessages.setObjectName("txtChatMessages")
        self.verticalLayout.addWidget(self.txtChatMessages)

        self.toolbar = QtWidgets.QToolBar(dlgChat)
        self.verticalLayout.addWidget(self.toolbar)
        smiles_icn = QtGui.QIcon()
        smiles_icn.addPixmap(QtGui.QPixmap(":/images/icons/pressed_smile_btn.png"))
        self.smileButton = QtWidgets.QToolButton()
        self.smileButton.setIcon(smiles_icn)
        self.smileButton.setFixedSize(25,25)
        self.smileButton.setArrowType(Qt.NoArrow)
        iconTextBold = QtGui.QIcon()
        iconTextBold.addPixmap(QPixmap(":/images/icons/b.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        iconTextItalic = QtGui.QIcon()
        iconTextItalic.addPixmap(QPixmap(":/images/icons/i.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        iconTextUnderline = QtGui.QIcon()
        iconTextUnderline.addPixmap(QPixmap(":/images/icons/u.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        iconTextStrike = QtGui.QIcon()
        iconTextStrike.addPixmap(QPixmap(":/images/icons/S.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bold = QtWidgets.QAction(QtGui.QIcon(":/images/icons/b.jpg"), 'Bold', self.controller)
        self.bold.setCheckable(True)
        self.italic = QtWidgets.QAction(iconTextItalic, 'Italic', self.controller)
        self.italic.setCheckable(True)
        self.underline = QtWidgets.QAction(iconTextUnderline, 'Underline', self.controller)
        self.underline.setCheckable(True)
        self.strike = QtWidgets.QAction(iconTextStrike, 'Strike-out', self.controller)
        self.strike.setCheckable(True)
        self.toolbar.addWidget(self.smileButton)
        self.toolbar.addAction(self.bold)
        self.toolbar.addAction(self.italic)
        self.toolbar.addAction(self.underline)
        self.toolbar.addAction(self.strike)


        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.txtNewMessage = QtWidgets.QTextEdit(dlgChat)
        self.txtNewMessage.setMinimumHeight(300)
        self.txtNewMessage.setMinimumSize(QtCore.QSize(0, 40))
        self.txtNewMessage.setMaximumSize(QtCore.QSize(16777215, 80))
        self.txtNewMessage.setFrameShape(QtWidgets.QFrame.HLine)
        self.txtNewMessage.setFrameShadow(QtWidgets.QFrame.Plain)
        self.txtNewMessage.setLineWidth(1)
        self.txtNewMessage.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtNewMessage.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtNewMessage.setObjectName("txtNewMessage")
        self.verticalLayout.addWidget(self.txtNewMessage)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnSendMsg = QtWidgets.QPushButton(dlgChat)
        self.btnSendMsg.setMinimumSize(QtCore.QSize(0, 20))
        self.btnSendMsg.setMaximumSize(QtCore.QSize(16777215, 20))
        self.btnSendMsg.setAutoDefault(True)
        self.btnSendMsg.setDefault(True)
        self.btnSendMsg.setFlat(True)
        self.btnSendMsg.setObjectName("btnSendMsg")
        self.horizontalLayout.addWidget(self.btnSendMsg)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslateUi(dlgChat)
        QtCore.QMetaObject.connectSlotsByName(dlgChat)
        dlgChat.setTabOrder(self.btnSendMsg, self.txtChatMessages)


    def retranslateUi(self, dlgChat):
        _translate = QtCore.QCoreApplication.translate
        self.txtChatMessages.setHtml(_translate("dlgChat", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.btnSendMsg.setText(_translate("dlgChat", "Send"))
        self.btnSendMsg.setShortcut(_translate("dlgChat", "Ctrl+Return"))

import ClientRepo.ui.resources
