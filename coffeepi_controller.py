#!/usr/bin/env python
import time
from collections import deque
import urllib
import urllib2
import json

#This is the controller for our CoffeePi 

import adafruit_mcp3008

coffee_pots={}

minimum_valid_data = 20
maximum_valid_data = 700

class coffee_pot:
    def __init__(self, name, full=400, empty=50, off=20, max=500.00):
        self.name = name
        self.values = [0,0,0,0,0,0,0,0,0,0]
        self.lastbrew = 0
        self.current_level = 0
        self.removed = False
        self.full = full
        self.empty = empty
        self.off = off
        self.post_value = 1.0
        self.max = max
        coffee_pots[name] = self

    def addReading(self, value):
        self.values.pop(0)
        self.values.append(value)
        temp_current_level = reduce(lambda x, y: x + y, self.values) / len(self.values)
        if value > self.full and self.removed:
            self.lastbrew = time.time()
        self.removed = temp_current_level < self.off
        self.post_value = temp_current_level / self.max
        
left = coffee_pot("1") 
right = coffee_pot("2")      



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
            temp_dict["currentLevel"] = coffee_pots[item].post_value
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
        
        
        count = 1
        
    
    count = count + 1
    print count
    time.sleep(1)
    

