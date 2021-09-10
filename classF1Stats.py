import requests
import xmltodict

class f1Data:
    def __init__(self):
        championship = self.getChampionship()
        nextRace = self.getNextRace()
    
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