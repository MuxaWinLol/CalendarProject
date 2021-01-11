from datetime import datetime

from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog


class DialogNoti(QDialog):
    def __init__(self):
        # Инициализация класса
        super().__init__()
        uic.loadUi('CreateNotiDialog.ui', self)
        self.setWindowTitle("Calendar - управление напоминаниями")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))

        self.model = QtGui.QStandardItemModel()
        self.listView.setModel(self.model)
        self.pushButton.clicked.connect(self.run)
        self.buttonBox.accepted.connect(self.save)

        self.lst = []

        self.set_init_data()
        self.upd()

    def set_init_data(self):
        # Добавляет к списку self.lst все уведомления из файла notis.txt
        with open("notis.txt", "r", encoding="UTF-8") as fl:
            self.lst = [i.strip() for i in fl.readlines() if i.strip()]

    def run(self):
        # Добавляет уведомление в список self.lst, если дата еще не прошла
        now = datetime.now().strftime("%Y/%m/%d %H:%M")
        inp = f"{self.calendarWidget.selectedDate().toString('yyyy/MM/dd')} {self.timeEdit.text().rjust(5, '0')}"
        if now < inp:
            self.lst.append(f"{inp} - {self.lineEdit.text()}")
            self.label_2.setText("")
            self.upd()
        else:
            self.label_2.setText("Эта дата уже прошла.")

    def upd(self):
        # Обновляет виджет listView
        self.lst.sort()
        self.model.clear()
        for i in self.lst:
            self.model.appendRow(QtGui.QStandardItem(i))

    def save(self):
        # Сохраняет изменения в файл
        fileout("notis.txt", self.lst)


def fileout(filename, lst):
    # Очищает файл filename и записывает в него информацию из списка lst
    with open(filename, "w+", encoding="UTF-8") as fl:
        print(*lst, sep="\n", file=fl)
