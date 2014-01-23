#!/usr/bin/env python
from __future__ import division
import time
from collections import deque
import urllib
import urllib2
import json
from coffeepi_serial_lcd import Serial_LCD
lcd = serial_LCD('/dev/ttyAMA0', 19200)
#This is the controller for our CoffeePi 

import adafruit_mcp3008

coffee_pots={}

minimum_valid_data = 5
maximum_valid_data = 700

class coffee_pot:
    def __init__(self, name, full=400, empty=50, off=20, max=500.00):
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
        coffee_pots[name] = self

    def addReading(self, value):
        self.values.pop(0)
        self.values.append(value)
        if value > self.full and self.removed:
            self.lastbrew = time.time()
        self.removed = value < self.off


        # thiscurrentvalue = min(temp_current_level, self.full)
        # thiscurrentvalue = max(thiscurrentvalue, self.empty)

        # self.post_value = (thiscurrentvalue - self.empty) / (self.full - self.empty)
        #self.post_value = sumbitches

    def getPostValue(self):
        temp_current_level = float(reduce(lambda x, y: x + y, self.values) / float(len(self.values)))

        #sumbitches = min(temp_current_level / self.full, 1)
        #sumbitches = max(sumbitches, 0)

        # self.postvalue = (self.full - self.empty) / (temp_current_level-self.empty)
        self.postvalue = float((float(temp_current_level - self.empty)) / (float(self.full - self.empty)))

        self.postvalue = min(self.postvalue, 1)
        self.postvalue = max(self.postvalue, 0)

        return self.postvalue

        
left = coffee_pot("1", full=115, empty = 61, off=25, max=115) 
right = coffee_pot("2", full=50, empty = 30, off = 25, max=50)     



count = 1
while True:

    
    readings = adafruit_mcp3008.getWeights()
    print readings
    for reading in readings:
        if minimum_valid_data > readings[reading] or maximum_valid_data < readings[reading]:
            continue            
        coffee_pots[reading].addReading(readings[reading])

    if count % 10 == 0:
        print "modded on 10"
        to_post = {"update":[]}
        for item in coffee_pots:
            temp_dict = {}
            temp_dict["pot"] = coffee_pots[item].name
            temp_dict["lastBrew"] = coffee_pots[item].lastbrew 
            temp_dict["currentLevel"] = coffee_pots[item].getPostValue()
            temp_dict["removed"] = coffee_pots[item].removed
            to_post["update"].append(temp_dict)
        ##POST HERE
        print "exited the for"
        url = 'http://coffeemonitor-backstopcoffee.rhcloud.com/pots/update'
        params = json.JSONEncoder().encode(to_post)
        headers ={'Content-type': "application/json"}
        req = urllib2.Request(url, params, headers)
        print "about to try"
        try: 
            response = urllib2.urlopen(req).read()
            print params
        except urllib2.HTTPError, error:
            print error
            print "it failed."
            contents = error.read()
        print "tried to send request"
        coffeepi_serial_lcd.write
        lcd.writeToLcd(to_post["update"][lcd_count])
        count = 1
        
    
    count = count + 1
    print count
    time.sleep(1)
    

