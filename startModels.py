# -*- coding: big5 -*-

import os
import _winreg
import re
from PyQt4 import QtGui, uic
import qgis.utils
import subprocess
import MBFace
from selectorDiag import netSelector
from PyQt4.QtGui import QMessageBox, QFileDialog
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
        self.readSetting()
        self.dlg = callModelsPopUp()

        try:
            self.vncPath = self.settings['VncViewerPath']
        except:
            try:
                reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
                k = _winreg.OpenKey(
                    reg, r'SOFTWARE\Classes\VncViewer.Config')
                pathKey = _winreg.EnumKey(k, 0)
                pathName = _winreg.QueryValue(k, pathKey)
                pathName = pathName.split(',')[0]
                self.vncPath = pathName
                self.settings.update({'VncViewerPath': self.vncPath})

                f = open(os.path.join(self.plugin_dir, 'settings'), 'w')
                for key in self.settings.keys():
                    f.write(key + ' = ' + self.settings[key] + '\n')
                f.close()
            except:
                self.noVnc()

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
        elif model == 'RESED':
            self.callRESED()
            self.dlg.setWindowTitle('RESED')
            self.dlg.init1D.clicked.connect(self.runRESED)
            self.dlg.init2D.clicked.connect(self.viewRESEDManual)
        else:
            self.callNTOUHydro()
            self.dlg.init1D.clicked.connect(self.callNTOUHydro_WRAP)
            self.dlg.init2D.clicked.connect(self.callNTOUHydro_WRA)
            self.dlg.init3D.clicked.connect(self.callNTOUHydro_author)

    def callNTOUHydro(self):
        self.dlg.init3D.setVisible(True)
        self.dlg.init1D.setText(u'本地端使用\n(限水規所內網域)')
        self.dlg.init2D.setText(u'遠端連線使用\n(限水利署內網域)')
        self.dlg.init3D.setText(u'申請使用權限')

    def readSetting(self):
        try:
            f = open(os.path.join(self.plugin_dir, 'settings'), 'r')
            lines = f.readlines()
            setting = dict()
            for line in lines:
                key = re.split('=', line)[0]
                content = re.split('=', line)[1]
                setting.update({key: content})
            f.close()
            self.settings = setting
        except:
            setting = dict()
            self.settings = setting

    def callNTOUHydro_WRAP(self):
        try:
            batPath = self.settings['NTOUHydro']
            subprocess.Popen([batPath])
        except:
            try:
                reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
                key = _winreg.OpenKey(
                    reg, r'SOFTWARE\Wow6432Node\MicrosoftWindows\CurrentVersion\
Uninstall\QGIS Wien\DisplayIcon')
                pathKey = _winreg.EnumKey(key, 0)
                pathName = _winreg.QueryValue(key, pathKey)

                basePath = os.path.dirname(os.path.dirname(pathName))
                batPath = os.path.join(basePath, 'bin', 'qgis-ltr.bat')

                self.settings.update({'NTOUHydro': batPath})
                f = open(os.path.join(self.plugin_dir, 'settings'), 'w')
                for key in self.settings.keys():
                    f.write(key + ' = ' + self.settings[key] + '\n')
                f.close()

                subprocess.Popen([batPath])
            except:
                title = u'找不到水文水理分析系統'
                message = u'找不到水文水理分析系統\n請先至「申請權限」網頁下載\
軟體'
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(message)
                msg.setWindowTitle(title)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

                Caption = u'請指定水文水理分析系統的執行路徑(qgis-ltr.bat)'
                fileName = QFileDialog.getOpenFileName(self.dlg, Caption, '',
                                                       "*.bat")
                if fileName:
                    self.ntouHydroPath = fileName.encode('big5')
                    self.settings.update({'NTOUHydro': self.ntouHydroPath})

                    f = open(os.path.join(self.plugin_dir, 'settings'), 'w')
                    for key in self.settings.keys():
                        f.write(key + ' = ' + self.settings[key] + '\n')
                    f.close()

    def noVnc(self):
        title = u'找不到VncViewer'
        message = u'找不到已安裝的VncViewer\n請先安裝VncViewer再使用此功能'
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

        Caption = u'請指定UltraVNC Viewer執行檔(vncviewer.exe)的路徑'
        fileName = QFileDialog.getOpenFileName(self.dlg, Caption, '', "*.exe")
        if fileName:
            self.vncPath = fileName.encode('big5')
            self.settings.update({'VncViewerPath': self.vncPath})

            f = open(os.path.join(self.plugin_dir, 'settings'), 'w')
            for key in self.settings.keys():
                f.write(key + ' = ' + self.settings[key] + '\n')
            f.close()

    def callNTOUHydro_WRA(self):
        if self.vncPath:
            self.dlg.done(0)
            subprocess.Popen([self.vncPath, '210.69.15.31::5999',
                             '-user', '07-gpu', '-password', '1!qaz2@wsx'])
            self.dlg.done(0)
        else:
            self.noVnc()

    def callNTOUHydro_author(self):
        os.system('start http://emh-123.wrap.gov.tw/wagis/river/index.html')
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
        infoViewer = infoView(self.iface, 103)
        infoViewer.run()
        if self.vncPath:
            self.dlg.done(0)
            subprocess.Popen([self.vncPath, '210.69.15.31::5999',
                             '-user', '07-gpu', '-password', '1!qaz2@wsx'])
        else:
            self.noVnc()

        self.dlg.done(0)

    def callSRH(self):
        self.dlg.init3D.setVisible(True)
        self.dlg.init1D.setText('SRH-1D')
        self.dlg.init2D.setText('SRH-2D')
        self.dlg.init3D.setText('SRH-3D')

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
        else:
            title = u'請先安裝SRH2D Mesh Builder QGIS插件'
            message = u'SRH2D Mesh Builder插件尚未安裝\n請從關閉視窗後開啟的連\
結下載SRH2D Mesh Builder安裝包'
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(message)
            msg.setWindowTitle(title)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            os.system('start https://drive.google.com/a/manysplendid.com/file/d\
/0BwtvbTG03hXKR3NHeGEyYUl0T0U/view?usp=sharing')

    def callSRH3D(self):
        infoViewer = infoView(self.iface, 104)
        result = infoViewer.run()
        if self.vncPath:
            self.dlg.done(0)
            subprocess.Popen([self.vncPath, '210.69.15.31::5999',
                             '-user', '07-gpu', '-password', '1!qaz2@wsx'])
            self.dlg.done(0)
        else:
            self.noVnc()

    def run(self):
        result = self.dlg.exec_()
        if result:
            pass
