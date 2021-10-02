from PyQt5 import QtWidgets

from track_ui import Ui_Form


class track(QtWidgets.QFrame, Ui_Form):
    def  __init__ (self):
        super(track, self).__init__()
        self.setupUi(self)
        self.track = 0
        self.radioButton.toggled.connect(self.setfirst)
        self.radioButton_2.toggled.connect(self.setsecond)
        self.radioButton_3.toggled.connect(self.setnone)
        
    def setfirst(self):
        self.track = -1

    def setsecond(self):
        self.track = -2

    def setnone(self):
        self.track = 0

