#!/usr/bin/env python

# Import required module
import sys
import time
from PySide.QtGui import QApplication, QWidget, QLabel, QIcon, QToolTip, QFont, QPushButton, QMessageBox

global myApp

class SampleWindow(QWidget):
    """ Our main window class
    """

    # Constructor function
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Icon Sample")
        self.setGeometry(300, 300, 200, 150)
        self.setMinimumHeight(100)
        self.setMinimumWidth(250)
        self.setMaximumHeight(200)
        self.setMaximumWidth(800)
        QToolTip.setFont(QFont("Decorative", 8, QFont.Bold))
        self.setToolTip('Our main window')

    def setIcon(self):
        """ Function to set Icon
        """
        appIcon = QIcon('eloancn_logo.png')
        self.setWindowIcon(appIcon)

    def setIconModes(self):
        myIcon1 = QIcon('eloancn_logo.png')
        myLabel1 = QLabel('sample', self)
        pixmap1 = myIcon1.pixmap(50, 50, QIcon.Active, QIcon.On)
        myLabel1.setPixmap(pixmap1)
        myLabel1.setToolTip('Active Icon')

        myIcon2 = QIcon('eloancn_logo.png')
        myLabel2 = QLabel('sample', self)
        pixmap2 = myIcon2.pixmap(50, 50, QIcon.Disabled, QIcon.On)
        myLabel2.setPixmap(pixmap2)
        myLabel2.move(50, 0)
        myLabel1.setToolTip('Disabled Icon')

        myIcon3 = QIcon('eloancn_logo.png')
        myLabel3 = QLabel('sample', self)
        pixmap3 = myIcon3.pixmap(50, 50, QIcon.Selected, QIcon.On)
        myLabel3.setPixmap(pixmap3)
        myLabel2.move(100, 0)
        myLabel1.setToolTip('Selected Icon')

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
        myWindow.setIconModes()
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
