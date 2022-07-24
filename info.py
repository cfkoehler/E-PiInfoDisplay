from PIL import Image, ImageDraw, ImageFont, ImageOps
import classF1Stats as f1Data
from classTodoist import tasks
from classStocks import stockData
from covidData import covidData
from openWeather import openWeather
import classSpaceLaunchNow as rocket
import calendar
import datetime
from waveshare_epd import epd7in5
import logging
import sys
import os
import json
import socket
from textwrap import shorten

picdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)


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

    # Get data
    logging.info("Getting Data")
    weekdays = list(calendar.day_name)
    now = datetime.datetime.now()
    weather = openWeather(settings['weather']['api_key'], settings['weather']
                          ['city_lat'], settings['weather']['city_lon'], "imperial")
    currentWeather = weather.current()
    sunrise = datetime.datetime.fromtimestamp(currentWeather['sunrise'])
    sunset = datetime.datetime.fromtimestamp(currentWeather['sunset'])
    dailyWeather = weather.dailyForcast()
    taskCall = tasks(settings['todoist']['email'],
                     settings['todoist']['password'])
    taskList = taskCall.taskList

    # Set up display
    epd = epd7in5.EPD()
    logging.info("Initialize and Clear Display")
    epd.init()

    Himage = Image.new('1', (epd.width, epd.height),
                       255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    draw.line((320, 0, 320, 384), fill=0)  # center line
    draw.line((10, 90, 310, 90), fill=0)  # Line under time/date
    draw.line((10, 280, 310, 280), fill=0)  # Line above roket lauch
    draw.line((330, 165, 630, 165), fill=0)  # Line bellow Weather

    #Date and time
    draw.text((10, 1), "Refreshed: " + padTime(now.hour) +
              ":" + padTime(now.minute), font=font24, fill=0)
    draw.text((10, 23), calendar.day_name[now.weekday()] + " " + getMonthName(
        now.month) + " " + str(now.day) + getDayModifyer(now.day), font=font24, fill=0)
    draw.text((10, 45), "Sunrise: " + padTime(sunrise.hour) +
              ":" + padTime(sunrise.minute), font=font24, fill=0)
    draw.text((10, 65), "Sunset: " + padTime(sunset.hour) +
              ":" + padTime(sunset.minute), font=font24, fill=0)

    # Weather
    draw.text((320, 1), str(
        round(currentWeather['feels_like'])) + u"\u00b0", font=font80, fill=0)
    draw.text((430, 45), stringShort(
        currentWeather['weather'][0]['description'], 18), font=font24, fill=0)
    draw.text((450, 5), "Low: " + str(round(dailyWeather[0][3]['min'])) + " High: " + str(
        round(dailyWeather[0][3]['max'])), font=font24, fill=0)
    draw.text((480,30), "Hum: " + str(round(currentWeather['humidity'])), font=font18, fill=0)

    # Daily Weather
    draw.text((325, 80), calendar.day_name[dailyWeather[1][0].weekday()] + ": " + dailyWeather[1]
              [6] + " (" + str(round(dailyWeather[1][3]['min'])) + u"\u00b0" + ")", font=font18, fill=0)
    draw.text((325, 100), calendar.day_name[dailyWeather[2][0].weekday(
    )] + ": " + dailyWeather[2][6] + " (" + str(round(dailyWeather[2][3]['min'])) + u"\u00b0" + ")", font=font18, fill=0)
    draw.text((325, 120), calendar.day_name[dailyWeather[3][0].weekday(
    )] + ": " + dailyWeather[3][6] + " (" + str(round(dailyWeather[3][3]['min'])) + u"\u00b0" + ")", font=font18, fill=0)
    draw.text((325, 140), calendar.day_name[dailyWeather[4][0].weekday(
    )] + ": " + dailyWeather[4][6] + " (" + str(round(dailyWeather[4][3]['min'])) + u"\u00b0" + ")", font=font18, fill=0)

    # Rocket Launches
    launches = rocket.getSpaceLaunchs()
    if len(launches) > 1:
        draw.text((50, 280), "Rocket Launches", font=font24, fill=0)
        draw.text((5, 305), stringShort(
            launches[0][0], 30), font=font14, fill=0)
        draw.text((5, 320), stringShort(
            launches[1][0], 30), font=font14, fill=0)
        draw.text((5, 335), stringShort(
            launches[2][0], 30), font=font14, fill=0)
        draw.text((5, 350), stringShort(
            launches[3][0], 30), font=font14, fill=0)
        draw.text((5, 365), stringShort(
            launches[4][0], 30), font=font14, fill=0)
        draw.text((220, 305), str(launches[0][1].month) + "/" + str(
            launches[0][1].day) + " " + str(launches[0][1].time()), font=font14, fill=0)
        draw.text((220, 320), str(launches[1][1].month) + "/" + str(
            launches[1][1].day) + " " + str(launches[1][1].time()), font=font14, fill=0)
        draw.text((220, 335), str(launches[2][1].month) + "/" + str(
            launches[2][1].day) + " " + str(launches[2][1].time()), font=font14, fill=0)
        draw.text((220, 350), str(launches[3][1].month) + "/" + str(
            launches[3][1].day) + " " + str(launches[3][1].time()), font=font14, fill=0)
        draw.text((220, 365), str(launches[4][1].month) + "/" + str(
            launches[4][1].day) + " " + str(launches[4][1].time()), font=font14, fill=0)
    else:
        draw.text((40, 300), "Error Requesting", font=font24, fill=0)
        draw.text((40, 340), "Rocket Launches", font=font24, fill=0)

    # F1 Data
    f1 = f1Data.getChampionship()
    nextRace = f1Data.getNextRace()
    draw.text((325, 162), "Current F1 Standings", font=font30, fill=0)
    draw.text((325, 192), "Points", font=font14, fill=0)
    draw.text((370, 192), "Racer", font=font14, fill=0)
    draw.text((450, 192), "Team", font=font14, fill=0)
    xPx = 210
    for i in range(1, 11):
        draw.text((325, xPx), f1[str(i)].get('points'), font=font14, fill=0)
        draw.text((370, xPx), f1[str(i)].get('name'), font=font14, fill=0)
        draw.text((450, xPx), f1[str(i)].get('team'), font=font14, fill=0)
        xPx = xPx + 15
    if len(nextRace) > 0:
        draw.text((520, 195), "NEXT RACE:", font=font14, fill=0)
        draw.text((520, 210), stringShort(
            nextRace['name'], 20), font=font14, fill=0)
        draw.text((535, 225), stringShort(
            nextRace['date'], 20), font=font14, fill=0)

    # Task List
    draw.text((50, 92), "Upcoming Tasks", font=font24, fill=0)
    xPx = 123
    amount = len(taskList)
    if amount > 10:
        amount = 10

    for i in range(0, amount):
        draw.text((5, xPx), stringShort(
            taskList[i][0], 80), font=font14, fill=0)
        draw.text((235, xPx), stringShort(
            taskList[i][1], 10), font=font14, fill=0)
        xPx = xPx + 15

    epd.Clear()
    logging.info("Writing Image to Display")
    Himage = Himage.convert('L')
    inverted_image = ImageOps.invert(Himage)
    inverted_image = inverted_image.convert('1')
    epd.display(epd.getbuffer(inverted_image))

    logging.info("Display Sleep")
    epd.sleep()


def main():
    try:
        # Get settings
        with open("settings.json", 'r') as f:
            settings = json.load(f)
        nightStartVal = settings['basic']['night_start']
        nightEndVal = settings['basic']['night_end']
        nightStart = int(nightStartVal[0:2])
        nightEnd = int(nightEndVal[0:2])

        sleep = False
        currentTime = datetime.datetime.now()
        if int(currentTime.hour) < nightStart and int(currentTime.hour) > nightEnd:
            sleep = False
            logging.info("Script Refresh")
            refreshDisplay(settings)
        else:
            logging.info("Script Night Mode")
            if sleep != True:
                epd = epd7in5.EPD()
                epd.init()
                epd.Clear()
                sleep = True

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd7in5.epdconfig.module_exit()
        exit()


if __name__ == "__main__":
    main()
