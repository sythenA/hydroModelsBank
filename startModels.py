# -*- coding: big5 -*-

import os
import _winreg
import re
from PyQt4 import QtGui, uic
import qgis.utils
import subprocess
import MBFace
from toUnicode import toUnicode
from qgis.PyQt.QtCore import QSettings
from selectorDiag import netSelector
from PyQt4.QtGui import QMessageBox, QFileDialog
from msg import MSG
from link import links
from infoDiag import infoView


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
        self.settings = QSettings('ManySplendid', 'HydroModelBanks')
        self.vncPath = self.settings.value('vnc_path')

        if model == 'CCHE':
            self.callCCHE()
            self.dlg.setWindowTitle('CCHE')
            self.dlg.init1D.clicked.connect(self.callCCHE1D)
            self.dlg.init2D.clicked.connect(self.callCCHE2D)
            self.dlg.init3D.clicked.connect(self.callCCHE3D)
            self.dlg.init4.clicked.connect(self.callCCHE_MESH)
        elif model == 'SRH':
            self.callSRH()
            self.dlg.setWindowTitle('SRH')
            self.dlg.init1D.clicked.connect(self.callSRH1D)
            self.dlg.init2D.clicked.connect(self.callSRH2D)
            self.dlg.init3D.clicked.connect(self.callSRH3D)
            self.dlg.init4.setVisible(False)
        elif model == 'RESED':
            self.callRESED()
            self.dlg.setWindowTitle('RESED')
            self.dlg.init1D.clicked.connect(self.runRESED)
            self.dlg.init2D.clicked.connect(self.viewRESEDManual)
        else:
            self.callNTOUHydro()
            self.dlg.setWindowTitle(toUnicode(MSG['msg18']))
            self.dlg.init1D.clicked.connect(self.callNTOUHydro_WRAP)
            self.dlg.init2D.clicked.connect(self.callNTOUHydro_WRA)
            self.dlg.init3D.clicked.connect(self.callNTOUHydro_author)

    def callNTOUHydro(self):
        self.dlg.init4.setVisible(False)
        self.dlg.init3D.setVisible(True)
        self.dlg.init1D.setText(toUnicode(MSG['msg04']))
        self.dlg.init2D.setText(toUnicode(MSG['msg05']))
        self.dlg.init3D.setText(toUnicode(MSG['msg06']))

    def callNTOUHydro_WRAP(self):
        try:
            batPath = self.settings.value('NTOUHydro')
            subprocess.Popen([batPath])
        except(TypeError):
            try:
                reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
                key = _winreg.OpenKey(
                    reg,
                    r'SOFTWARE\Wow6432Node\MicrosoftWindows\CurrentVersion\
Uninstall\QGIS Wien\DisplayIcon')
                pathKey = _winreg.EnumKey(key, 0)
                pathName = _winreg.QueryValue(key, pathKey)

                basePath = os.path.dirname(os.path.dirname(pathName))
                batPath = os.path.join(basePath, 'bin', 'qgis-ltr.bat')

                self.settings.setValue('NTOUHydro', batPath)
                f = open(os.path.join(self.plugin_dir, 'settings'), 'w')
                for key in self.settings.keys():
                    f.write(key + ' = ' + self.settings[key] + '\n')
                f.close()

                subprocess.Popen([batPath])
            except(WindowsError):
                title = toUnicode(MSG['msg07'])
                message = toUnicode(MSG['msg08'])
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(message)
                msg.setWindowTitle(title)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

                Caption = toUnicode(MSG['msg09'])
                fileName = QFileDialog.getOpenFileName(self.dlg, Caption, '',
                                                       "*.bat")
                if fileName:
                    self.ntouHydroPath = toUnicode(fileName)
                    self.settings.setValue('NTOUHydro', self.ntouHydroPath)

    def noVnc(self):
        title = toUnicode(MSG['msg01'])
        message = toUnicode(MSG['msg03'])
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

        Caption = toUnicode(MSG['msg01'])
        fileName = QFileDialog.getOpenFileName(self.dlg, Caption, '', "*.exe")
        if fileName:
            self.vncPath = toUnicode(fileName)

            if self.vncPath:
                self.settings.setValue('vnc_path', self.vncPath)

    def callNTOUHydro_WRA(self):
        if self.vncPath:
            self.dlg.done(0)
            subprocess.Popen([self.vncPath, links[17],
                             '-user', links[18], '-password', links[19]])
            self.dlg.done(0)
        else:
            self.noVnc()

    def callNTOUHydro_author(self):
        os.system('start '+links[20])
        self.dlg.done(0)

    def callSRH1D(self):
        filePath = os.path.join(self.plugin_dir, 'SRH1D_table.xls')
        self.dlg.done(0)
        os.system('"'+filePath+'"')
        os.system("kill -9 %d" % (os.getpid()))
        self.dlg.done(0)

    def callCCHE1D(self):
        infoViewer = infoView(self.iface, 102)
        infoViewer.run()
        path = links[1]
        os.system('start '+path)
        self.dlg.done(0)

    def callCCHE2D(self):
        title = toUnicode(MSG['msg10'])
        selector = netSelector(self.iface, title)
        selector.run()
        self.dlg.done(0)

    def runRESED(self):
        filePath = os.path.join(self.plugin_dir,
                                'RiverSimulation-20160629.exe')
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
        self.dlg.init4.setVisible(True)
        self.dlg.init1D.setText('CCHE1D')
        self.dlg.init2D.setText('CCHE2D')
        self.dlg.init3D.setText('CCHE3D')
        self.dlg.init4.setText('CCHE MESH')

    def callCCHE3D(self):
        os.system('start ' + links[4])

        infoViewer = infoView(self.iface, 103)
        infoViewer.run()
        if self.vncPath:
            self.dlg.done(0)
            subprocess.Popen([self.vncPath, links[17],
                             '-user', links[18], '-password', links[19]])
        else:
            self.noVnc()

        self.dlg.done(0)

    def callCCHE_MESH(self):
        os.system('start ' + links[5])

    def callSRH(self):
        self.dlg.init3D.setVisible(True)
        self.dlg.init1D.setText('SRH-1D')
        self.dlg.init2D.setText('SRH-2D')
        self.dlg.init3D.setText('SRH-3D')
        self.dlg.init4.setVisible(False)

    def callRESED(self):
        self.dlg.init1D.setText('RESED')
        self.dlg.init2D.setText(toUnicode(MSG['msg11']))
        self.dlg.init3D.setText(u'')
        self.dlg.init3D.setEnabled(False)
        self.dlg.init3D.setVisible(False)
        self.dlg.init4.setVisible(False)

    def callSRH2D(self):
        self.dlg.init3D.setVisible(True)
        self.dlg.init4.setVisible(True)
        self.dlg.init1D.setText(toUnicode(MSG['msg14']))
        self.dlg.init2D.setText(toUnicode(MSG['msg15']))
        self.dlg.init3D.setText(toUnicode(MSG['msg16']))
        self.dlg.init4.setText(toUnicode(MSG['msg17']))

        self.dlg.init1D.clicked.disconnect()
        self.dlg.init2D.clicked.disconnect()
        self.dlg.init3D.clicked.disconnect()
        try:
            self.dlg.init4.clicked.disconnect()
        except(TypeError):
            pass

        self.dlg.setWindowTitle('SRH-2D')
        self.dlg.init1D.clicked.connect(self.callMeshBuilder)
        self.dlg.init2D.clicked.connect(self.getMeshBuilder)
        self.dlg.init3D.clicked.connect(self.getTECViewer)
        self.dlg.init4.clicked.connect(self.getImageMagick)

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
        else:
            title = toUnicode(MSG['msg12'])
            message = toUnicode(MSG['msg13'])
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(message)
            msg.setWindowTitle(title)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            os.system('start ' + links[7])

    def callSRH3D(self):
        infoViewer = infoView(self.iface, 104)
        result = infoViewer.run()
        if self.vncPath:
            self.dlg.done(0)
            subprocess.Popen([self.vncPath, links[17],
                             '-user', links[18], '-password', links[19]])
            self.dlg.done(0)
        else:
            self.noVnc()

    def getMeshBuilder(self):
        os.system('start ' + links[7])

    def getTECViewer(self):
        os.system('start ' + links[13])

    def getImageMagick(self):
        os.system('start ' + links[6])

    def run(self):
        result = self.dlg.exec_()
        if result:
            pass
