#!/usr/bin/env python
from __future__ import division
import time
from collections import deque
import urllib
import urllib2
import json
from coffeepi_serial_lcd import Serial_LCD
lcd = Serial_LCD('/dev/ttyAMA0', 19200)
#This is the controller for our CoffeePi 

import adafruit_mcp3008

coffee_pots={}

minimum_valid_data = 0
maximum_valid_data = 700


## important, the max of a pot is the fullest we will consider the pot to be ever, but the full amount is how heavy
## it needs to be in order to be considered full by our controller.

class coffee_pot:
    def __init__(self, name, full=400, empty=50, off=0, max=500.00):
        self.name = name
        self.values = [0,0,0,0,0,0,0,0,0,0]
        self.lastbrew = time.time()
        self.current_level = 0
        self.removed = False
        self.full = full
        self.empty = empty
        self.off = off
        self.post_value = 0
        self.max = max
        self.max_cycle = 0
        coffee_pots[name] = self

    def addReading(self, value):
        self.values.pop(0)
        self.values.append(value)
        if value > self.full and self.removed:
            self.lastbrew = time.time()
            self.max = value
        self.removed = value < self.off
        print "Coffee Pot: " + self.name + " is reading " + str(value) + "\n"

        # thiscurrentvalue = min(temp_current_level, self.full)
        # thiscurrentvalue = max(thiscurrentvalue, self.empty)

        # self.post_value = (thiscurrentvalue - self.empty) / (self.full - self.empty)
        #self.post_value = sumbitches

    def getPostValue(self):
        temp_current_level = float(reduce(lambda x, y: x + y, self.values) / float(len(self.values)))

        #sumbitches = min(temp_current_level / self.full, 1)
        #sumbitches = max(sumbitches, 0)

        # self.postvalue = (self.full - self.empty) / (temp_current_level-self.empty)
        self.postvalue = float((float(temp_current_level - self.empty)) / (float(self.max - self.empty)))

        self.postvalue = min(self.postvalue, 1)
        self.postvalue = max(self.postvalue, 0)

        return self.postvalue

        
left = coffee_pot("1", full=35, empty = 21, off=12, max=50) 
right = coffee_pot("2", full=100, empty = 64, off = 20, max=125)     



count = 1
while True:

    
    readings = adafruit_mcp3008.getWeights()
    for reading in readings:
        if minimum_valid_data > readings[reading] or maximum_valid_data < readings[reading]:
            continue            
        coffee_pots[reading].addReading(readings[reading])
        if coffee_pots[reading].max_cycle != 0:
            if coffee_pots[reading].max_cycle < 2:
                coffee_pots[reading].max_cycle += 1
            else:
                coffee_pots[reading].max_cycle = 0
                coffee_pots[reading].max = reading 

    if count % 10 == 0:
        to_post = {"update":[]}
        for item in coffee_pots:
            temp_dict = {}
            temp_dict["pot"] = coffee_pots[item].name
            temp_dict["lastBrew"] = coffee_pots[item].lastbrew 
            temp_dict["currentLevel"] = coffee_pots[item].getPostValue()
            temp_dict["removed"] = coffee_pots[item].removed
            to_post["update"].append(temp_dict)
            print to_post["update"]
        ##POST HERE
        url = 'http://coffeemonitor-backstopcoffee.rhcloud.com/pots/update'
        params = json.JSONEncoder().encode(to_post)
        headers ={'Content-type': "application/json"}
        req = urllib2.Request(url, params, headers)
        try: 
            response = urllib2.urlopen(req).read()
        except urllib2.HTTPError, error:
            print error
            print "it failed."
            contents = error.read()
        lcd.writeToLcd(to_post["update"])
        count = 1
        
    
    count = count + 1
    time.sleep(1)
    


    #

