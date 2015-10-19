#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import required module
import sys
import time
from PySide.QtGui import *

global myApp

class SampleWindow(QWidget):
    """ Our main window class
    """

    # Constructor function
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle(u'翼龙贷自动投标')
        self.setGeometry(300, 300, 800, 600)

        QToolTip.setFont(QFont("Decorative", 8, QFont.Bold))
        self.setToolTip('Our main window')

    def setIcon(self):
        """ Function to set Icon
        """
        appIcon = QIcon('eloancn_logo.png')
        self.setWindowIcon(appIcon)

    def setInputWidget(self):
        self.myNameButton = QPushButton(u'用户名', self)
        self.myLoginPasswdButton = QPushButton(u'登录密码', self)
        self.myPayPasswdButton = QPushButton(u'支付密码', self)
        self.myMonthButton = QPushButton(u'月数<=', self)
        self.myRateButton = QPushButton(u'利率>=', self)

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
        self.setGeometry(400, 400, 400, 400)
        #self.setWindowTitle(u'翼龙贷自动投标')
        self.show()

    def quitApp(self):
        global myApp
        userInfo = QMessageBox.question(self, 'Confirmation',
                    "This will quit the application. Do you want to continue?",
                        QMessageBox.Yes | QMessageBox.No)
        if userInfo == QMessageBox.Yes:
            myApp.quit()
        else:
            pass

    def setButton(self):
        myButton = QPushButton('Quit', self)
        myButton.move(50, 100)
        myButton.clicked.connect(self.quitApp)

    def center(self):
        qRect = self.frameGeometry()
        conterPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

if __name__ == '__main__':
    global myApp
    # Exception Handling
    try:
        myApp = QApplication(sys.argv)
        myWindow = SampleWindow()
        myWindow.setIcon()
        myWindow.setInputWidget()
        #myWindow.setIconModes()
        #myWindow.setButton()
        myWindow.show()
        myApp.exec_()
        sys.exit(0)
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window...")
    except Exception:
        print(sys.exc_info()[1])
