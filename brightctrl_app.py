import sys, os
from PyQt5.QtWidgets import QApplication
from gui.app_mw import AppMainWindow
from PyQt5.QtWinExtras import QtWin
import logging

app = QApplication(sys.argv)
app_real_path = os.path.realpath(sys.argv[0])
logging.basicConfig(level=logging.INFO, format='%(asctime)s = %(name)s - %(levelname)s : %(message)s')

if __name__ == "__main__":
    logging.info("APP: %s"%app_real_path)
    mw = AppMainWindow()
    mw.show()
    retcode = app.exec_()
    logging.info("App is end, good bye.")
    sys.exit(retcode)
    
