# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SignVerify.ui'
#
# Created: Sun May  3 11:07:56 2015
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
        Dialog.resize(472, 522)
        self.verticalLayoutWidget = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(1, 6, 471, 511))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setMargin(3)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.messageEdit = QtGui.QTextEdit(self.verticalLayoutWidget)
        self.messageEdit.setObjectName(_fromUtf8("messageEdit"))
        self.verticalLayout.addWidget(self.messageEdit)
        self.addressEdit = QtGui.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addressEdit.sizePolicy().hasHeightForWidth())
        self.addressEdit.setSizePolicy(sizePolicy)
        self.addressEdit.setObjectName(_fromUtf8("addressEdit"))
        self.verticalLayout.addWidget(self.addressEdit)
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMargin(3)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.signatureEdit = QtGui.QTextEdit(self.verticalLayoutWidget)
        self.signatureEdit.setObjectName(_fromUtf8("signatureEdit"))
        self.verticalLayout.addWidget(self.signatureEdit)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.signButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.signButton.setObjectName(_fromUtf8("signButton"))
        self.horizontalLayout.addWidget(self.signButton)
        self.verifyButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.verifyButton.setObjectName(_fromUtf8("verifyButton"))
        self.horizontalLayout.addWidget(self.verifyButton)
        self.closeButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Sign/Verify", None))
        self.label.setText(_translate("Dialog", "Message", None))
        self.addressEdit.setPlaceholderText(_translate("Dialog", "Address", None))
        self.label_2.setText(_translate("Dialog", "Signature", None))
        self.signButton.setText(_translate("Dialog", "Sign", None))
        self.verifyButton.setText(_translate("Dialog", "Verify", None))
        self.closeButton.setText(_translate("Dialog", "Close", None))

