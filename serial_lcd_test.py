#!/usr/bin/env python
from coffeepi_serial_lcd import Serial_LCD

program = "CoffeePi v1.0"

lcd = Serial_LCD('/dev/ttyAMA0',19200,program)

temp_dict = {}
temp_dict["pot"] = 1
temp_dict["lastBrew"] = "1/1/1900" 
temp_dict["currentLevel"] = 0.54
temp_dict["removed"] = False

lcd.writeToLcd(temp_dict)