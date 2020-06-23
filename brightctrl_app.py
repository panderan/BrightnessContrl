import sys
from PyQt5.QtWidgets import QApplication
from gui.app_mw import AppMainWindow
from PyQt5.QtWinExtras import QtWin

app = QApplication(sys.argv)

if __name__ == "__main__":
    mw = AppMainWindow()
    mw.show()
    sys.exit(app.exec_())
    
