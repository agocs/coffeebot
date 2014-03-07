"""This is the module DocString!  It contains important information 
about what this module does.  For instance, 
this module is the data controller for the coffeebot!"""

#!/usr/bin/env python
#This is the controller for our CoffeePi
from __future__ import division
import logging
from coffee_pot import coffee_pot
import time
import urllib2
import json

if __name__ == '__main__':
    import adafruit_mcp3008
    from coffeepi_serial_lcd import coffeepi_serial_lcd

#defaults for readings off of sensors
VALID_DATA_MIN = 50
VALID_DATA_MAX = 125
COFFEE_POTS = {}




## THESE ARE SET UP FUNCTIONS.  They prepare for the main loop.
def configure_logging():
    """Sets up the basic configuration for loggin."""
    logging.basicConfig(file='coffee_bot_3000.log', 
                        level=logging.DEBUG, 
                        format='%(asctime)s %(levelname)s %(message)s')
    logging.info("Logging configured.")



def initialize_lcd():
    """Initializes the LCD Screen."""
    try:
        lcd = coffeepi_serial_lcd('/dev/ttyAMA0', 19200)
        logging.info("Initialized LCD Screen.")
    except:
        logging.exception("Failed to initialize the LCD Screen.")
    return lcd
    

def initialize_coffee_pots():
    """Adds coffee pots to the dictionary COFFEE_POTS."""
    logging.info("Initializing coffee pot objects.")
    
    try:
        COFFEE_POTS["1"] = coffee_pot("1", 
                                        full=50, 
                                        empty=35, 
                                        off=VALID_DATA_MIN, 
                                        max=VALID_DATA_MAX, 
                                        file="coffe_pot_1.txt")

        COFFEE_POTS["2"] = coffee_pot("2", 
                                        full=50, 
                                        empty=35, 
                                        off=VALID_DATA_MIN, 
                                        max=VALID_DATA_MAX, 
                                        file="coffee_pot_2.txt")
        logging.info("Coffee pot objects created.")
    except:
        logging.exception("Problem when initializing coffee pots.")


##THESE ARE EVENT LOOP FUNCTIONS.  They are used to add readings and send them out.

def read_write_sensors():
    """reads values by calling getWeights fron adafruit_mcp3008.  """
    logging.info("Reading sensors and adding reading to coffee pots.")
    try:
        readings = adafruit_mcp3008.getWeights()
        
        for reading in readings:
            value = readings[reading]
            
            if VALID_DATA_MIN > value:
                value = VALID_DATA_MIN
                
            if VALID_DATA_MAX < value:
                value = VALID_DATA_MAX
            COFFEE_POTS[reading].add_reading(value)
        logging.info("Sensors read and reading set to coffee pots successfully.")
    except:
        logging.exception('Error occurred during read and setting values from sensors')
        
        #Consider here performing a clean exit; then configure the script to respawn if it dies?


def build_post_request():
    """builds and returns a customized post request containing coffee pots."""

    logging.info('Setting up data dictionary...')
    to_post = {"update":[]}
    try:    
        for item in COFFEE_POTS:
            temp_dict = {}
            temp_dict["pot"] = COFFEE_POTS[item].name
            temp_dict["lastBrew"] = COFFEE_POTS[item].lastbrew
            temp_dict["currentLevel"] = COFFEE_POTS[item].get_post_value()
            temp_dict["removed"] = COFFEE_POTS[item].removed
            to_post["update"].append(temp_dict)
            logging.info('Data dictionary created: %s', 
                        to_post["update"])
        logging.info("Successfully built post request")
    except:
        logging.exception("Problem while building post request.")
    return to_post


def send_post_request(post_request):
    """sends post_request, provided as the only argument, to the coffeemonitor."""
    logging.info('Preparing to post data to coffee monitor site...')
    try:
        url = 'http://coffeemonitor-backstopcoffee.rhcloud.com/pots/update'
        params = json.JSONEncoder().encode(post_request)
        headers = {'Content-type': "application/json"}
        req = urllib2.Request(url, params, headers)

        response = urllib2.urlopen(req)
        response.read()
        logging.info("Successfully sent post request.")
    except urllib2.HTTPError, error:
        logging.exception('Error occurred while attempting to post an update to the web service')
        contents = error
        contents.read()


def main():
    """Main event loop."""
    


    configure_logging()

    lcd = initialize_lcd()

    initialize_coffee_pots()
    
    logging.info('Entering main loop...')    
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
            logging.exception('Error occurred while attempting to process the sensor readings')
        
        count = count + 1
        time.sleep(1)

if __name__ == '__main__':
    main()
