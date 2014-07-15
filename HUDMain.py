from Sh1106.GearIndicatorLCD import *
from I2CConfig import *
from WideHKOLED.WideHKOLED import *
from threading import Thread
import time


def cycleGears():
    while True:
        for i in range(0,5):
            gearIndicator.displayGear(i)
            time.sleep(2)

def flopText():
    while True:
        dataDisplay.sendString("HelloWorld", 0, 0)
        time.sleep(1)
        dataDisplay.clearScreen()
        dataDisplay.sendString("HelloWorld", 1, 0)
        time.sleep(1)
        dataDisplay.clearScreen()

if __name__=="__main__":
    #Initialize Gear Indicator on I2C 1
    gearIndicator = GearIndicatorLCD()

    #Initialize I2C 0
    i2cConfig()

    #Initialize digit display on I2C 0
    dataDisplay = WideHKOLED()

    #Test the output to both displays.
    try:
        Thread(target=cycleGears).start()
        Thread(target=flopText()).start()

    except:
        print "Cannot start thread"
    # gearIndicator.displayGear(1)
    # dataDisplay.sendString("Hello World", 0, 0)
    # time.sleep(4)
    # gearIndicator.displayGear(2)
    # dataDisplay.sendString("This is a test", 1, 0)

