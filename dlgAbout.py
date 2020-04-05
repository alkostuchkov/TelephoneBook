#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
import dlgAboutUI  # Dialog About UI


class DlgAbout(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = dlgAboutUI.Ui_dlgAbout()
        self.ui.setupUi(self)
        # for Translation.
        # self._translate = QtCore.QCoreApplication.translate
        self.ui.btnClose.clicked.connect(self.close)
        self.ui.textBrowser.anchorClicked.connect(lambda: print("anchorClicked"))

    # @QtCore.pyqtslot()
    # def slot_anchorClicked(self):
    #     pass
