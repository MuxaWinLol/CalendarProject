from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QInputDialog


class TimerDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('timer.ui', self)
        self.setWindowTitle("Calendar - управление напоминаниями")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))

        self.cnt = 0
        self.fl = False
        self.lcdNumber.setDigitCount(12)
        self.lcdNumber.display("0:00:00.00")

        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.reset)
        self.pushButton_3.clicked.connect(self.set_seconds)

        # Установка таймера
        t = QTimer(self)
        t.timeout.connect(self.updatee)
        t.start(10)

    def updatee(self):
        if self.fl:
            self.cnt -= 1
            if self.cnt == -1:
                self.fl = False
                return
            self.lcdNumber.display(self.sec_to_clock(self.cnt / 100))

    def set_seconds(self):
        self.fl = False
        inp, done = QInputDialog.getInt(self, 'Time', 'Time in seconds:')
        if done:
            self.cnt = inp * 100
            self.lcdNumber.display(self.sec_to_clock(inp))

    def start(self):
        if not self.fl:
            if self.cnt != -1:
                self.pushButton.setText("Pause")
                self.fl = True
                return
            self.pushButton.setText("Start")
            return
        print(1)
        self.pushButton.setText("Start")
        self.fl = False

    def reset(self):
        self.fl = False
        self.cnt = -1
        self.pushButton.setText("Start")
        self.lcdNumber.display("0:00:00.00")

    def sec_to_clock(self, xx):
        min = int(xx // 60 % 60)
        hrs = int(xx // 360)
        sec = int(xx % 60)
        mis = int(xx % 1 * 100)
        return f"{hrs}:{str(min).rjust(2, '0')}:{str(sec).rjust(2, '0')}.{str(mis).ljust(2, '0')}"
