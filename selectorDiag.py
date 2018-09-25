
import os
from PyQt4 import QtGui, uic
from qgis.PyQt.QtCore import QSettings
from msg import MSG
from toUnicode import toUnicode
import subprocess
from link import links
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
        self.settings = QSettings('ManySplendid', 'HydroModelBanks')

        self.dlg = selectorDiag()
        self.dlg.setWindowTitle(title)
        self.dlg.getTestVer.clicked.connect(self.downLoadTestVer)
        self.dlg.lauchOfficial.clicked.connect(self.lauchVnc)

    def downLoadTestVer(self):
        os.system('start ' + links[2])
        self.dlg.done(0)

    def lauchVnc(self):
        self.dlg.done(0)
        infoViewer = infoView(self.iface, 101)
        result = infoViewer.run()
        if self.settings.value('vnc_path'):
            subprocess.Popen([self.vncPath, links[17],
                              '-user', links[18], '-password', links[19]])
        else:
            QtGui.QMessageBox(QtGui.QMessageBox.critical,
                              title=toUnicode(MSG['msg02']),
                              text=toUnicode(MSG['msg03']))

    def run(self):
        self.dlg.exec_()
