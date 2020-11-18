from openWeather import openWeather

api_key = "9501f50b9b1cf893fd7bb895171e7fce"
location = "Glen Burnie, US"
lat = 39.1626
lon = -76.6247
weather = openWeather(api_key, lat, lon, "imperial")
#print(weather.hourlyForcast())
daily = weather.dailyForcast()

print(daily[0][3]['min'])
current = weather.current()
print(current['temp'])