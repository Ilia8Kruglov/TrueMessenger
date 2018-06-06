# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'contacts.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(200, 606)
        MainWindow.setMinimumSize(QtCore.QSize(200, 0))
        MainWindow.setMaximumSize(QtCore.QSize(200, 16777215))
        MainWindow.setTabletTracking(True)
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":images/icons/chat1.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setMinimumSize(QtCore.QSize(200, 0))
        self.centralwidget.setMaximumSize(QtCore.QSize(200, 16777215))
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 30, 201, 31))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnAdd = QtWidgets.QPushButton(self.layoutWidget)
        self.btnAdd.setEnabled(True)
        self.btnAdd.setMinimumSize(QtCore.QSize(24, 24))
        self.btnAdd.setMaximumSize(QtCore.QSize(35, 24))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnAdd.setFont(font)
        self.btnAdd.setAutoDefault(False)
        self.btnAdd.setDefault(False)
        self.btnAdd.setFlat(True)
        self.btnAdd.setObjectName("btnAdd")
        self.horizontalLayout.addWidget(self.btnAdd)
        self.btnDel = QtWidgets.QPushButton(self.layoutWidget)
        self.btnDel.setEnabled(True)
        self.btnDel.setMinimumSize(QtCore.QSize(24, 24))
        self.btnDel.setMaximumSize(QtCore.QSize(34, 24))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnDel.setFont(font)
        self.btnDel.setIconSize(QtCore.QSize(16, 16))
        self.btnDel.setAutoRepeatDelay(299)
        self.btnDel.setAutoDefault(False)
        self.btnDel.setDefault(False)
        self.btnDel.setFlat(True)
        self.btnDel.setObjectName("btnDel")
        self.horizontalLayout.addWidget(self.btnDel)
        self.btnDel.raise_()
        self.btnAdd.raise_()
        self.lstContacts = QtWidgets.QListWidget(self.centralwidget)
        self.lstContacts.setEnabled(True)
        self.lstContacts.setGeometry(QtCore.QRect(0, 60, 205, 521))
        self.lstContacts.setMinimumSize(QtCore.QSize(205, 0))
        self.lstContacts.setMaximumSize(QtCore.QSize(198, 16777215))
        font = QtGui.QFont()
        font.setItalic(False)
        self.lstContacts.setFont(font)
        self.lstContacts.setStyleSheet("QListView {\n"
"    show-decoration-selected: 1; \n"
"}\n"
"\n"
"QListView::item:alternate {\n"
"    background: #EEEEEE;\n"
"}\n"
"\n"
"QListView::item:selected {\n"
"    border: 1px solid #6a6ea9;\n"
"}\n"
"\n"
"QListView::item:selected:!active {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #ABAFE5, stop: 1 #8588B2);\n"
"}\n"
"\n"
"QListView::item:selected:active {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #6a6ea9, stop: 1 #888dd9);\n"
"}\n"
"\n"
"QListView::item:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #FAFBFE, stop: 1 #DCDEF1);\n"
"}")
        self.lstContacts.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lstContacts.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lstContacts.setLineWidth(10)
        self.lstContacts.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lstContacts.setTabKeyNavigation(True)
        self.lstContacts.setDragEnabled(False)
        self.lstContacts.setAlternatingRowColors(False)
        self.lstContacts.setIconSize(QtCore.QSize(0, 0))
        self.lstContacts.setProperty("ListColor", QtGui.QColor(16, 0, 253))
        self.lstContacts.setObjectName("lstContacts")
        self.lnContact = QtWidgets.QLineEdit(self.centralwidget)
        self.lnContact.setEnabled(True)
        self.lnContact.setGeometry(QtCore.QRect(0, 0, 198, 31))
        self.lnContact.setMinimumSize(QtCore.QSize(198, 0))
        self.lnContact.setMaximumSize(QtCore.QSize(198, 16777215))
        self.lnContact.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.lnContact.setFrame(False)
        self.lnContact.setObjectName("lnContact")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusMessage = QtWidgets.QStatusBar(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.statusMessage.setFont(font)
        self.statusMessage.setObjectName("statusMessage")
        MainWindow.setStatusBar(self.statusMessage)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # mainMenu = self.menuBar()
        # fileMenu = mainMenu.addMenu('File')
        # exitButton = QtWidgets.QAction(QIcon('exit24.png'), 'Exit', self)
        # exitButton.setShortcut('Ctrl+Q')
        # exitButton.setStatusTip('Exit application')
        # exitButton.triggered.connect(self.close)
        # fileMenu.addAction(exitButton)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Contacts"))
        self.btnAdd.setText(_translate("MainWindow", "ADD"))
        self.btnAdd.setShortcut(_translate("MainWindow", "Return", "Enter"))
        self.btnDel.setText(_translate("MainWindow", "DEL"))
        self.lstContacts.setSortingEnabled(True)

import ClientRepo.ui.resources
