
import os
from PyQt4 import QtGui, uic


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'simModels.ui'))


class callModelsPopUp(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(callModelsPopUp, self).__init__(parent)

        self.setupUi(self)


class callModels:
    def __init__(self, iface, model='SRH'):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)

        self.dlg = callModelsPopUp()

        if model == 'CCHE':
            self.callCCHE()
            self.dlg.setWindowTitle('CCHE')
        elif model == 'SRH':
            self.callSRH()
            self.dlg.setWindowTitle('SRH')
        else:
            self.callRESED()
            self.dlg.setWindowTitle('RESED')

    def callCCHE(self):
        self.dlg.init1D.setText('CCHE1D')
        self.dlg.init2D.setText('CCHE2D')
        self.dlg.init3D.setText('CCHE3D')

    def callSRH(self):
        self.dlg.init1D.setText('SRH1D')
        self.dlg.init2D.setText('SRH2D')
        self.dlg.init3D.setText('SRH3D')

    def callRESED(self):
        self.dlg.init1D.setText('RESED1D')
        self.dlg.init2D.setText('RESED2D')
        self.dlg.init3D.setText('RESED3D')

    def run(self):
        result = self.dlg.exec_()
        if result:
            pass
