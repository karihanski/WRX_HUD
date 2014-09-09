from MenuSystem import MainMenuContext
from MenuSystem import MonitoredParameterContext
from MenuSystem import PeakBoostContext
from MenuSystem import DtcCodeContext

class MenuManager():

    def __init__(self, inLcd):
        self.lcd = inLcd
        #Spawn the menu contexts
        self.contexts = {}
        self.contexts['Main Menu'] = MainMenuContext(self, inLcd)
        self.contexts['Monitored Parameters'] = MonitoredParameterContext(self, inLcd)
        self.contexts['Peak Boost'] = PeakBoostContext(self, inLcd)
        self.contexts['DtcCodeContext'] = DtcCodeContext(self, inLcd)

        self.currentContext = 'Main Menu'
        self.menuMode = False

    """
    Callbacks for buttons
    """
    def upButtonCallback(self):
        if self.menuMode:
            self.contexts[self.currentContext].onUp()

    def downButtonCallback(self):
        if self.menuMode:
            self.contexts[self.currentContext].onDown()

    def setButtonCallback(self):
        if self.menuMode:
            self.contexts[self.currentContext].onSet()
        else:
            self.menuMode = True
            self.currentContext = 'Main Menu'
            self.initiateDisplay()

    def backButtonCallback(self):
        if self.menuMode:
            self.contexts[self.currentContext].onBack()

    """
    Misc
    """
    def setCurrentContext(self, inContext):
        self.currentContext = inContext

    def initiateDisplay(self):
        self.contexts[self.currentContext].initDisplay()