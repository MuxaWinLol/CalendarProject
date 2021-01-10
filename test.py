import requests

api_key = "c899646d34325b3b9d8b1f18e564256a"
url = f"http://www.openweathermap.org/data/2.5/weather?appid={api_key}&q={input('City Name: ')}"

json_data = requests.get(url).json()

print(json_data)
