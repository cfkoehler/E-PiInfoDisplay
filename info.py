import sys
import os
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

logging.basicConfig(level=logging.DEBUG)


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

def weekDayCircle(date):
    weekdayNumber = date.isoweekday()
    switcher = {
        1: draw.arc((50, 90, 190, 100), 0, 360, fill = 0),
        2: draw.arc((50, 90, 190, 100), 0, 360, fill = 0),
        3: draw.arc((50, 90, 190, 100), 0, 360, fill = 0),
        4: draw.arc((50, 90, 190, 100), 0, 360, fill = 0),
        5: draw.arc((50, 90, 190, 100), 0, 360, fill = 0),
        6: draw.arc((50, 90, 190, 100), 0, 360, fill = 0),
        7: draw.ellipse((50, 90, 100, 120), fill=0, outline=0)
    }
    switcher.get(weekdayNumber, 1)
    print(weekdayNumber)


try:
    logging.info("Info Display Test")
    epd = epd7in5.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    font24 = ImageFont.truetype('Font.ttc', 24)
    font18 = ImageFont.truetype('Font.ttc', 18)
    font30 = ImageFont.truetype('Font.ttc', 30)
    font80 = ImageFont.truetype('Font.ttc', 80)
    now = datetime.datetime.now()

    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    draw.line((320, 0, 320, 384), fill = 0)
    draw.text((50, 5), str(now.hour) + ":" + str(now.minute), font = font80, fill = 0)
    draw.text((50, 90), "M   T   W   Th   F   Su   Sa", font = font18, fill = 0)
    weekDayCircle(now)
    draw.text((50, 115), getMonthName(now.month)  + " " + str(now.day) + getDayModifyer(now.day) + " " + str(now.year), font = font24, fill = 0)
    
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)
    logging.info("Clear...")
    epd.init()
    epd.Clear()




except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5.epdconfig.module_exit()
    exit()