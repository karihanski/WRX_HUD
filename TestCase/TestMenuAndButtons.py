from Hardware.SH1106.SH1106LCD import *
from Hardware.Keypad.Keypad import *
from MenuSystem import MenuManager
from MenuSystem import MainMenuContext
from MenuSystem import MonitoredParameterContext

lcd = SH1106LCD()
menu = MenuManager(lcd)
keypad = Keypad(menu)

while True:
    pass
