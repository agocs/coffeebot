"""This is the module DocString!  It contains important information 
about what this module does.  For instance, 
this module is the data controller for the coffeebot!"""

#!/usr/bin/env python
#This is the controller for our CoffeePi
from __future__ import division
from coffee_pot import coffee_pot
import time
import urllib2
import json
from storm_log import *

if __name__ == '__main__':
    import adafruit_mcp3008
    from coffeepi_serial_lcd import coffeepi_serial_lcd

#defaults for readings off of sensors
VALID_DATA_MIN = 10
VALID_DATA_MAX = 125
COFFEE_POTS = {}




## THESE ARE SET UP FUNCTIONS.  They prepare for the main loop.

def initialize_lcd():
    """Initializes the LCD Screen."""
    try:
        lcd = coffeepi_serial_lcd('/dev/ttyAMA0', 19200)
        #storm.send("Initialized LCD Screen.", sourcetype = 'syslog', host = 'controller')
    except:
        storm.send("ERROR Failed to initialize the LCD Screen.", sourcetype = 'syslog', host = 'controller')
    return lcd
    

def initialize_coffee_pots():
    """Adds coffee pots to the dictionary COFFEE_POTS."""
    #storm.send("Initializing coffee pot objects.", sourcetype = 'syslog', host = 'controller')
    
    try:
        COFFEE_POTS["1"] = coffee_pot("1", 
                                        full=50, 
                                        empty=35, 
                                        off=50, 
                                        max=100, 
                                        file="coffee_pot_1.txt")

        COFFEE_POTS["2"] = coffee_pot("2", 
                                        full=50, 
                                        empty=35, 
                                        off=50, 
                                        max=100, 
                                        file="coffee_pot_2.txt")
        storm.send("Coffee pot objects created.", sourcetype = 'syslog', host = 'controller')
    except:
        storm.send("ERROR Problem when initializing coffee pots.", sourcetype = 'syslog', host = 'controller')


##THESE ARE EVENT LOOP FUNCTIONS.  They are used to add readings and send them out.

def read_write_sensors():
    """reads values by calling getWeights fron adafruit_mcp3008.  """
    #storm.send("Reading sensors and adding reading to coffee pots.", sourcetype = 'syslog', host = 'controller')
    try:
        try:
            readings = adafruit_mcp3008.getWeights()
        except:
            storm.send("ERROR occured in the getWeights() function in file adafruit_mcp3008")
        for reading in readings:
            value = readings[reading]
            
            if VALID_DATA_MIN > value:
                value = VALID_DATA_MIN
                
            if VALID_DATA_MAX < value:
                value = VALID_DATA_MAX
            try:
                COFFEE_POTS[reading].add_reading(value)    
            except:
                storm.send('ERROR occured while trying to add readings to coffee pots.')
            
        #storm.send("Sensors read and reading set to coffee pots successfully.", sourcetype = 'syslog', host = 'controller')
    except:
        storm.send('ERROR occurred during read and setting values from sensors', sourcetype = 'syslog', host = 'controller')
        
        #Consider here performing a clean exit; then configure the script to respawn if it dies?


def build_post_request():
    """builds and returns a customized post request containing coffee pots."""

    #storm.send('Setting up data dictionary...', sourcetype = 'syslog', host = 'controller')
    to_post = {"update":[]}
    try:    
        for item in COFFEE_POTS:
            temp_dict = {}
            temp_dict["pot"] = COFFEE_POTS[item].name
            temp_dict["lastBrew"] = COFFEE_POTS[item].lastbrew
            temp_dict["currentLevel"] = COFFEE_POTS[item].get_post_value()
            temp_dict["removed"] = COFFEE_POTS[item].removed
            to_post["update"].append(temp_dict)
        #storm.send('Data dictionary created:' + str(to_post["update"]), sourcetype = 'syslog', host = 'controller')
        #storm.send("Successfully built post request", sourcetype = 'syslog', host = 'controller')
    except:
        storm.send("ERROR Problem while building post request.", sourcetype = 'syslog', host = 'controller')
    return to_post


def send_post_request(post_request):
    """sends post_request, provided as the only argument, to the coffeemonitor."""
    #storm.send('Preparing to post data to coffee monitor site...', sourcetype = 'syslog', host = 'controller')
    try:
        url = 'http://coffeemonitor-backstopcoffee.rhcloud.com/pots/update'
        params = json.JSONEncoder().encode(post_request)
        headers = {'Content-type': "application/json"}
        req = urllib2.Request(url, params, headers)

        response = urllib2.urlopen(req)
        response.read()
        storm.send("Successfully sent post request: " + params, sourcetype = 'syslog', host = 'controller')
    except urllib2.HTTPError, error:
        storm.send('ERROR occurred while attempting to post an update to the web service', sourcetype = 'syslog', host = 'controller')
        contents = error
        contents.read()


def main():
    """Main event loop."""
    
    lcd = initialize_lcd()

    initialize_coffee_pots()
    
    storm.send('Entering main loop...', sourcetype = 'syslog', host = 'controller')    
    count = 1
    
    while True:
        #once per second, sensors are read and readings are added to coffeepots.
        read_write_sensors()
            
        try:
            if count % 10 == 0:
                
                post_request = build_post_request()

                send_post_request(post_request)
                    
                lcd.writeToLcd(post_request["update"])
                count = 1
        except:
            storm.send('ERROR occurred while attempting to process the sensor readings', sourcetype = 'syslog', host = 'controller')
        
        count = count + 1
        time.sleep(1)

if __name__ == '__main__':
    main()
