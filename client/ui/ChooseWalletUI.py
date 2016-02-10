# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChooseWallet.ui'
#
# Created: Sat May  2 05:28:04 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(397, 216)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/windowIcon/coinami.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet(_fromUtf8(""))
        self.verticalLayoutWidget = QtGui.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 381, 111))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.defaultButton = QtGui.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.defaultButton.setFont(font)
        self.defaultButton.setStyleSheet(_fromUtf8(""))
        self.defaultButton.setObjectName(_fromUtf8("defaultButton"))
        self.verticalLayout.addWidget(self.defaultButton)
        self.selectButton = QtGui.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.selectButton.setFont(font)
        self.selectButton.setStyleSheet(_fromUtf8(""))
        self.selectButton.setObjectName(_fromUtf8("selectButton"))
        self.verticalLayout.addWidget(self.selectButton)
        self.newButton = QtGui.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.newButton.setFont(font)
        self.newButton.setStyleSheet(_fromUtf8(""))
        self.newButton.setObjectName(_fromUtf8("newButton"))
        self.verticalLayout.addWidget(self.newButton)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(290, 140, 97, 51))
        self.pushButton.setStyleSheet(_fromUtf8(""))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.statusText = QtGui.QLabel(Form)
        self.statusText.setGeometry(QtCore.QRect(10, 190, 389, 18))
        self.statusText.setObjectName(_fromUtf8("statusText"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Choose a Wallet", None))
        self.defaultButton.setText(_translate("Form", "Use Default Wallet", None))
        self.selectButton.setText(_translate("Form", "Select a Wallet", None))
        self.newButton.setText(_translate("Form", "New Wallet", None))
        self.pushButton.setText(_translate("Form", "OK", None))
        self.statusText.setText(_translate("Form", "TextLabel", None))

import icons_rc
