from GearInidicator import GearIndicatorLCD
from I2CConfig import *
from WideHKOLED import WideHKOLED
import time

if __name__=="__main__":
    #Initialize Gear Indicator on I2C 1
    gearIndicator = GearIndicatorLCD()

    #Initialize I2C 0
    i2cConfig()

    #Initialize digit display on I2C 0
    dataDisplay = WideHKOLED()

    #Test the output to both displays.
    gearIndicator.displayGear(1)
    dataDisplay.sendString("Hello World", 0, 0)
    time.sleep(4)
    gearIndicator.displayGear(2)
    dataDisplay.sendString("This is a test", 1, 0)

