from covidData import covidData
from datetime import datetime
import json
import requests

covid = covidData("MD")
covidCurrent = covid.currentData()
covidState = covid.currentStateData()

#print(covidCurrent)
#print(type(covidCurrent))
#print(covidCurrent[0]['date'])

covidDate = covidCurrent[0]['date']
date = datetime.strptime('20201026', '%Y%m%d')
#print(date.month)
#print(date.day)
print(covidCurrent[0]['positive'])

print(covidState)


with open("settings.json", 'r') as f:
    settings = json.load(f)
    print(settings)
    print(type(settings))
    print(settings['covid']['state'])


url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/auto-complete"

querystring = {"region":"US","q":"tesla"}

headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "49d80e2c43mshc0a825d936c18b4p1a8831jsn74673e749708"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)