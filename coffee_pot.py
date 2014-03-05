import logging

## note the following when considering the property values to send in
## name = the name of the coffee pot
## full = sensor value when coffee pot is full (approximate)
## empty = sensor value when the coffee pot is empty (approximate)
## off = sensor value when the coffee pot has been removed (approximate)
## max = sensor value maximum reading (consider additional pressure from a human pumping the coffee out)
## file = the name of the file that the coffe pot will write its last brew time into.


class coffee_pot:
    def __init__(self, name, full=400, empty=50, off=0, max=500.00, file = None):
        self.name = name
        self.values = [0,0,0,0,0,0,0,0,0,0]
        self.lastbrew = getLastBrew()
        self.removed = False
        self.full = full
        self.empty = empty
        self.off = off
        self.postvalue = 0
        self.max = max
        self.file = file

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



        ## Zach's responses - 
        ## 1) self.full should be used as a minimum value.  The range is essentially anything greater than self.full.
        ## 2) a) this whole system is relying on accurate measurements.  It relies on self.off being absolute, as well as self.full.  If we are going to implement any kind of leniency, than a large part of the system would need to change, and we may need to reframe the entire measurement methodology.
        ## 3) as for using bias values, it seems to me that in this sort of system, we would want to use absolute minimums or maximums.  For instance, we know that x is the lightest it weighs when full, so anything above x is full, not anything within a range of x.  I think we should either wait for the more accurate scales to be in place, and use absolutes, or develop a reliable way of getting accurate levels from an inaccurate scale.
        if value > self.full and self.removed:
            self.lastbrew = time.time()
            writeLastBrew()
        self.removed = value < self.off
        logging.info('Coffee Pot: %s is reading %s', self.name, str(value))

    def getPostValue(self):
        temp_current_level = float(reduce(lambda x, y: x + y, self.values) / float(len(self.values)))

        self.postvalue = float((float(temp_current_level - self.empty)) / (float(int(self.max) - self.empty)))

        self.postvalue = min(self.postvalue, 1)
        self.postvalue = max(self.postvalue, 0)
        logging.info('Coffee Pot: %s post value is %s', self.name, str(self.postvalue))
        return self.postvalue



    def getLastBrew(self):
        """getLastBrew checks to see if self.file exists, and if it does, reads out the first line. 
        I didn't think we needed to check the contents, because nothing extra could end up 
        there, and when we write to the file, we us w+ which deletes the content anyway."""
        logging.info("%s is getting an initial value for its last brew time.", self.name)
        try:
            if os.path.exists(self.file):
                last_brew_file = open(self.file, "r")
                last_brew_file.seek(0)
                logging.info("last brew time was read from %s.", self.file)
                return last_brew_file.readline()
            else:
                logging.info("last brew time was set to current time, because no last brew file was detected.")
                return time.time()

        except:
            logging.exception("Error occured when setting initial last brew time.")

 
    def writeLastBrew(self):
        """writeLastBrew either opens the existing self.file, deletes the contents and writes time.time()
        or it creates the file """
        last_brew_file = open(self.file, 'w+')
        last_brew_file.write(str(time.time()))