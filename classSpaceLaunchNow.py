import requests
import json
import datetime as dt
from dateutil import tz


def getSpaceLaunchs():
    jsonRaw = getData()
    reported = []
    
    if len(jsonRaw) == 0:
        return(reported)

    #for each of the first 10 results get name, launch date, country/agency
    for x in range(10):
        name = jsonRaw['results'][x]['name']
        date = jsonRaw['results'][x]['net']
        date = dt.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
        # Convert date to local
        #date = date.replace(tzinfo=tz.gettz('UTC'))
        date = date.astimezone(tz.tzlocal())
        reported.append([name, date])

    return(reported)

    

def getData(): 
    try:
        response = requests.get("https://spacelaunchnow.me/api/3.3.0/launch/upcoming/?format=json")
        response.raise_for_status()
        json = response.json()
        return json
    except:
        return []

