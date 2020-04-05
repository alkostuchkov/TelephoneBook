# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlgAboutUI_ru.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dlgAbout(object):
    def setupUi(self, dlgAbout):
        dlgAbout.setObjectName("dlgAbout")
        dlgAbout.resize(699, 327)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dlgAbout.sizePolicy().hasHeightForWidth())
        dlgAbout.setSizePolicy(sizePolicy)
        dlgAbout.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        dlgAbout.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/iconsOther/Icons/appIcon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dlgAbout.setWindowIcon(icon)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(dlgAbout)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblAppIcon = QtWidgets.QLabel(dlgAbout)
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setBold(False)
        font.setWeight(50)
        self.lblAppIcon.setFont(font)
        self.lblAppIcon.setText("")
        self.lblAppIcon.setPixmap(QtGui.QPixmap(":/iconsOther/Icons/appIcon.ico"))
        self.lblAppIcon.setScaledContents(True)
        self.lblAppIcon.setObjectName("lblAppIcon")
        self.verticalLayout.addWidget(self.lblAppIcon)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lblProgName = QtWidgets.QLabel(dlgAbout)
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lblProgName.setFont(font)
        self.lblProgName.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.lblProgName.setOpenExternalLinks(False)
        self.lblProgName.setObjectName("lblProgName")
        self.verticalLayout_2.addWidget(self.lblProgName)
        self.lblProgVersion = QtWidgets.QLabel(dlgAbout)
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.lblProgVersion.setFont(font)
        self.lblProgVersion.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.lblProgVersion.setObjectName("lblProgVersion")
        self.verticalLayout_2.addWidget(self.lblProgVersion)
        self.textBrowser = QtWidgets.QTextBrowser(dlgAbout)
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setBold(False)
        font.setWeight(50)
        self.textBrowser.setFont(font)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnClose = QtWidgets.QPushButton(dlgAbout)
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setBold(False)
        font.setWeight(50)
        self.btnClose.setFont(font)
        self.btnClose.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/iconsOneBit/Icons/OneBit/onebit_33.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnClose.setIcon(icon1)
        self.btnClose.setIconSize(QtCore.QSize(32, 32))
        self.btnClose.setObjectName("btnClose")
        self.horizontalLayout.addWidget(self.btnClose)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.retranslateUi(dlgAbout)
        QtCore.QMetaObject.connectSlotsByName(dlgAbout)

    def retranslateUi(self, dlgAbout):
        _translate = QtCore.QCoreApplication.translate
        dlgAbout.setWindowTitle(_translate("dlgAbout", "О PhoneBook"))
        self.lblProgName.setText(_translate("dlgAbout", "PhoneBook"))
        self.lblProgVersion.setText(_translate("dlgAbout", "Версия 1.0.0"))
        self.textBrowser.setHtml(_translate("dlgAbout", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Console\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://noProgramSiteYet/\"><span style=\" text-decoration: underline; color:#0000ff;\">http://noProgramSiteYet/</span></a></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Автор:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Александр Костючков &lt;<a href=\"mailto:alkostuchkov@gmail.com\"><span style=\" text-decoration: underline; color:#0000ff;\">alkostuchkov@gmail.com</span></a>&gt;</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Благодарю за помощь:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Владислав Илюшников &lt;<a href=\"mailto:niglad73@mail.ru\"><span style=\" text-decoration: underline; color:#0000ff;\">niglad73@mail.ru</span></a>&gt;</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.btnClose.setText(_translate("dlgAbout", " Закрыть "))

import res_rc
