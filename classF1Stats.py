import requests
import xmltodict
from datetime import datetime

def getChampionship():
    url = "http://ergast.com/api/f1/current/driverStandings"
    response = requests.get(url)
    dict = xmltodict.parse(response.content)
    championship = {}
    
    for driver in dict['MRData']['StandingsTable']['StandingsList']['DriverStanding']:
        racer = {}
        racer['name'] = driver['Driver']['FamilyName']
        racer['team'] = driver['Constructor']['Name']
        racer['points'] = driver['@points']
        championship[driver['@position']] = racer

    return championship

def getSeason(year):
    url = "https://ergast.com/api/f1/{}".format(year)
    response = requests.get(url)
    dict = xmltodict.parse(response.content)
    season = {}
    for race in dict['MRData']['RaceTable']['Race']:
        raceStat = {}
        raceStat['round'] = race['@round']
        raceStat['name'] = race['RaceName']
        raceStat['country'] = race['Circuit']['Location']['Country']
        raceStat['date'] = race['Date']
        season[raceStat['round']] = raceStat

    return season

def getNextRace():
    todays_date = datetime.today()
    season = getSeason(datetime.today().year)

    #For each race check if it is the next one 
    for race in season:
        date = datetime.strptime(season[race]['date'], '%Y-%m-%d')
        if date == todays_date or date > todays_date:
            return(season[race])
        else:
            return {}
