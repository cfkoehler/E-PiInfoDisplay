from datetime import datetime
from openWeather import openWeather

weather = openWeather("9501f50b9b1cf893fd7bb895171e7fce", 39.1626, -76.6247, "imperial")
currentWeather = weather.current()
dailyWeather = weather.dailyForcast()


sunrise = datetime.fromtimestamp(currentWeather['sunrise'])
sunset = datetime.fromtimestamp(currentWeather['sunset'])
print(sunset)