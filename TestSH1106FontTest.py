from Hardware.SH1106.SH1106LCD import *
from Hardware.I2CConfig import *
from Hardware.SH1106.SH1106FontLib import *

i2cConfig()
lcd = SH1106LCD()
lcd.setCursorPosition(0, 0)
myFont = font2
for i in myFont:
    lcd.sendDataByte(myFont[i])


