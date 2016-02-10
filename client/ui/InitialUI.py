# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Initial.ui'
#
# Created: Sun May  3 02:11:50 2015
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
        Dialog.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/windowIcon/coinami.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 70, 401, 111))
        font = QtGui.QFont()
        font.setPointSize(48)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet(_fromUtf8("QLabel {\n"
"qproperty-alignment: AlignCenter;\n"
" color : #e5c100;}"))
        self.label.setMargin(4)
        self.label.setObjectName(_fromUtf8("label"))
        self.situationText = QtGui.QLabel(Dialog)
        self.situationText.setGeometry(QtCore.QRect(0, 180, 401, 111))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.situationText.setFont(font)
        self.situationText.setStyleSheet(_fromUtf8("QLabel {qproperty-alignment: AlignCenter;}"))
        self.situationText.setMargin(4)
        self.situationText.setObjectName(_fromUtf8("situationText"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Starting Client", None))
        self.label.setText(_translate("Dialog", "Coinami", None))
        self.situationText.setText(_translate("Dialog", "Starting Database", None))

import icons_rc
