# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddContact.ui'
#
# Created: Sat May  2 05:28:08 2015
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(330, 162)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/windowIcon/coinami.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setStyleSheet(_fromUtf8(""))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(150, 120, 171, 31))
        self.buttonBox.setStyleSheet(_fromUtf8(""))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.addContactNameEdit = QtGui.QLineEdit(Dialog)
        self.addContactNameEdit.setGeometry(QtCore.QRect(10, 10, 311, 41))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.addContactNameEdit.setFont(font)
        self.addContactNameEdit.setStyleSheet(_fromUtf8(""))
        self.addContactNameEdit.setText(_fromUtf8(""))
        self.addContactNameEdit.setObjectName(_fromUtf8("addContactNameEdit"))
        self.addContactAddressEdit = QtGui.QLineEdit(Dialog)
        self.addContactAddressEdit.setGeometry(QtCore.QRect(10, 60, 311, 41))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.addContactAddressEdit.setFont(font)
        self.addContactAddressEdit.setStyleSheet(_fromUtf8(""))
        self.addContactAddressEdit.setText(_fromUtf8(""))
        self.addContactAddressEdit.setObjectName(_fromUtf8("addContactAddressEdit"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Add Contact", None))
        self.addContactNameEdit.setToolTip(_translate("Dialog", "<html><head/><body><p>Coins</p></body></html>", None))
        self.addContactNameEdit.setPlaceholderText(_translate("Dialog", "Name", None))
        self.addContactAddressEdit.setToolTip(_translate("Dialog", "<html><head/><body><p>Coins</p></body></html>", None))
        self.addContactAddressEdit.setPlaceholderText(_translate("Dialog", "Address", None))

import icons_rc
