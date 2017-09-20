# -*- coding: big5 -*-

import os
from PyQt4 import QtGui, uic
import qgis.utils
import MBFace


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
            self.dlg.init1D.clicked.connect(self.callSRH1D)
            self.dlg.init2D.clicked.connect(self.callMeshBuilder)
        else:
            self.callRESED()
            self.dlg.setWindowTitle('RESED')
            self.dlg.init1D.clicked.connect(self.runRESED)
            self.dlg.init2D.clicked.connect(self.viewRESEDManual)

    def callSRH1D(self):
        filePath = os.path.join(self.plugin_dir, 'SRH1D_table.xls')
        self.dlg.done(0)
        os.system('"'+filePath+'"')
        os.system("kill -9 %d" % (os.getpid()))

    def runRESED(self):
        filePath = os.path.join(self.plugin_dir, 'RiverSimulation-20160629.exe')
        self.dlg.done(0)
        os.system('"'+filePath+'"')
        os.system("kill -9 %d" % (os.getpid()))

    def viewRESEDManual(self):
        filePath = os.path.join(self.plugin_dir, 'RESEDManual20160627.pdf')
        self.dlg.done(0)
        os.system('"'+filePath+'"')
        os.system("kill -9 %d" % (os.getpid()))

    def callCCHE(self):
        self.dlg.init1D.setText('CCHE1D')
        self.dlg.init2D.setText('CCHE2D')
        self.dlg.init3D.setText('CCHE3D')

    def callSRH(self):
        self.dlg.init1D.setText('SRH1D')
        self.dlg.init2D.setText('SRH2D')
        self.dlg.init3D.setText('SRH3D')

    def callRESED(self):
        self.dlg.init1D.setText('RESED')
        self.dlg.init2D.setText(u'使用者手冊')
        self.dlg.init3D.setText(u'')
        self.dlg.init3D.setEnabled(False)

    def callMeshBuilder(self):
        installed = False
        all_plugin = qgis.utils.available_plugins
        for plugin in all_plugin:
            if 'meshBuilder' in plugin:
                installed = True

        if installed:
            toolBar = MBFace.callMB(self.iface)
            self.dlg.done(0)
            toolBar.run()

    def run(self):
        result = self.dlg.exec_()
        if result:
            pass
