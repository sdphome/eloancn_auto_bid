#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PySide.QtGui import *


class MyInputDialog(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.myNameButton = QPushButton(u'用户名', self)
        self.myNameButton.clicked.connect(self.showNameDialog)

        self.myLoginPasswdButton = QPushButton(u'登录密码', self)
        self.myLoginPasswdButton.clicked.connect(self.showLoginPasswdDialog)

        self.myPayPasswdButton = QPushButton(u'支付密码', self)
        self.myPayPasswdButton.clicked.connect(self.showPayPasswdDialog)

        self.myMonthButton = QPushButton(u'月数<=', self)
        self.myMonthButton.clicked.connect(self.showMonthDialog)

        self.myRateButton = QPushButton(u'利率>=', self)
        self.myRateButton.clicked.connect(self.showRateDialog)

        self.myNameLE = QLineEdit(self)
        self.myLoginPasswdLE = QLineEdit(self)
        self.myPayPasswdLE = QLineEdit(self)
        self.myMonthLE = QLineEdit(self)
        self.myRateLE = QLineEdit(self)

        self.myLayout = QFormLayout()
        self.myLayout.addRow(self.myNameButton, self.myNameLE)
        self.myLayout.addRow(self.myLoginPasswdButton, self.myLoginPasswdLE)
        self.myLayout.addRow(self.myPayPasswdButton, self.myPayPasswdLE)
        self.myLayout.addRow(self.myMonthButton, self.myMonthLE)
        self.myLayout.addRow(self.myRateButton, self.myRateLE)

        self.setLayout(self.myLayout)
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle(u'翼龙贷自动投标')
        self.show()

    def showNameDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Text Dialog',
                                        u'输入你的用户名:')
        if ok:
            self.myNameLE.setText(str(text))

    def showLoginPasswdDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Text Dialog',
                                        u'输入登录密码:')
        if ok:
            self.myLoginPasswdLE.setText(str(text))

    def showPayPasswdDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Text Dialog',
                                        u'输入支付密码:')
        if ok:
            self.myPayPasswdLE.setText(str(text))

    def showMonthDialog(self):
        text, ok = QInputDialog.getInteger(self, 'Input Number Dialog',
                                           u'输入最大投资的月数:')
        if ok:
            self.myMonthLE.setText(str(text))


    def showRateDialog(self):
        text, ok = QInputDialog.getInteger(self, 'Input Number Dialog',
                                           u'输入最少的年化收益:')
        if ok:
            self.myRateLE.setText(str(text))

if __name__ == '__main__':
    # Exception Handling
    try:
        myApp = QApplication(sys.argv)
        myID = MyInputDialog()
        myID.show()
        myApp.exec_()
        sys.exit(0)
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window...")
    except Exception:
        print(sys.exc_info()[1])
