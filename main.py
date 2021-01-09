from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from noti import DialogNoti, fileout
from datetime import datetime
from PyQt5 import QtGui
from PyQt5 import uic
import plyer
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.setWindowTitle("Calendar - главное меню")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.pushButton.clicked.connect(self.create_noti)
        t = QTimer(self)
        t.timeout.connect(self.upd)
        t.start(1000)

    def create_noti(self):
        self.dnoti = DialogNoti()
        self.dnoti.show()

    def update_noti(self):
        time = datetime.now().strftime("%Y/%m/%d %H:%M")
        lst = []
        with open("notis.txt", "r", encoding="UTF-8") as fl:
            for i in [i.strip() for i in fl.readlines() if i.strip()]:
                tmp = i.split("-")
                if tmp[0].strip() <= time:
                    plyer.notification.notify(message=tmp[1].strip(), app_name='Calendar', title='Напоминание')
                else:
                    lst.append(i)
        fileout("notis.txt", lst)

    def upd(self):
        self.update_noti()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())