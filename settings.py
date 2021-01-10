import sys
import json

import geocoder
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication


class DialogSettings(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('settings.ui', self)
        self.setWindowTitle("Calendar - настройки")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))

        self.pth = ""
        self.starttext = ""
        self.set_init_data()

        self.pushButton.clicked.connect(self.get_file)
        self.pushButton_2.clicked.connect(self.get_location)
        self.pushButton_3.clicked.connect(self.islocvalid)
        self.lineEdit_3.setEnabled(False)
        self.buttonBox.accepted.connect(self.save)
        self.lineEdit.textChanged.connect(self.upd)
        self.lineEdit_2.textChanged.connect(self.upd)

    def set_init_data(self):
        with open("settings.txt", "r", encoding="UTF-8") as fl:
            rlns = fl.readlines()
        if len(rlns) == 2:
            self.starttext = rlns[1]
            self.pth = rlns[0].strip()
            self.lineEdit_3.setText(f"\t\tВыбранный файл:   {self.pth}")
            loc = self.starttext.strip().split(",")
            if loc[0] and loc[1]:
                self.lineEdit.setText(loc[0])
                self.lineEdit_2.setText(loc[1])

    def get_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Music files (*.mp3 *.ogg *.wav)")[0]
        if fname:
            self.pth = fname
            self.lineEdit_3.setText(f"\t\tВыбранный файл:   {self.pth}")

    def get_location(self):
        g = str(geocoder.ip('me')[0])[1:-1].split(", ")
        self.lineEdit.setText(g[1])
        self.lineEdit_2.setText(g[2])
        self.label_5.setText("")

    def save(self):
        with open("settings.txt", "w+", encoding="UTF-8") as fl:
            print(self.pth, f"{self.lineEdit.text()},{self.lineEdit_2.text()}", sep="\n", file=fl)

    def islocvalid(self):
        with open("city.list.json", "r", encoding="UTF-8") as fl:
            data = json.load(fl)

        city = self.lineEdit.text().capitalize()
        country = self.lineEdit_2.text().upper()

        for i in data:
            if i["name"] == city and i["country"] == country:
                self.lineEdit.setText(city)
                self.lineEdit_2.setText(country)
                self.buttonBox.setEnabled(True)
                break
        else:
            self.buttonBox.setEnabled(False)
            self.label_5.setText("Локация введена некорректно.")

    def upd(self):
        self.label_5.setText("")
        if self.starttext != f"{self.lineEdit.text().capitalize()},{self.lineEdit_2.text().upper()}":
            self.buttonBox.setEnabled(False)
        else:
            self.buttonBox.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DialogSettings()
    ex.show()
    sys.exit(app.exec_())
