from Hardware.Sh1106.SH1106LCD import *
from Hardware.I2CConfig import *
from Hardware.WideHKOLED.WideHKOLED import *



if __name__=="__main__":
    i2cConfig()
    gearIndicator = SH1106LCD(1)
    dataDisplay = WideHKOLED()