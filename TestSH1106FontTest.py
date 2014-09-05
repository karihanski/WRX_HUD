from Hardware.SH1106.SH1106LCD import *
from Hardware.I2CConfig import *
from Hardware.SH1106.SH1106FontLib import *

i2cConfig()
lcd = SH1106LCD()
lcd.setCursorPosition(0, 0)
myFont = font1
for i in range(0,130):
    lcd.sendDataByte(myFont[i])


