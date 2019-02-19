# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\serialWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 513)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.messageLine = QtWidgets.QLineEdit(self.centralwidget)
        self.messageLine.setObjectName("messageLine")
        self.gridLayout.addWidget(self.messageLine, 0, 0, 1, 1)
        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sendButton.setFont(font)
        self.sendButton.setObjectName("sendButton")
        self.gridLayout.addWidget(self.sendButton, 0, 1, 1, 1)
        self.serialDisplay = QtWidgets.QTextBrowser(self.centralwidget)
        self.serialDisplay.setReadOnly(True)
        self.serialDisplay.setObjectName("serialDisplay")
        self.gridLayout.addWidget(self.serialDisplay, 1, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuBAUD = QtWidgets.QMenu(self.menubar)
        self.menuBAUD.setObjectName("menuBAUD")
        self.menuPORT = QtWidgets.QMenu(self.menubar)
        self.menuPORT.setObjectName("menuPORT")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionClear_Output = QtWidgets.QAction(MainWindow)
        self.actionClear_Output.setObjectName("actionClear_Output")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionClear_Output)
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuBAUD.menuAction())
        self.menubar.addAction(self.menuPORT.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.sendButton.setText(_translate("MainWindow", "Send"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuBAUD.setTitle(_translate("MainWindow", "BAUD"))
        self.menuPORT.setTitle(_translate("MainWindow", "PORT"))
        self.actionClear_Output.setText(_translate("MainWindow", "Clear Output"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

