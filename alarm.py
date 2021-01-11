import sqlite3

from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog


class DialogAlarm(QDialog):
    def __init__(self):
        # Инициализация класса
        super().__init__()
        uic.loadUi('alarm.ui', self)
        self.setWindowTitle("Calendar - управление будильниками")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))

        self.pushButton.clicked.connect(self.res)
        self.pushButton_2.clicked.connect(self.get_file)
        self.buttonBox.accepted.connect(self.save)
        [i.clicked.connect(self.run) for i in (self.radioButton_8, self.radioButton_9)]
        self.model = QtGui.QStandardItemModel()
        self.listView.setModel(self.model)

        self.btns = [self.radioButton, self.radioButton_2, self.radioButton_3,
                     self.radioButton_4, self.radioButton_5, self.radioButton_6, self.radioButton_7]
        self.lst = []
        self.pth = ""
        self.defaultpth = ""
        self.flag = True

        self.set_init_data()

    def set_init_data(self):
        # Присваивает списку self.lst все будильники из базы данных alarms.sqlite,
        # переменной self.defaultpath -- путь к файлу с рингтоном по умолчанию
        con = sqlite3.connect("alarms.sqlite")
        cur = con.cursor()
        tmp = cur.execute("""SELECT name, time, days, 
                        ringpath FROM alarms WHERE TRUE """).fetchall()
        self.lst = [f"{i[0]} - {i[1]} - {i[2]} - {i[3]}" for i in tmp]
        self.upd()
        con.close()

        with open("settings.txt", "r", encoding="UTF-8") as f:
            self.defaultpth = f.readlines()[0].strip()

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

    def run(self):
        #
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
        # Открывает диалог выбора файла
        fname = QFileDialog.getOpenFileName(self, "Open file",
                                            "c:\\", "Music files (*.mp3 *.ogg *.wav)")[0]
        if fname:
            self.pth = fname
            self.pushButton.setEnabled(True)

    def res(self):
        # Добавляет будильник в список self.lst в формате:
        # {имя} - {время} - {дни действия} - {путь к файлу с рингтоном}
        self.lst.append(f"{self.lineEdit.text()} - {self.timeEdit.text().rjust(5, '0')} - "
                        f"b{''.join(['1' if i.isChecked() else '0' for i in self.btns])}"
                        f" - {self.pth if not self.flag else self.defaultpth}")

        self.upd()

    def upd(self):
        # Обновляет виджет listView
        ind = self.listView.selectedIndexes()
        self.lst.sort(reverse=True)
        self.model.clear()
        for i in self.lst:
            self.model.appendRow(QtGui.QStandardItem(i))

    def save(self):
        # Очищает базу данных alarms.sqlite и записывает в нее информацию из списка self.lst
        con = sqlite3.connect("alarms.sqlite")
        cur = con.cursor()
        cur.execute("""DELETE FROM alarms""")
        con.commit()
        for i in range(len(self.lst)):
            tmp = self.lst[i].split(" - ")
            if self.lst[i]:
                cur.execute("""INSERT INTO alarms (name, time, days, ringpath) 
                VALUES ('{}', '{}', '{}', '{}')""".format(tmp[0], tmp[1], tmp[2], tmp[3]))
                con.commit()
        con.close()

