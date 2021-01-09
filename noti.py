from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from datetime import datetime
from PyQt5 import QtGui
from PyQt5 import uic
import sys


class DialogNoti(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('CreateNotiDialog.ui', self)
        self.setWindowTitle("Calendar - управление напоминаниями")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.model = QtGui.QStandardItemModel()
        self.listView.setModel(self.model)
        self.pushButton.clicked.connect(self.run)
        self.finished.connect(self.save)
        with open("notis.txt", "r", encoding="UTF-8") as fl:
            self.lst = [i.strip() for i in fl.readlines() if i.strip()]
            self.upd()

    def run(self):
        now = datetime.now().strftime("%Y/%m/%d %H:%M")
        inp = f"{self.calendarWidget.selectedDate().toString('yyyy/MM/dd')} {self.timeEdit.text().rjust(5, '0')}"
        if now < inp:
            self.lst.append(f"{inp} - {self.lineEdit.text()}")
            self.label_2.setText("")
            self.upd()
        else:
            self.label_2.setText("Эта дата уже прошла.")

    def upd(self):
        self.lst.sort()
        self.model.clear()
        for i in self.lst:
            self.model.appendRow(QtGui.QStandardItem(i))

    def save(self):
        fileout("notis.txt", self.lst)


def fileout(filename, lst):
    open(filename, "w").close()
    with open(filename, "w", encoding="UTF-8") as fl:
        print(*lst, sep="\n", file=fl)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DialogNoti()
    ex.show()
    sys.exit(app.exec_())