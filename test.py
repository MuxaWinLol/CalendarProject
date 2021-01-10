import requests
import json
import geocoder

g = str(geocoder.ip('me')[0]).replace("[", "").replace("]", "").split(", ")
print(g)
city = input("Название города: ")
cityid = None

with open("city.list.json", "r", encoding="UTF-8") as fl:
    data = json.load(fl)

for i in data:
    if i["coord"] == city:
        cityid = i["id"]

if cityid:
    print(cityid)
    api_key = "c899646d34325b3b9d8b1f18e564256a"
    url = f"http://www.openweathermap.org/data/2.5/weather?appid={api_key}&id={city}"
    json_data = requests.get(url).json()
    print(json_data)
else:
    print("Неправильно введено название города.")
