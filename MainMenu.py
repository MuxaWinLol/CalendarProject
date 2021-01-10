import sys
import sqlite3
from datetime import datetime

import plyer
import simpleaudio
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication

from noti import fileout
from noti import DialogNoti
from alarm import DialogAlarm
from settings import DialogSettings


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.setWindowTitle("Calendar - главное меню")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.pushButton.clicked.connect(self.create_noti)
        self.flag = True
        self.notusedbutton = True
        self.pushButton_2.clicked.connect(self.create_alarm)
        self.pushButton_4.clicked.connect(self.stopbutton)
        self.pushButton_4.setEnabled(False)
        self.pushButton_4.setVisible(False)
        self.pushButton_5.clicked.connect(self.create_settings)
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
                    self.trigger_noti(tmp[1].strip())
                else:
                    lst.append(i)
        fileout("notis.txt", lst)

    def trigger_noti(self, name):
        plyer.notification.notify(message=name, app_name='Calendar', title='Напоминание')

    def create_alarm(self):
        self.dalarm = DialogAlarm()
        self.dalarm.show()

    def update_alarm(self):
        time = datetime.now().strftime("%H:%M")
        day = datetime.weekday(datetime.now())
        con = sqlite3.connect("alarms.sqlite")
        cur = con.cursor()
        if self.notusedbutton:
            for i in cur.execute("""SELECT name, time, days, ringpath FROM alarms""").fetchall():
                if i[2][1:][day] == "1" and time == i[1]:
                    if self.flag:
                        self.trigger_alarm(i[0], i[3])
                        self.flag = False
                        self.pushButton_4.setEnabled(True)
                        self.pushButton_4.setVisible(True)
                else:
                    self.notusedbutton = True
                    self.pushButton_4.setEnabled(False)
        else:
            self.pushButton_4.setVisible(False)
        con.close()

    def trigger_alarm(self, name, pth):
        self.notusedbutton = True
        self.trigger_noti(str(name))
        wave = simpleaudio.WaveObject.from_wave_file(pth)
        wave.play()
        self.flag = True

    def upd(self):
        self.update_noti()
        self.update_alarm()

    def stopbutton(self):
        self.notusedbutton = False
        self.pushButton_4.setEnabled(False)
        self.pushButton_4.setVisible(False)

    def create_settings(self):
        self.dsettings = DialogSettings()
        self.dsettings.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
