import requests
from datetime import datetime

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from translate import Translator
from PyQt5.QtWidgets import QDialog


class DialogWeather(QDialog):
    def __init__(self):
        # Инициализация класса
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Calendar - погода")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.reloadButton.clicked.connect(self.make_request)

        self.api_key = "c899646d34325b3b9d8b1f18e564256a"
        self.url_now = ""
        self.data_now = ""
        self.url_fc = ""
        self.data_fc = ""

        self.make_request()

    def make_request(self):
        # Запрос данных из openweathermap api
        with open("settings.txt", "r", encoding="UTF-8") as fl:
            tmp = fl.readlines()
            if len(tmp) == 2:
                loc = tmp[1].strip()
            else:
                self.close()

        self.label.setText(f'Город: {loc.replace(",", ", ")}')
        self.url_now = f"http://api.openweathermap.org/data/2.5/weather?q={loc}&APPID={self.api_key}&units=metric"
        self.url_fc = f"http://api.openweathermap.org/data/2.5/forecast?q={loc}&APPID={self.api_key}&units=metric"
        self.data_now = requests.get(self.url_now).json()
        self.data_fc = requests.get(self.url_fc).json()["list"]

        self.init_weather()

    def init_weather(self):
        # Вставка запрошенных данных в соответствующие поля
        self.sunrise.setText(f'Рассвет: {timestamp_to_time(self.data_now["sys"]["sunrise"])}')
        self.sunset.setText(f'Закат: {timestamp_to_time(self.data_now["sys"]["sunset"])}')
        self.lat.setText(f'Широта: {self.data_now["coord"]["lat"]}')
        self.long.setText(f'Долгота: {self.data_now["coord"]["lon"]}')
        self.temp_now.setText(f'Темпрература: {self.data_now["main"]["temp"]}°C')
        self.pres_now.setText(f'Давление: {pascal_to_mmhg(self.data_now["main"]["pressure"])}')
        self.hum_now.setText(f'Влажность: {self.data_now["main"]["humidity"]}%')
        self.speed.setText(f'Скорость: {self.data_now["wind"]["speed"]} м/с')
        self.direction.setText(f'Направление: {deg_to_dir(self.data_now["wind"]["deg"])}')
        self.label_7.setPixmap(QtGui.QPixmap(r"images/" + self.data_now["weather"][0]["icon"]))
        translator = Translator(to_lang="ru")
        translation = translator.translate(self.data_now["weather"][0]["description"].capitalize())
        self.label_8.setText(translation)

        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)

        for n, forecast in enumerate(self.data_fc[:8], 1):
            lbltime = QtWidgets.QLabel()
            lbltime.setText(timestamp_to_time(forecast["dt"]))

            lblicon = QtWidgets.QLabel()
            lblicon.setPixmap(QtGui.QPixmap(r"images/" + forecast["weather"][0]["icon"]))
            lblicon.setScaledContents(True)

            lbltemp = QtWidgets.QLabel()
            lbltemp.setText("%.1f°C" % forecast['main']['temp'])

            lblwindicon = QtWidgets.QLabel()
            lblwindicon.setPixmap(QtGui.QPixmap(r"images/wind.png"))
            lblwindicon.setScaledContents(True)

            lblwindspeed = QtWidgets.QLabel()
            lblwindspeed.setText(f' {int(forecast["wind"]["speed"])} м/с')

            lblvoid = QtWidgets.QLabel()
            lblvoid.setText("                   ")

            self.gridLayout.addWidget(lbltime, 1, 2 * n, 1, 1)
            self.gridLayout.addWidget(lblicon, 2, 2 * n, 1, 1)
            self.gridLayout.addWidget(lbltemp, 3, 2 * n, 1, 1)
            self.gridLayout.addWidget(lblwindicon, 4, 2 * n, 1, 1)
            self.gridLayout.addWidget(lblwindspeed, 5, 2 * n, 1, 1)
            self.gridLayout.addWidget(lblvoid, 1, 2 * n + 1, 1, 1)

    def setupUi(self, Dialog):

        Dialog.setObjectName("Dialog")
        Dialog.resize(904, 335)
        self.reloadButton = QtWidgets.QPushButton(Dialog)
        self.reloadButton.setGeometry(QtCore.QRect(855, 10, 30, 30))
        self.reloadButton.setIcon(QtGui.QIcon(r"images/reload.png"))
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(420, 10, 131, 20))
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 220, 861, 101))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(370, 80, 160, 80))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.direction = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.direction.setObjectName("direction")
        self.gridLayout_2.addWidget(self.direction, 2, 0, 1, 1)
        self.speed = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.speed.setObjectName("speed")
        self.gridLayout_2.addWidget(self.speed, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(350, 50, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(600, 50, 131, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(560, 80, 160, 80))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 1)
        self.long = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.long.setObjectName("long")
        self.gridLayout_3.addWidget(self.long, 2, 0, 1, 1)
        self.lat = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.lat.setObjectName("lat")
        self.gridLayout_3.addWidget(self.lat, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(140, 50, 131, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(150, 80, 160, 80))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.temp_now = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.temp_now.setObjectName("temp_now")
        self.gridLayout_4.addWidget(self.temp_now, 1, 0, 1, 1)
        self.hum_now = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.hum_now.setObjectName("hum_now")
        self.gridLayout_4.addWidget(self.hum_now, 2, 0, 1, 1)
        self.pres_now = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.pres_now.setObjectName("pres_now")
        self.gridLayout_4.addWidget(self.pres_now, 3, 0, 1, 1)
        self.gridLayoutWidget_5 = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget_5.setGeometry(QtCore.QRect(720, 80, 160, 80))
        self.gridLayoutWidget_5.setObjectName("gridLayoutWidget_5")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.gridLayoutWidget_5)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.sunset = QtWidgets.QLabel(self.gridLayoutWidget_5)
        self.sunset.setObjectName("sunset")
        self.gridLayout_5.addWidget(self.sunset, 2, 0, 1, 1)
        self.sunrise = QtWidgets.QLabel(self.gridLayoutWidget_5)
        self.sunrise.setObjectName("sunrise")
        self.gridLayout_5.addWidget(self.sunrise, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(360, 190, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(45, 109, 41, 41))
        self.label_7.setText("")
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(15, 79, 101, 21))
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.direction.setText(_translate("Dialog", "Направление: "))
        self.speed.setText(_translate("Dialog", "Скорость: "))
        self.label_2.setText(_translate("Dialog",
                                        "<html><head/><body><p align=\"center\"><span style=\""
                                        " font-size:12pt; font-weight:600; font-style:italic;\">"
                                        "Ветер</span></p></body></html>"))
        self.label_5.setText(_translate("Dialog",
                                        "<html><head/><body><p align=\"center\"><span style=\""
                                        " font-size:12pt; font-weight:600; font-style:italic;\">"
                                        "Локация</span></p></body></html>"))
        self.long.setText(_translate("Dialog", "Долгота: "))
        self.lat.setText(_translate("Dialog", "Широта: "))
        self.label_4.setText(_translate("Dialog",
                                        "<html><head/><body><p align=\"center\"><span style=\""
                                        " font-size:12pt; font-weight:600; font-style:italic;\">"
                                        "Воздух</span></p></body></html>"))
        self.temp_now.setText(_translate("Dialog", "Температура: "))
        self.hum_now.setText(_translate("Dialog", "Влажность: "))
        self.pres_now.setText(_translate("Dialog", "Давление: "))
        self.sunset.setText(_translate("Dialog", "Закат: "))
        self.sunrise.setText(_translate("Dialog", "Рассвет: "))
        self.label_6.setText(_translate("Dialog",
                                        "<html><head/><body><p align=\"center\"><span style=\""
                                        " font-size:12pt; font-weight:600; font-style:italic;\">"
                                        "Прогноз погоды</span></p></body></html>"))


def timestamp_to_time(ts):
    # Перевод из таймстампа во время дня
    dt = datetime.fromtimestamp(ts).strftime("%H:00")
    return dt


def pascal_to_mmhg(pascals):
    # Перевод из Паскалей в миллиметры от ртутного столба
    mmhg = pascals / 1.33
    return f"{int(mmhg)} мм рт. ст."


def deg_to_dir(deg):
    # Перевод угла направления ветра в сторону света
    d = {0: "В",
         1: "СВ",
         2: "С",
         3: "СЗ",
         4: "З",
         5: "ЮЗ",
         6: "Ю",
         7: "ЮВ",
         8: "В"}
    tmp = deg // 45
    c1 = abs(deg - tmp)
    c2 = abs(deg - tmp + 1)
    if c1 < c2:
        ans = d[tmp]
    else:
        ans = d[tmp + 1]
    return ans
