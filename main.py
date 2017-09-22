from PyQt5 import QtWidgets
import sys
from windows.main import Window

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec_()
    sys.exit(0)
