import requests
import json
import datetime as dt


def getSpaceLaunchs():
    jsonRaw = getData()
    results = jsonRaw['results']
    reported = []

    #for each of the first 5 results get name, launch date, country/agency
    for x in range(10):
        #print(jsonRaw['results'][x]['name'])
        #print(jsonRaw['results'][x]['window_start'])
        #print[jsonRaw['results'][x]['pad']['location']['country_code']]
        name = jsonRaw['results'][x]['name']
        date = jsonRaw['results'][x]['net']
        date = dt.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
        reported.append([name, date])

    return(reported)

    

def getData(): 
    response = requests.get("https://spacelaunchnow.me/api/3.3.0/launch/upcoming/?format=json")
    response.raise_for_status()
    json = response.json()
    return json

def processData():
    return null
