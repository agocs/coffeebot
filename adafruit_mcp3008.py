#!/usr/bin/env python
import time
import os
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
DEBUG = 1

SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

class CoffeeWeight:
    def __init__(self, name, adcnum, tolerance):
        self.name = name
        self.adcnum = adcnum
        self.tolerance = tolerance
        self.sensor_changed = 0
        self.last_read = 0

    #Pretty function to run readadc
    def __str__(self):
        return self.name
    
    def getWeight(self):
        current_read = self.readadc(self.adcnum, SPICLK, SPIMOSI, SPIMISO, SPICS)
        if abs(current_read - self.last_read) > self.tolerance:
            self.last_read = current_read
        return self.last_read
    
    
    
    #gets our weight
    def readadc(self, adcnum, clockpin, mosipin, misopin, cspin):
            if ((adcnum > 7) or (adcnum < 0)):
                    return -1
            GPIO.output(cspin, True)

            GPIO.output(clockpin, False)  # start clock low
            GPIO.output(cspin, False)     # bring CS low

            commandout = adcnum
            commandout |= 0x18  # start bit + single-ended bit
            commandout <<= 3    # we only need to send 5 bits here
            for i in range(5):
                    if (commandout & 0x80):
                            GPIO.output(mosipin, True)
                    else:
                            GPIO.output(mosipin, False)
                    commandout <<= 1
                    GPIO.output(clockpin, True)
                    GPIO.output(clockpin, False)

            adcout = 0
            # read in one empty bit, one null bit and 10 ADC bits
            for i in range(12):
                    GPIO.output(clockpin, True)
                    GPIO.output(clockpin, False)
                    adcout <<= 1
                    if (GPIO.input(misopin)):
                            adcout |= 0x1

            GPIO.output(cspin, True)
        
            adcout >>= 1       # first bit is 'null' so drop it
            return adcout
    
coffee_pot_list = []

coffee_pot_list.append(CoffeeWeight("1", 0, 5))
coffee_pot_list.append(CoffeeWeight("2", 1, 5))


def getWeights():
    coffee_weight_dict = {}
    for coffee_pot in coffee_pot_list:
        coffee_weight_dict[coffee_pot.name] = coffee_pot.getWeight()
    return coffee_weight_dict


if __name__ == "__main__":
    while True:
            # we'll assume that the pot didn't move

            if DEBUG:
                for coffee_pot in coffee_pot_list:
                    print "Coffee Pot: " + coffee_pot.name + " weighs " + str(coffee_pot.getWeight())
                print getWeights()
                    

            # hang out and do nothing for a half second
            time.sleep(0.5)
