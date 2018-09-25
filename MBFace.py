
import os
from PyQt4 import QtGui, uic
from PyQt4.QtCore import QSize


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'meshBuilder.ui'))


class callMBPopUp(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(callMBPopUp, self).__init__(parent)

        self.setupUi(self)


class callMB:
    def __init__(self, iface, MBModuleName):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.dlg = callMBPopUp()
        self.setIcon()
        MB = __import__(str(MBModuleName) + '.meshBuilder')
        self.MeshBuilder = MB

        self.dlg.initMBBtn.clicked.connect(self.initMBDiag)
        self.dlg.initSrhpre.clicked.connect(self.startSrhpre)
        self.dlg.init2dmViewer.clicked.connect(self.startMesh2DViewer)
        self.dlg.initFlipLine.clicked.connect(self.doLineFlip)

    def setIcon(self):
        mbIcon = QtGui.QIcon()
        mbPix = QtGui.QPixmap(os.path.join(self.plugin_dir, 'icons',
                                           'SRH-2D-01.png'))
        mbIcon.addPixmap(mbPix)
        self.dlg.initMBBtn.setIcon(mbIcon)
        self.dlg.initMBBtn.setIconSize(QSize(50, 50))

        preIcon = QtGui.QIcon()
        prePix = QtGui.QPixmap(os.path.join(self.plugin_dir, 'icons',
                                            'SRHPRP UI-1-01.png'))
        preIcon.addPixmap(prePix)
        self.dlg.initSrhpre.setIcon(preIcon)
        self.dlg.initSrhpre.setIconSize(QSize(50, 50))

        viewerIcon = QtGui.QIcon()
        viewerPix = QtGui.QPixmap(os.path.join(self.plugin_dir, 'icons',
                                               '2DM-VIEWER-01.png'))
        viewerIcon.addPixmap(viewerPix)
        self.dlg.init2dmViewer.setIcon(viewerIcon)
        self.dlg.init2dmViewer.setIconSize(QSize(50, 50))

        flipIcon = QtGui.QIcon()
        flipPix = QtGui.QPixmap(os.path.join(self.plugin_dir, 'icons',
                                             'FLIP LINE-01.png'))
        flipIcon.addPixmap(flipPix)
        self.dlg.initFlipLine.setIcon(flipIcon)
        self.dlg.initFlipLine.setIconSize(QSize(50, 50))

    def initMBDiag(self):
        meshBuilder = self.MeshBuilder
        MBinterface = meshBuilder.meshBuilder.meshBuilder(self.iface)
        self.dlg.done(0)
        MBinterface.run()

    def startSrhpre(self):
        meshBuilder = self.MeshBuilder
        srhUI = meshBuilder.srhpre.shepred.shepred(self.iface)
        self.dlg.done(0)
        srhUI.run()

    def startMesh2DViewer(self):
        meshBuilder = self.MeshBuilder
        viewerUI = meshBuilder.mesh2DViewer.mesh2DView(self.iface)
        self.dlg.done(0)
        viewerUI.run()

    def doLineFlip(self):
        meshBuilder = self.MeshBuilder
        meshBuilder.lineFlip.flip()

    def run(self):
        result = self.dlg.exec_()
        if result:
            pass
