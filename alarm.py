import sys
import sqlite3

from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication


class DialogAlarm(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('alarm.ui', self)
        self.setWindowTitle("Calendar - управление будильниками")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.pushButton.clicked.connect(self.res)
        self.pushButton_2.clicked.connect(self.get_file)
        self.buttonBox.accepted.connect(self.save)

        [i.clicked.connect(self.run) for i in (self.radioButton_8, self.radioButton_9)]
        self.btns = [self.radioButton, self.radioButton_2, self.radioButton_3,
                     self.radioButton_4, self.radioButton_5, self.radioButton_6, self.radioButton_7]
        self.pth = ""
        with open("settings.txt", "r", encoding="UTF-8") as f:
            self.defaultpth = f.read()

        if self.defaultpth:
            self.flag = True
            self.pushButton_2.setEnabled(False)
            self.radioButton_8.setChecked(True)
        else:
            self.flag = False
            self.radioButton_9.setChecked(True)
            self.radioButton_8.setEnabled(False)
        if not self.flag and not self.pth:
            self.pushButton.setEnabled(False)
        self.model = QtGui.QStandardItemModel()
        self.listView.setModel(self.model)
        con = sqlite3.connect("alarms.sqlite")
        cur = con.cursor()
        tmp = cur.execute("""SELECT name, time, days, ringpath FROM alarms WHERE TRUE """).fetchall()
        self.lst = [f"{i[0]} - {i[1]} - {i[2]} - {i[3]}" for i in tmp]
        self.upd()
        con.close()

    def run(self):
        if self.radioButton_8.isChecked():
            self.flag = True
            self.pushButton_2.setEnabled(False)
            self.pushButton.setEnabled(True)
        elif self.radioButton_9.isChecked():
            self.flag = False
            self.pushButton_2.setEnabled(True)
            if not self.pth:
                self.pushButton.setEnabled(False)

    def get_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Music files (*.mp3 *.ogg *.wav)")[0]
        if fname:
            self.pth = fname
            self.pushButton.setEnabled(True)

    def res(self):
        self.lst.append(f"{self.lineEdit.text()} - {self.timeEdit.text().rjust(5, '0')} - "
                        f"b{''.join(['1' if i.isChecked() else '0' for i in self.btns])}"
                        f" - {self.pth if not self.flag else self.defaultpth}")

        self.upd()

    def upd(self):
        ind = self.listView.selectedIndexes()
        self.lst.sort(reverse=True)
        self.model.clear()
        for i in self.lst:
            self.model.appendRow(QtGui.QStandardItem(i))

    def save(self):
        con = sqlite3.connect("alarms.sqlite")
        cur = con.cursor()
        cur.execute("""DELETE FROM alarms""")
        con.commit()
        for i in range(len(self.lst)):
            tmp = self.lst[i].split(" - ")
            cur.execute("""INSERT INTO alarms (name, time, days, ringpath) 
            VALUES ('{}', '{}', '{}', '{}')""".format(tmp[0], tmp[1], tmp[2], tmp[3]))
            con.commit()
        con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DialogAlarm()
    ex.show()
    sys.exit(app.exec_())
