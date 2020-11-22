# E-Pi Information Display

*<u>Readme instructions are not complete</u>*

#### Basic information display for E-ink monitor attached to pi zero w

##### Information Display:

- Time
- Date
- Todoist Tasks
- Upcoming Space Rocket Launches
- Current Weather
- 4 day Weather forecast
- Current USA COVID Data
- Current USA State COVID Data
- Current US Stock Price for 5 Stocks



#### Supplies: 

- E-Ink Display: https://www.waveshare.com/product/displays/e-paper/7.5inch-e-paper-hat.htm
- Raspberry Pi Zero W
- 3D printed Stand: https://www.thingiverse.com/thing:3152929



#### Set Up Process:

1. Set up raspberry pi headless on your local network (assuming you can do this or find out how to do this on your own.)

2. Install python libraries that are used:

   1. ```bash
      pip3 install yfinance
      ```

      

   2. ```bash
      pip3 install todoist-python
      ```

3. Rename settings-SAMPLE.json to settings.json

4. Add parameters to settings.json

   1. Weather: 
      1. Get API key from openWeather
      2. Add Location latitude and longitude
      3. Set Units
   2. Add current state to COVID setting
   3. Add login credentials to Todoist
   4. Add 5 stock ticker symbols

5. Start script: 

   ```bash
   python3 info.py
   ```