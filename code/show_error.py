from PyQt5 import QtWidgets,QtCore

from error_ui import Ui_Form


class error(QtWidgets.QFrame, Ui_Form):
    def  __init__ (self):
        super(error, self).__init__()
        self.setupUi(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.pushButton.clicked.connect(self.close)
        
    def raise_error(self,reason):
        self.label.setText("<font size = 5>{}<font>".format(reason))

        
