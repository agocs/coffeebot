#!/usr/bin/env python
#This is the controller for our CoffeePi
from __future__ import division
import time
from collections import deque
import urllib
import urllib2
import json
import logging
import adafruit_mcp3008
import coffee_pot
import coffeepi_serial_lcd

#defaults for readings off of sensors
valid_data_min = 20
valid_data_max = 125

#Setup logging
logging.basicConfig(file='coffee_bot_3000.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s')

logging.info('Initializing LCD interface...')
lcd = coffeepi_serial_lcd('/dev/ttyAMA0', 19200)

logging.info('Initializing coffee pot objects...')
coffee_pots={}
coffee_pots["1"] = coffee_pot("1", full=70, empty = 35, off = valid_data_min, max=valid_data_max)
coffee_pots["2"] = coffee_pot("2", full=70, empty = 35, off = valid_data_min, max=valid_data_max)

logging.info('Entering main loop...')
count = 1
while True:

	try:
		logging.info('Reading sensors values...')
		readings = adafruit_mcp3008.getWeights()
		
		for reading in readings:
			value = readings[reading]
			
			if valid_data_min > value:
				value = valid_data_min
				
			if valid_data_max < value
				value = valid_data_max

			coffee_pots[reading].addReading(value)
	except:
		logging.exception('Error occurred during read and setting values from sensors')
		#Consider here performing a clean exit; then configure the script to respawn if it dies?

	try:
		if count % 10 == 0:
			logging.info('Setting up data dictionary...')
			to_post = {"update":[]}
			for item in coffee_pots:
				temp_dict = {}
				temp_dict["pot"] = coffee_pots[item].name
				temp_dict["lastBrew"] = coffee_pots[item].lastbrew
				temp_dict["currentLevel"] = coffee_pots[item].getPostValue()
				temp_dict["removed"] = coffee_pots[item].removed
				to_post["update"].append(temp_dict)
				logging.info('Data dictionary created: %s', to_post["update"])
				
			##POST HERE
			try:
				logging.info('Preparing to post data to coffee monitor site...')
				url = 'http://coffeemonitor-backstopcoffee.rhcloud.com/pots/update'
				params = json.JSONEncoder().encode(to_post)
				headers ={'Content-type': "application/json"}
				req = urllib2.Request(url, params, headers)

				response = urllib2.urlopen(req).read()
			except urllib2.HTTPError, error:
				logging.exception('Error occurred while attempting to post an update to the web service')
				contents = error.read()
				
			lcd.writeToLcd(to_post["update"])
			count = 1
	except:
		logging.exception('Error occurred while attempting to process the sensor readings')

    count = count + 1
    time.sleep(1)
