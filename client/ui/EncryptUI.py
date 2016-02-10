# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Encrypt.ui'
#
# Created: Sun May  3 12:00:52 2015
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
        Dialog.resize(764, 522)
        self.verticalLayoutWidget = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(1, 6, 761, 511))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setMargin(3)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.norEdit = QtGui.QTextEdit(self.verticalLayoutWidget)
        self.norEdit.setObjectName(_fromUtf8("norEdit"))
        self.verticalLayout.addWidget(self.norEdit)
        self.keyEdit = QtGui.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keyEdit.sizePolicy().hasHeightForWidth())
        self.keyEdit.setSizePolicy(sizePolicy)
        self.keyEdit.setObjectName(_fromUtf8("keyEdit"))
        self.verticalLayout.addWidget(self.keyEdit)
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMargin(3)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.encEdit = QtGui.QTextEdit(self.verticalLayoutWidget)
        self.encEdit.setObjectName(_fromUtf8("encEdit"))
        self.verticalLayout.addWidget(self.encEdit)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.encButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.encButton.setObjectName(_fromUtf8("encButton"))
        self.horizontalLayout.addWidget(self.encButton)
        self.decButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.decButton.setObjectName(_fromUtf8("decButton"))
        self.horizontalLayout.addWidget(self.decButton)
        self.closeButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Sign/Verify", None))
        self.label.setText(_translate("Dialog", "Normal Text", None))
        self.keyEdit.setPlaceholderText(_translate("Dialog", "Public Key", None))
        self.label_2.setText(_translate("Dialog", "Encrypted Text", None))
        self.encButton.setText(_translate("Dialog", "Encrypt", None))
        self.decButton.setText(_translate("Dialog", "Decrypt", None))
        self.closeButton.setText(_translate("Dialog", "Close", None))

