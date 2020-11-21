import sys
import os
import json
import requests

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5
import time
import datetime
from PIL import Image,ImageDraw,ImageFont
import traceback
import calendar
import classSpaceLaunchNow as  rocket
from openWeather import openWeather
from covidData import covidData
from classStocks import stockData

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='infoLog.log',
    filemode='w')


def getMonthName(month):
    switcher = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }
    return switcher.get(month, "Invalid Month")

def getDayModifyer(day):
    switcher = {
        1: "st",
        2: "nd",
        3: "rd",
    }
    return switcher.get(day, "th")

def getInternetSpeed():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM internetSpeed ORDER BY time DESC LIMIT 1")
    myresult = mycursor.fetchall()

def stringShort(letters, length):
    if len(letters) <= length:
        return letters
    else:
        return letters[:length-2] + ".."

def padTime(time):
    if time <= 9:
        return "0" + str(time)
    else:
        return str(time)

def refreshDisplay(settings):
    logging.info("Starting Display Refresh")

    font24 = ImageFont.truetype('Font.ttc', 24)
    font18 = ImageFont.truetype('Font.ttc', 18)
    font14 = ImageFont.truetype('Font.ttc', 14)
    font30 = ImageFont.truetype('Font.ttc', 30)
    font80 = ImageFont.truetype('Font.ttc', 80)

    #Get data
    logging.info("Getting Data")
    weekdays = list(calendar.day_name)
    now = datetime.datetime.now()
    weather = openWeather(settings['weather']['api_key'], settings['weather']['city_lat'], settings['weather']['city_lon'], "imperial")
    currentWeather = weather.current()
    dailyWeather = weather.dailyForcast()
    covid = covidData(settings['covid']['state'])
    covidCurrent = covid.currentData()
    covidState = covid.currentStateData()
    covidDate = datetime.datetime.strptime(str(covidCurrent[0]['date']), '%Y%m%d')
    stock = stockData(settings['stocks']['tickers'])
    stockCurrent = stock.returnData()
    stockList = settings['stocks']['tickers'].split()


    #Set up display
    epd = epd7in5.EPD()
    logging.info("Initialize and Clear Display")
    epd.init()
    

    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    draw.line((320, 0, 320, 384), fill = 0) #center line
    draw.line((10, 110, 310, 110), fill = 0) #Line under time/date
    draw.line((10, 300, 310, 300), fill = 0) #Line above roket lauch
    draw.line((330, 165, 630, 165), fill = 0) #Line bellow Weather
    draw.line((330, 280, 630, 280), fill = 0) #Line bellow COVID
    
    #Date and time
    #draw.text((5, 1), now(sunrise.time()) , font = font14, fill = 0)
    draw.text((50, 1), padTime(now.hour) + ":" + padTime(now.minute), font = font80, fill = 0)
    draw.text((10, 75), calendar.day_name[now.weekday()] +  " " + getMonthName(now.month)  + " " + str(now.day) + getDayModifyer(now.day), font = font24, fill = 0)

    #Weather
    draw.text((325, 1), str(round(currentWeather['temp'])) + u"\u00b0", font = font80, fill = 0)
    draw.text((410, 45), stringShort(currentWeather['weather'][0]['description'],18), font = font30, fill = 0)
    draw.text((450, 10), "Low: " + str(round(dailyWeather[0][3]['min'])) + " High: " + str(round(dailyWeather[0][3]['max'])), font = font24, fill = 0)
    #Daily Weather
    draw.text((325, 80), calendar.day_name[dailyWeather[1][0].weekday()] + ": " + dailyWeather[1][6] + " (" + str(round(dailyWeather[1][3]['min'])) + u"\u00b0" + ")", font = font18, fill = 0)
    draw.text((325, 100), calendar.day_name[dailyWeather[2][0].weekday()] + ": " + dailyWeather[2][6] + " (" + str(round(dailyWeather[2][3]['min'])) + u"\u00b0" + ")", font = font18, fill = 0)
    draw.text((325, 120), calendar.day_name[dailyWeather[3][0].weekday()] + ": " + dailyWeather[3][6] + " (" + str(round(dailyWeather[3][3]['min'])) + u"\u00b0" + ")", font = font18, fill = 0)
    draw.text((325, 140), calendar.day_name[dailyWeather[4][0].weekday()] + ": " + dailyWeather[4][6] + " (" + str(round(dailyWeather[4][3]['min'])) + u"\u00b0" + ")", font = font18, fill = 0)

    #Rocket Launches
    launches = rocket.getSpaceLaunchs()
    draw.text((5, 310), stringShort(launches[0][0],40), font = font14, fill = 0)
    draw.text((5, 325), stringShort(launches[1][0],40), font = font14, fill = 0)
    draw.text((5, 340), stringShort(launches[2][0],40), font = font14, fill = 0)
    draw.text((5, 355), stringShort(launches[3][0],40), font = font14, fill = 0)
    draw.text((5, 370), stringShort(launches[4][0],40), font = font14, fill = 0)
    draw.text((220, 310), str(launches[0][1].month) + "/" + str(launches[0][1].day) + " " + str(launches[0][1].time()), font = font14, fill = 0)
    draw.text((220, 325), str(launches[1][1].month) + "/" + str(launches[1][1].day) + " " + str(launches[1][1].time()), font = font14, fill = 0)
    draw.text((220, 340), str(launches[2][1].month) + "/" + str(launches[2][1].day) + " " + str(launches[2][1].time()), font = font14, fill = 0)
    draw.text((220, 355), str(launches[3][1].month) + "/" + str(launches[3][1].day) + " " + str(launches[3][1].time()), font = font14, fill = 0)
    draw.text((220, 370), str(launches[4][1].month) + "/" + str(launches[4][1].day) + " " + str(launches[4][1].time()), font = font14, fill = 0)

    #COVID DATA
    draw.text((325, 165), "US COVID as of: " + str(covidDate.month) + "/" + str(covidDate.day), font = font30, fill = 0)
    draw.text((325, 200), "Total Cases: " + format(covidCurrent[0]['positive'], ",d"), font = font14, fill = 0)
    draw.text((325, 220), "Case Increase: " + format(covidCurrent[0]['positiveIncrease'], ",d"), font = font14, fill = 0)
    draw.text((325, 240), "Total Deaths: " + format(covidCurrent[0]['death'], ",d"), font = font14, fill = 0)
    draw.text((325, 260), "Death Increase: " + format(covidCurrent[0]['deathIncrease'], ",d"), font = font14, fill = 0)
    draw.text((510, 200), "State: " + settings['covid']['state'], font = font18, fill = 0)
    draw.text((480, 220), "Case Increase: " + format(covidState['positiveIncrease']), font = font14, fill = 0)
    draw.text((480, 240), "Death Increase: " + format(covidState['deathIncrease']), font = font14, fill = 0)
    
    #Stock Data
    draw.text((350, 280), "Current Stock Price", font = font24, fill = 0)
    draw.text((325, 310), stockList[0] + " Current: " + str(stockCurrent.tickers[0].info["bid"]) + "  Start: " + str(stockCurrent.tickers[0].info["open"]), font = font14, fill = 0)
    draw.text((325, 325), stockList[1] + " Current: " + str(stockCurrent.tickers[1].info["bid"]) + "  Start: " + str(stockCurrent.tickers[1].info["open"]), font = font14, fill = 0)
    draw.text((325, 340), stockList[2] + " Current: " + str(stockCurrent.tickers[2].info["bid"]) + "  Start: " + str(stockCurrent.tickers[2].info["open"]), font = font14, fill = 0)
    draw.text((325, 355), stockList[3] + " Current: " + str(stockCurrent.tickers[3].info["bid"]) + "  Start: " + str(stockCurrent.tickers[3].info["open"]), font = font14, fill = 0)
    draw.text((325, 370), stockList[4] + " Current: " + str(stockCurrent.tickers[4].info["bid"]) + "  Start: " + str(stockCurrent.tickers[4].info["open"]), font = font14, fill = 0)

    epd.Clear()
    logging.info("Writing Image to Display")
    epd.display(epd.getbuffer(Himage))
    logging.info("Display Sleep")
    epd.sleep()

    



def main():
    try:
        #Get settings
        with open("settings.json", 'r') as f:
            settings = json.load(f)

        startTime = time.time()
        while True:
            refreshDisplay(settings)
            logging.info("Script Sleep")
            sleepTime = settings['basic']['refresh_sec']
            time.sleep(sleepTime - ((time.time() - startTime) % sleepTime))
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd7in5.epdconfig.module_exit()
        exit()

if __name__ =="__main__":
    main()