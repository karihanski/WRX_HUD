from Hardware.SH1106.SH1106LCD import *
from Hardware.Input import Keypad
from MenuSystem import MenuManager


lcd = SH1106LCD()
menu = MenuManager(lcd)
keypad = Keypad(menu)

while True:
    pass
