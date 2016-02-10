# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BlockInfo.ui'
#
# Created: Sun May  3 01:51:30 2015
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
        Dialog.resize(1013, 456)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 111, 18))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 111, 18))
        self.label_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 111, 18))
        self.label_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 100, 111, 18))
        self.label_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 130, 111, 18))
        self.label_5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.timeText = QtGui.QLabel(Dialog)
        self.timeText.setGeometry(QtCore.QRect(140, 70, 111, 18))
        self.timeText.setFocusPolicy(QtCore.Qt.NoFocus)
        self.timeText.setObjectName(_fromUtf8("timeText"))
        self.minerText = QtGui.QLabel(Dialog)
        self.minerText.setGeometry(QtCore.QRect(140, 40, 851, 18))
        self.minerText.setFocusPolicy(QtCore.Qt.NoFocus)
        self.minerText.setObjectName(_fromUtf8("minerText"))
        self.blocknumberText = QtGui.QLabel(Dialog)
        self.blocknumberText.setGeometry(QtCore.QRect(140, 10, 851, 18))
        self.blocknumberText.setObjectName(_fromUtf8("blocknumberText"))
        self.authText = QtGui.QLabel(Dialog)
        self.authText.setGeometry(QtCore.QRect(140, 100, 851, 18))
        self.authText.setFocusPolicy(QtCore.Qt.NoFocus)
        self.authText.setObjectName(_fromUtf8("authText"))
        self.txTable = QtGui.QTableView(Dialog)
        self.txTable.setGeometry(QtCore.QRect(10, 160, 991, 291))
        self.txTable.setObjectName(_fromUtf8("txTable"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Block Info", None))
        self.label.setText(_translate("Dialog", "Block Number", None))
        self.label_2.setText(_translate("Dialog", "Miner", None))
        self.label_3.setText(_translate("Dialog", "Time", None))
        self.label_4.setText(_translate("Dialog", "Signing Authority", None))
        self.label_5.setText(_translate("Dialog", "Transactions", None))
        self.timeText.setText(_translate("Dialog", "Time", None))
        self.minerText.setText(_translate("Dialog", "Miner", None))
        self.blocknumberText.setText(_translate("Dialog", "Block Number", None))
        self.authText.setText(_translate("Dialog", "Signing Authority", None))

