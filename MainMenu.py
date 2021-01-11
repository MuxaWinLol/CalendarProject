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
from timer import TimerDialog
from weather import DialogWeather
from settings import DialogSettings


class MainWindow(QMainWindow):
    def __init__(self):
        # Инициализация класса
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.setWindowTitle("Calendar - главное меню")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))

        self.pushButton.clicked.connect(self.create_noti)
        self.pushButton_2.clicked.connect(self.create_alarm)
        self.pushButton_4.clicked.connect(self.stopbutton)
        self.pushButton_3.clicked.connect(self.create_weather)
        self.pushButton_5.clicked.connect(self.create_settings)
        self.pushButton_7.clicked.connect(self.create_timer)

        self.flag = True
        self.notusedbutton = True
        self.pushButton_4.setEnabled(False)
        self.pushButton_4.setVisible(False)

        # Установка таймера
        t = QTimer(self)
        t.timeout.connect(self.upd)
        t.start(1000)

    def create_noti(self):
        # Создание диалогового окна управления уведомлениями
        self.dnoti = DialogNoti()
        self.dnoti.show()

    def create_alarm(self):
        # Создает диалоговое окно управления будильниками
        self.dalarm = DialogAlarm()
        self.dalarm.show()

    def create_settings(self):
        # Создает диалоговое окно настроек
        self.dsettings = DialogSettings()
        self.dsettings.show()

    def create_weather(self):
        # Создает диалоговое окно настроек
        self.dweather = DialogWeather()
        self.dweather.show()

    def create_timer(self):
        self.dtimer = TimerDialog()
        self.dtimer.show()

    def upd(self):
        # Главная функция обновления (интервал = 1000 мс)
        self.update_noti()
        self.update_alarm()

    def update_noti(self):
        # Обновление все уведомления из файла notis.txt
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

    def update_alarm(self):
        # Обновление будильников из базы данных alarms.sqlite
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

    def trigger_noti(self, name):
        # Отправляет системное оповещение
        plyer.notification.notify(message=name, app_name='Calendar', title='Напоминание')

    def trigger_alarm(self, name, pth):
        # Вызывает системное оповещение и играет рингтон
        self.notusedbutton = True
        self.trigger_noti(str(name))
        wave = simpleaudio.WaveObject.from_wave_file(pth)
        wave.play()
        self.flag = True

    def stopbutton(self):
        # Останавливает музыку (при переходе на следующий круг)
        self.notusedbutton = False

        self.pushButton_4.setEnabled(False)
        self.pushButton_4.setVisible(False)


if __name__ == '__main__':
    # Создание объекта MainWindow
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
