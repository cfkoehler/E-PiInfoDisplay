import requests
from datetime import datetime

class covidData:

    def __init__(self, state):
        self.covid = self.getData()
        self.state = state
        self.covidState = self.getStateData()

    def getData(self):
        url = "https://api.covidtracking.com/v1/us/current.json"
        r = requests.get(url)
        covid = r.json()
        return(covid)
        
    def currentData(self):
        return self.covid

    def getStateData(self):
        url = "https://api.covidtracking.com/v1/states/" + self.state + "/current.json"
        r = requests.get(url)
        covidState = r.json()
        return(covidState)
    
    def currentStateData(self):
        return self.covidState