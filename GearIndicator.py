from Sh1106.SH1106LCD import *
from I2CConfig import *
class GearIndicator():



    def __init__(self):
        #Set up second I2C bus
        i2cConfig()
        self.lcd = SH1106LCD(1)

        #Import startup image from disk.
        self.image_path = os.chdir("Sh1106")

        self.lcd.addImage("FirstGear", "shift_1_sized.bmp")
        self.lcd.addImage("SecondGear", "shift_2_sized.bmp")
        self.lcd.addImage("ThirdGear", "shift_3_sized.bmp")
        self.lcd.addImage("FourthGear", "shift_4_sized.bmp")
        self.lcd.addImage("FifthGear", "shift_5_sized.bmp")
        self.lcd.addImage("Reverse", "shift_r_sized.bmp")
        self.lcd.addImage("Neutral", "shift_r_sized.bmp")
        self.lcd.addImage("SubaruLogo", "subie_logo.bmp")
        self.lcd.addImage("WrxLogo", "wrx_log.bmp")
