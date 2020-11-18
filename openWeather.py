#Class to connect and manage OpenWeatherMap connection
import requests
from datetime import datetime

class openWeather:

	def __init__(self, api, lat, lon, units):
		self.api = api
		self.lon = lon
		self.lat = lat
		self.units = units
		self.weather = self.getForcast()

	def getForcast(self):
		url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units={}&appid={}".format(self.lat, self.lon, self.units, self.api)
		r = requests.get(url)
		weather = r.json()
		return(weather)
	
	def hourlyForcast(self):
		hourly = []
		for i in self.weather['hourly']:
			ts = i['dt']
			time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
			temp = i['temp']
			hum = i['humidity']
			cond = i['weather'][0]['description']
			#print(time + "|" + "temp:" + str(temp) + "|" + "cond:" + cond)
			hourly.append([time,temp,hum,cond])
		return hourly

	def dailyForcast(self):
		daily = []
		for i in self.weather['daily']:
			time = datetime.utcfromtimestamp(i['dt'])
			sunrise = datetime.utcfromtimestamp(i['sunrise']).strftime('%Y-%m-%d %H:%M:%S')
			sunset = datetime.utcfromtimestamp(i['sunset']).strftime('%Y-%m-%d %H:%M:%S')
			temp = i['temp']
			hum = i['humidity']
			main = i['weather'][0]['main']
			description = i['weather'][0]['description']
			icon = i['weather'][0]['icon']
			daily.append([time,sunrise,sunset,temp,hum,main,description,icon])
		return(daily)
	
	def current(self):
		return(self.weather['current'])