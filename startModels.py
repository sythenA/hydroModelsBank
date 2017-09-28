# -*- coding: big5 -*-

import os
import _winreg
from PyQt4 import QtGui, uic
import qgis.utils
import subprocess
import MBFace
from selectorDiag import netSelector


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
            self.dlg.init1D.clicked.connect(self.callCCHE1D)
            self.dlg.init2D.clicked.connect(self.callCCHE2D)
            self.dlg.init3D.clicked.connect(self.callCCHE3D)
        elif model == 'SRH':
            self.callSRH()
            self.dlg.setWindowTitle('SRH')
            self.dlg.init1D.clicked.connect(self.callSRH1D)
            self.dlg.init2D.clicked.connect(self.callMeshBuilder)
            self.dlg.init3D.clicked.connect(self.callSRH3D)
        else:
            self.callRESED()
            self.dlg.setWindowTitle('RESED')
            self.dlg.init1D.clicked.connect(self.runRESED)
            self.dlg.init2D.clicked.connect(self.viewRESEDManual)

        self.vncPath = ''
        try:
            reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
            k = _winreg.OpenKey(
                reg, r'SOFTWARE\Classes\VncViewer.Config')
            pathKey = _winreg.EnumKey(k, 0)
            pathName = _winreg.QueryValue(k, pathKey)
            pathName = pathName.split(',')[0]
            self.vncPath = pathName
        except:
            pass

    def callSRH1D(self):
        filePath = os.path.join(self.plugin_dir, 'SRH1D_table.xls')
        self.dlg.done(0)
        os.system('"'+filePath+'"')
        os.system("kill -9 %d" % (os.getpid()))

    def callCCHE1D(self):
        path = 'https://drive.google.com/file/d/0BwtvbTG03hXKM21yN0w5Sm14ajA/vi\
ew?usp=sharing'
        os.system('start '+path)
        self.dlg.done(0)

    def callCCHE2D(self):
        title = u'CCHE2D使用方式'
        selector = netSelector(self.iface, title)
        selector.run()
        self.dlg.done(0)

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
        self.dlg.init3D.setVisible(True)
        self.dlg.init1D.setText('CCHE1D')
        self.dlg.init2D.setText('CCHE2D')
        self.dlg.init3D.setText('CCHE3D')

    def callCCHE3D(self):
        if self.vncPath:
            self.dlg.done(0)
            subprocess.Popen([self.vncPath, '210.69.15.31::5999',
                             '-user', '07-gpu', '-password', '1!qaz2@wsx'])

    def callSRH(self):
        self.dlg.init3D.setVisible(True)
        self.dlg.init1D.setText('SRH1D')
        self.dlg.init2D.setText('SRH2D')
        self.dlg.init3D.setText('SRH3D')

    def callRESED(self):
        self.dlg.init1D.setText('RESED')
        self.dlg.init2D.setText(u'使用者手冊')
        self.dlg.init3D.setText(u'')
        self.dlg.init3D.setEnabled(False)
        self.dlg.init3D.setVisible(False)

    def callMeshBuilder(self):
        installed = False
        all_plugin = qgis.utils.available_plugins
        for plugin in all_plugin:
            if 'meshBuilder' in plugin:
                installed = True
                self.MBModel = plugin
            elif 'MeshBuilder' in plugin:
                installed = True
                self.MBModel = plugin

        if installed:
            toolBar = MBFace.callMB(self.iface, self.MBModel)
            self.dlg.done(0)
            toolBar.run()

    def callSRH3D(self):
        if self.vncPath:
            self.dlg.done(0)
            subprocess.Popen([self.vncPath, '210.69.15.31::5999',
                             '-user', '07-gpu', '-password', '1!qaz2@wsx'])

    def run(self):
        result = self.dlg.exec_()
        if result:
            pass
