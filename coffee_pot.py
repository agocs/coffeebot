import logging

## note the following when considering the property values to send in
## name = the name of the coffee pot
## full = sensor value when coffee pot is full (approximate)
## empty = sensor value when the coffee pot is empty (approximate)
## off = sensor value when the coffee pot has been removed (approximate)
## max = sensor value maximum reading (consider additional pressure from a human pumping the coffee out)

class coffee_pot:
    def __init__(self, name, full=400, empty=50, off=0, max=500.00):
        self.name = name
        self.values = [0,0,0,0,0,0,0,0,0,0]
        self.lastbrew = time.time()-1
        self.removed = False
        self.full = full
        self.empty = empty
        self.off = off
        self.postvalue = 0
        self.max = max

    def addReading(self, value):
		## Before adding the new value, filter it?
		self.values.pop(0)
		self.values.append(value)
		
		## This doesn't look like it will work for a few reasons
		## 1) value comparisons (against self.full and self.off should be ranged or approximate; if full = 200 and sensor reads 195, isnt that full?
		## 2) consider how often this function will be called and what happens as we're reading values off one second at a time; couple that with the nature of analog circuits...
		##    to arrive at the conclusion that this probably won't consistently work because, 
		##		after declaring the pot removed, if the value pops above self.off at all, self.remove is set to false
		##		or, if as the pot is reseated, the value gradually (even though probably quickly) rises at all, self.remove is set to false
		##		and, if the readings vary at all from the original values provided for the levels, we'll never have a solid enough reading to provide status at all
		##
		## One suggestion is to declare the pot removed only until we get a reading of at least self.empty, not self.off
		## Another suggestion is to set and store the last removed time, and if recent and we get a reading near full, only then do we reset lastbrew time
		## A final suggestion, probably the most import, is to add a bias value to this class; the bias value is used to provide a range of values to compare against
		## when setting flags for removed and lastbrew at least
		
        if value > self.full and self.removed:
            self.lastbrew = time.time()
        self.removed = value < self.off
        logging.info('Coffee Pot: %s is reading %s', self.name, str(value))

    def getPostValue(self):
        temp_current_level = float(reduce(lambda x, y: x + y, self.values) / float(len(self.values)))

        self.postvalue = float((float(temp_current_level - self.empty)) / (float(int(self.max) - self.empty)))

        self.postvalue = min(self.postvalue, 1)
        self.postvalue = max(self.postvalue, 0)

		logging.info('Coffee Pot: %s post value is %s', self.name, str(self.postvalue))
        return self.postvalue