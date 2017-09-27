
import os
from PyQt4 import QtGui, uic
from PyQt4.QtGui import QMessageBox
import pickle


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'messageViewer.ui'))


class infoViewerDiag(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(infoViewerDiag, self).__init__(parent)

        self.setupUi(self)


class infoView:
    def __init__(self, iface, head):
        self.iface = iface
        plugin_dir = os.path.dirname(__file__)

        f = open(os.path.join(plugin_dir, 'infoText.lang'))
        self.messageLog = pickle.load(f)

        info = self.messageLog[head]
        title = info['title']
        message = info['detail']
        if head < 200:
            self.dlg = infoViewerDiag()
            self.dlg.setWindowTitle(title.decode('big5'))
            for line in message:
                self.dlg.textBrowser.append(line.decode('big5'))
        elif head > 200:
            self.infoBox(title, message)

    def infoBox(self, title, message):
        title = title.decode('big5')
        _message = ''
        for line in message:
            _message += (line.decode('big5') + '\n')
        _message = _message[:-1]
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(_message)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def run(self):
        result = self.dlg.exec_()
        if result:
            return result
