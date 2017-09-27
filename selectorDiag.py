
import os
from PyQt4 import QtGui, uic
import _winreg
import subprocess
from infoDiag import infoView


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'netSelector.ui'))


class selectorDiag(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(selectorDiag, self).__init__(parent)

        self.setupUi(self)


class netSelector:
    def __init__(self, iface, title):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)

        self.dlg = selectorDiag()
        self.dlg.setWindowTitle(title)
        self.dlg.lauchOfficial.clicked.connect(self.lauchVnc)

    def lauchVnc(self):
        self.dlg.done(0)
        infoViewer = infoView(self.iface, 101)
        result = infoViewer.run()
        self.vncPath = ''
        if result:
            try:
                reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
                k = _winreg.OpenKey(
                    reg, r'SOFTWARE\Classes\VncViewer.Config')
                pathKey = _winreg.EnumKey(k, 0)
                pathName = _winreg.QueryValue(k, pathKey)
                pathName = pathName.split(',')[0]
                self.vncPath = pathName
            except:
                infoView(self.iface, 201)

            subprocess.Popen([self.vncPath, '210.69.15.31::5999',
                              '-user', '07-gpu', '-password', '1!qaz2@wsx'])
        else:
            pass

    def run(self):
        self.dlg.exec_()
