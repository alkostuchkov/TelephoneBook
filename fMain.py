#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui
import fMainUI  # Main Form UI
import dlgAddRecords  # Class DlgAddRecords
import dlgEditRecord  # Class DlgEditRecord
import cPhoneBook  # Class PhoneBook
import dlgAbout  # Class DlgAbout
import os
import sqlite3


class MyWindow(QtWidgets.QMainWindow):
    # my SIGNAL when btnDelRecord or btnEditRecord clicked for passing name and list of phones.
    delOrEditCalled = QtCore.pyqtSignal(str, list)
    # my SIGNALs when lblZoomIn and lblZoomOut clicked.
    lblZoomInClicked = QtCore.pyqtSignal()
    lblZoomOutClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = fMainUI.Ui_fMain()
        self.ui.setupUi(self)
        self.name = ""
        self.__totalRecords = 0
        self.__selectedRecords = 0
        self.__foundRecords = 0
        self.__isLedSearchConnected = False
        self.__fontSize = 12
        self.__fontFamily = self.ui.lwdgOutput.font().family()  # "Lucida Console"

        # for Translation.
        # self.qtbasetranslator = QtCore.QTranslator()
        self.translator = QtCore.QTranslator()
        self._translate = QtCore.QCoreApplication.translate
        self.ui.cbxLanguage.currentIndexChanged.connect(self.cbxLanguage_currentIndexChanged)
        self.ui.cbxLanguage.setCurrentIndex(-1)  # for translator.

        # createActions and Menu are in the function eventFilter (for translator).
        self.retranslateUi()  # asingnment for statusBar.
        self.createStatusBar()

        # using QSettings for save and restore app settings.
        self.settings = QtCore.QSettings(os.getcwd() + os.path.sep + "config.ini",
                                         QtCore.QSettings.IniFormat)
        # self.loadSettings()

        # connections.
        self.ui.btnAddRecords.clicked.connect(self.btnAddRecords_clicked)
        self.ui.btnDelSelectedRecords.clicked.connect(self.btnDelSelectedRecords_clicked)
        self.ui.btnEditRecord.clicked.connect(self.btnEditRecord_clicked)
        self.ui.btnShowAllRecords.clicked.connect(self.btnShowAllRecords_clicked)
        self.ui.btnCleanAll.clicked.connect(self.btnCleanAll_clicked)
        self.ui.btnExit.clicked.connect(self.btnExit_clicked)

        self.ui.lwdgOutput.currentRowChanged.connect(self.lwdgOutput_currentRowChanged)
        self.ui.lwdgOutput.itemSelectionChanged.connect(self.lwdgOutput_itemSelectionChanged)

        # for zoom font in the lwdgOutput.
        self.lblZoomInClicked.connect(self.lblZoomIn_clicked)
        self.lblZoomOutClicked.connect(self.lblZoomOut_clicked)

        # install my event filters.
        self.ui.lwdgOutput.installEventFilter(self)
        self.ui.ledSearch.installEventFilter(self)
        self.ui.btnAddRecords.installEventFilter(self)
        self.ui.btnDelSelectedRecords.installEventFilter(self)
        self.ui.btnEditRecord.installEventFilter(self)
        self.ui.btnShowAllRecords.installEventFilter(self)
        self.ui.btnCleanAll.installEventFilter(self)
        self.ui.btnExit.installEventFilter(self)
        self.ui.lblZoomIn.installEventFilter(self)
        self.ui.lblZoomOut.installEventFilter(self)

        self.loadSettings()
        # show all records when starting.
        self.btnShowAllRecords_clicked()

    def retranslateUi(self):
        """
        Translates strings and components that cannot be initialized
        because they are initialize in the constructor.
        """
        # strings for statusBar (for translator).
        self.sTotalRecords = self._translate("fMain", " Количество записей в словаре: ")
        self.sSelectedRecords = self._translate("fMain", " Выбрано: ")
        self.sFoundRecords = self._translate("fMain", " Найдено: ")
        
        self.ui.lblTotalRecords.setText(self.sTotalRecords + str(self.__totalRecords))
        self.ui.lblFoundRecords.setText(self.sFoundRecords + str(self.__foundRecords))
        self.ui.lblSelectedRecords.setText(self.sSelectedRecords + str(self.__selectedRecords))

    def createStatusBar(self):
        """ Creates statusbar and components for its. """
        # # get strings for statusBar (for translator).
        # self.retranslateUi()

        # self.ui.lblTotalRecords.setText(self.sTotalRecords + str(self.__totalRecords))
        # self.ui.lblFoundRecords.setText(self.sFoundRecords + str(self.__foundRecords))
        # self.ui.lblSelectedRecords.setText(self.sSelectedRecords + str(self.__selectedRecords))

        # creare widget and add ui.lblTotalRecords, ui.lblSelectedRecords
        # and ui.lblFoundRecords into the widget.
        widget = QtWidgets.QWidget(self)
        widget.setLayout(QtWidgets.QHBoxLayout())
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding)
        widget.layout().addWidget(self.ui.lblTotalRecords)
        widget.layout().addSpacerItem(spacerItem)
        widget.layout().addWidget(self.ui.lblSelectedRecords)
        widget.layout().addSpacerItem(spacerItem)
        widget.layout().addWidget(self.ui.lblFoundRecords)
        widget.layout().addSpacerItem(spacerItem)

        # add widget with 3 labels and ui.btnExit into the statusBar.
        self.stBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.stBar)
        self.stBar.addPermanentWidget(widget, 3)
        self.stBar.addPermanentWidget(self.ui.btnExit, 1)

    def createActions(self):
        """ Creates actions. """
        self.actAddRecord = QtWidgets.QAction(QtGui.QIcon(":/iconsC9d/Icons/C9d/group_add.png"),
                                              self._translate("fMain", "Добавить записи"), self)
        self.actEditRecord = QtWidgets.QAction(QtGui.QIcon(":/iconsOneBit/Icons/OneBit/onebit_20.png"),
                                              self._translate("fMain", "Редактировать запись"), self)
        self.actDelSelectedRecords = QtWidgets.QAction(QtGui.QIcon(":/iconsC9d/Icons/C9d/group_delete.png"),
                                                       self._translate("fMain", "Удалить выбранные записи"), self)
        self.actShowAllRecords = QtWidgets.QAction(QtGui.QIcon(":/iconsC9d/Icons/C9d/group.png"),
                                                   self._translate("fMain", "Вывести весь справочник"), self)
        self.actAboutQt = QtWidgets.QAction(QtGui.QIcon(":/iconsOther/Icons/Qt.png"),
                                            self._translate("fMain", "О Qt"), self)
        self.actAbout = QtWidgets.QAction(QtGui.QIcon(":/iconsOther/Icons/appIcon.ico"),
                                          self._translate("fMain", "О программе"), self)
        self.actExit = QtWidgets.QAction(QtGui.QIcon(":/iconsOneBit/Icons/OneBit/onebit_33.png"),
                                         self._translate("fMain", "Выход"), self)

        # actions' connections.
        self.actAddRecord.triggered.connect(self.btnAddRecords_clicked)
        self.actEditRecord.triggered.connect(self.btnEditRecord_clicked)
        self.actDelSelectedRecords.triggered.connect(self.btnDelSelectedRecords_clicked)
        self.actShowAllRecords.triggered.connect(self.btnShowAllRecords_clicked)
        self.actAboutQt.triggered.connect(lambda: QtWidgets.QMessageBox.aboutQt(self, self._translate("fMain", "О Qt")))
        self.actAbout.triggered.connect(self.actAbout_triggered)
        self.actExit.triggered.connect(self.btnExit_clicked)

    def createMenu(self):
        """ Creates context menu. """
        self.menu = QtWidgets.QMenu(self)
        self.menu.setCursor(QtCore.Qt.PointingHandCursor)
        self.menu.addAction(self.actAddRecord)
        self.menu.addAction(self.actDelSelectedRecords)
        self.menu.addAction(self.actEditRecord)
        self.menu.addAction(self.actShowAllRecords)
        self.menu.addSeparator()
        self.menu.addAction(self.actAbout)
        self.menu.addAction(self.actAboutQt)
        self.menu.addSeparator()
        self.menu.addAction(self.actExit)

    def saveSettings(self):
        """
        Save app's settings to the file: config.ini.
        """
        self.settings.beginGroup("Language")
        self.settings.setValue("CurrentLanguage", self.ui.cbxLanguage.currentIndex())
        self.settings.endGroup()

        self.settings.beginGroup("lwdgOutput")
        self.settings.setValue("FontSize", self.ui.lwdgOutput.font().pointSize())
        self.settings.endGroup()

        self.settings.beginGroup("Splitter")
        self.settings.setValue("splitterSizes", self.ui.splitter.saveState())
        self.settings.endGroup()

    def loadSettings(self):
        """
        Load app's settings from the file: config.ini.
        """
        self.settings.beginGroup("Language")
        self.ui.cbxLanguage.setCurrentIndex(self.settings.value("CurrentLanguage", 0, type=int))
        self.settings.endGroup()

        self.settings.beginGroup("lwdgOutput")
        fontSize = self.settings.value("FontSize", 12, type=int)
        font = QtGui.QFont(self.__fontFamily, fontSize)
        self.ui.lwdgOutput.setFont(font)
        self.settings.endGroup()

        self.settings.beginGroup("Splitter")
        splitterSizesDefault = b'\x00\x00\x00\xff\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x01\x00\x00\x00\x00\xf8\x01\xff\xff\xff\xff\x01\x00\x00\x00\x01\x00'
        self.ui.splitter.restoreState(self.settings.value("splitterSizes", splitterSizesDefault))
        self.settings.endGroup()

    @QtCore.pyqtSlot()
    def lwdgOutput_currentRowChanged(self):
        """
        Get self.name (key) by method currentRowChanged in the lwdgOutput.
        """
        # get all record as a string.
        if self.ui.lwdgOutput.currentRow() != -1:  # avoid empty self.name (= "").
            text = self.ui.lwdgOutput.currentItem().text()
            i = text.find(":\n")  # Name:\n
            # get self.name (need for btnEditRecord_clicked).
            self.name = text[:i]

    @QtCore.pyqtSlot()
    def lwdgOutput_itemSelectionChanged(self):
        """ Shows quantity of selection items in the lwdgOutput. """
        self.__selectedRecords = len(self.ui.lwdgOutput.selectedItems())
        self.ui.lblSelectedRecords.setText(self.sSelectedRecords + str(self.__selectedRecords))

    @QtCore.pyqtSlot()
    def btnAddRecords_clicked(self):
        """  Create the instance of DlgAddRecord Class and show it. """
        addRecDialog = dlgAddRecords.DlgAddRecords()
        addRecDialog.exec_()
        # Show all records in the Main Form after adding records.
        self.btnShowAllRecords_clicked()

    @QtCore.pyqtSlot()
    def btnDelSelectedRecords_clicked(self):
        """ Deleting selected records from the phoneBook. """
        # check if the record is selected
        if self.ui.lwdgOutput.currentRow() == -1:  # no selection.
            QtWidgets.QMessageBox.warning(self,
            self._translate("fMain", "Удаление записи"),
            self._translate("fMain", "Нечего удалять.\n"
                                     "Для удаления выберите запись в списке."))
            self.ui.lwdgOutput.setFocus()
        else:  # is selected.
            # Create myPhoneBook INSTANCE and load data from the db.
            myPhoneBook = cPhoneBook.PhoneBook()
            try:  # open db and get dict.
                myPhoneBook.funOpenDbAndGetDict()
            except sqlite3.DatabaseError:
                QtWidgets.QMessageBox.critical(self,
                self._translate("fMain", "Открытие базы данных"),
                self._translate("fMain", "Ошибка при обращении к базе данных."))
            else:
                # get namesList with names for deleting from every selected row.
                namesList = []  # list of names from selected rows in the lwdgOutput.
                # get all record as a string.
                for record in self.ui.lwdgOutput.selectedItems():
                    text = record.text()
                    i = text.find(":\n")  # Name:\n
                    # append name to the namesList.
                    namesList.append(text[:i])

                btnReply = QtWidgets.QMessageBox.warning(self,
                           self._translate("fMain", "Удаление записи"),
                           self._translate("fMain", "Вы уверены что хотите удалить выбранные записи?"),
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if btnReply == QtWidgets.QMessageBox.Yes:
                    try:  # call funMultiRecordDeleting in the class PhoneBook.
                        myPhoneBook.funMultiRecordDeleting(namesList)
                    except sqlite3.DatabaseError:
                        QtWidgets.QMessageBox.critical(self,
                        self._translate("fMain", "Удаление записи"),
                        self._translate("fMain", "Ошибка при удалении."))
                    else:  # delete from the dict myPhoneBook.phoneBook.
                        del myPhoneBook.phoneBook[self.name]
                        QtWidgets.QMessageBox.information(self,
                        self._translate("fMain", "Удаление записи"),
                        self._translate("fMain", "Удаление прошло успешно."))
                # Show all records in the Main Form after deleting records.
                self.btnShowAllRecords_clicked()

    @QtCore.pyqtSlot()
    def btnEditRecord_clicked(self):
        """  Create the instance of DlgEditRecord Class and show it. """
        # check if there is multi selection in the ldwgOutput
        if len(self.ui.lwdgOutput.selectedItems()) > 1:
            QtWidgets.QMessageBox.warning(self,
            self._translate("fMain", "Редактирование записи"),
            self._translate("fMain", "Вы не можете редактировать\nнесколько записей одновременно.\n"
                                     "Выберите одну запись."))
        else:
            # check if the record is selected
            totalPhones = self.ui.lwdgOutput.count()
            if totalPhones == 0:  # lwdgPhonesForAdd is empty.
                QtWidgets.QMessageBox.warning(self,
                self._translate("fMain", "Редактирование записи"),
                self._translate("fMain", "Нечего редактировать.\n"
                                             "Выберите 'Вывести весь справочник' в главном окне."))
                self.ui.btnShowAllRecords.setFocus()
            elif self.ui.lwdgOutput.currentRow() == -1:  # or no selection.
                QtWidgets.QMessageBox.warning(self,
                self._translate("fMain", "Редактирование записи"),
                self._translate("fMain", "Нечего редактировать.\n"
                                              "Для редактирования выберите запись в списке."))
                self.ui.lwdgOutput.setFocus()
            else:  # is selected.
                # Create myPhoneBook INSTANCE and load data from the db.
                myPhoneBook = cPhoneBook.PhoneBook()
                try:  # open db and get dict.
                    myPhoneBook.funOpenDbAndGetDict()
                except sqlite3.DatabaseError:
                    QtWidgets.QMessageBox.critical(self,
                    self._translate("fMain", "Открытие базы данных"),
                    self._translate("fMain", "Ошибка при обращении к базе данных."))
                else:
                    # self.name was got in slot lwdgOutput_currentRowChanged.
                    # create instance of DlgEditRecord.
                    editRecDialog = dlgEditRecord.DlgEditRecord()
                    # connect fMain signal with dlgEditRecord.
                    self.delOrEditCalled.connect(editRecDialog.fMain_btnDelOrEditCalled)
                    # emit SIGNAL delOrEditCalled (pass: name and list of phones for this name).
                    self.delOrEditCalled.emit(self.name, myPhoneBook.phoneBook[self.name])
                    editRecDialog.exec_()

        # Show all records in the Main Form after edition.
        self.btnShowAllRecords_clicked()

    @QtCore.pyqtSlot()
    def btnShowAllRecords_clicked(self):
        """ Show all records. """
        # Create myPhoneBook INSTANCE and load data from the db.
        myPhoneBook = cPhoneBook.PhoneBook()
        try:  # open db and get dict.
            myPhoneBook.funOpenDbAndGetDict()
        except sqlite3.DatabaseError:
            QtWidgets.QMessageBox.critical(self,
            self._translate("fMain", "Открытие базы данных"),
            self._translate("fMain", "Ошибка при обращении к базе данных."))
        else:
            self.__totalRecords = len(myPhoneBook.phoneBook)
            self.ui.lblTotalRecords.setText(self.sTotalRecords + str(self.__totalRecords))
            self.__foundRecords = 0
            self.ui.lblFoundRecords.setText(self.sFoundRecords + str(self.__foundRecords))
            # check if the cPhoneBook.PhoneBook is empty.
            if len(myPhoneBook.phoneBook) == 0:
                QtWidgets.QMessageBox.warning(self,
                self._translate("fMain", "Показать все записи"),
                self._translate("fMain", "Ваш телефонный справочник пуст.\n"
                                         "Выберите 'Добавить запись' в главном окне для добавления записей."))
                self.ui.btnAddRecords.setFocus()
            else:
                self.ui.lwdgOutput.clear()
                outputStr = ""
                for key in sorted(myPhoneBook.phoneBook):
                    outputStr = str(key) + ":\n"
                    phonesStr = ""
                    for phoneNum in myPhoneBook.phoneBook[key]:
                        phonesStr += " " * (len(key) + 1) + phoneNum + "\n"
                    outputStr += phonesStr  # [:-1]  # Delete last "\n"
                    self.ui.lwdgOutput.addItem(outputStr)
            # The INSTANCE of myPhoneBook, created in the beginning
            # of this method is destroying here!!!

    @QtCore.pyqtSlot(str)  # search...
    def ledSearch_textChanged(self, findingText):
        """
        Get findingText from the ledSearch signal textChanged
        and create outputPhoneBook of search's results.
        """
        # Create myPhoneBook INSTANCE and load data from the db.
        myPhoneBook = cPhoneBook.PhoneBook()
        try:  # open db and get dict.
            myPhoneBook.funOpenDbAndGetDict()
        except sqlite3.DatabaseError:
            QtWidgets.QMessageBox.critical(self,
            self._translate("fMain", "Открытие базы данных"),
            self._translate("fMain", "Ошибка при обращении к базе данных."))
        else:
            # check if the cPhoneBook.PhoneBook is empty.
            if len(myPhoneBook.phoneBook) == 0:
                QtWidgets.QMessageBox.warning(self,
                self._translate("fMain", "Поиск"),
                self._translate("fMain", "Ваш телефонный справочник пуст.\n"
                                         "Выберите 'Добавить запись' в главном окне для добавления записей."))
                self.ui.lwdgOutput.setFocus()
            else:  # search in the names and in the phone numbers.
                whatFind = findingText.strip().lower()
                outputPhoneBook = dict()  # dict() will contain all results of searcing.
                for key in sorted(myPhoneBook.phoneBook):
                    if whatFind in key.lower() or whatFind in ", ".join(myPhoneBook.phoneBook[key]):
                        outputPhoneBook[key] = myPhoneBook.phoneBook[key]
                self.showSearchResults(outputPhoneBook)

    def showSearchResults(self, outputPhoneBook):
        """ Show results of searching. """
        self.ui.lwdgOutput.clear()
        outputStr = ""
        for key in sorted(outputPhoneBook):
            outputStr = str(key) + ":\n"
            phonesStr = ""
            for phoneNum in outputPhoneBook[key]:
                phonesStr += " " * (len(key) + 1) + phoneNum + "\n"
            outputStr += phonesStr  # [:-1]  # Delete last "\n"
            self.ui.lwdgOutput.addItem(outputStr)
        # show result's quantity.
        if self.ui.ledSearch.text().strip() != "":
            self.__foundRecords = len(outputPhoneBook)
            self.ui.lblFoundRecords.setText(self.sFoundRecords + str(self.__foundRecords))
        else:
            self.__foundRecords = 0
            self.ui.lblFoundRecords.setText(self.sFoundRecords + str(self.__foundRecords))


    @QtCore.pyqtSlot()
    def btnCleanAll_clicked(self):
        """ Clear PhoneBook deleting ALL records. """
        # Create myPhoneBook INSTANCE and load data from the db.
        myPhoneBook = cPhoneBook.PhoneBook()
        try:  # open db and get dict.
            myPhoneBook.funOpenDbAndGetDict()
        except sqlite3.DatabaseError:
            QtWidgets.QMessageBox.critical(self,
            self._translate("fMain", "Открытие базы данных"),
            self._translate("fMain", "Ошибка при обращении к базе данных."))
        else:
            # check if the PhoneBook is already empty.
            if len(myPhoneBook.phoneBook) != 0:  # NOT empty.
                btnReply = QtWidgets.QMessageBox.critical(self,
                self._translate("fMain", "Удаление ВСЕХ записей из справочника"),
                self._translate("fMain", "Данное действие удалить ВСЕ записи из справочника безвозвратно.\n"
                                         "Вы точно уверены, что хотите этого?"),
                                         QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                         QtWidgets.QMessageBox.No)
                if btnReply == QtWidgets.QMessageBox.Yes:
                    try:
                        myPhoneBook.funClearDb()
                    except sqlite3.DatabaseError:
                        QtWidgets.QMessageBox.critical(self,
                        self._translate("fMain", "Открытие базы данных"),
                        self._translate("fMain", "Ошибка при обращении к базе данных."))
                    else:
                        myPhoneBook.phoneBook.clear()
                        self.ui.lwdgOutput.clear()
                        QtWidgets.QMessageBox.information(self,
                        self._translate("fMain", "Удаление записи"),
                        self._translate("fMain", "Все записи успешно удалены из справочника."))
            else:  # IS already empty.
                QtWidgets.QMessageBox.information(self,
                self._translate("fMain", "Удаление записи"),
                self._translate("fMain", "Ваш справочник уже пуст."))
            self.btnShowAllRecords_clicked()

    @QtCore.pyqtSlot()
    def btnExit_clicked(self):
        """ Close the application. """
        self.close()
        # QtWidgets.qApp.quit()

    @QtCore.pyqtSlot()
    def actAbout_triggered(self):
        """  Create the instance of DlgAbout Class and show it. """
        dlgAboutProg = dlgAbout.DlgAbout()
        dlgAboutProg.exec_()

    @QtCore.pyqtSlot()
    def lblZoomIn_clicked(self):
        """ Magnify lwdgOutput font. """
        fontSize = self.ui.lwdgOutput.font().pointSize()
        fontSize += 1
        font = QtGui.QFont(self.__fontFamily, fontSize)
        # font.setBold(True)
        self.ui.lwdgOutput.setFont(font)

    @QtCore.pyqtSlot()
    def lblZoomOut_clicked(self):
        """ Minify lwdgOutput font. """
        fontSize = self.ui.lwdgOutput.font().pointSize()
        fontSize -= 1
        font = QtGui.QFont(self.__fontFamily, fontSize)
        # font.setBold(True)
        self.ui.lwdgOutput.setFont(font)

    @QtCore.pyqtSlot(int)
    def cbxLanguage_currentIndexChanged(self, index):
        """
        Change language by choosing in the cbxLanguage.
        :param index:
        """
        if index == 0:
            self.translator.load(":/lang/qtbase_ru")  # for QMessageBox and ... translator.
            # self.translator.load(":/lang/phoneBook_ru")
        elif index == 1:
            self.translator.load(":/lang/phoneBook_en")
            # self.qtbasetranslator.load(":lang/qtbase_en")
        QtWidgets.QApplication.installTranslator(self.translator)
        # QtWidgets.QApplication.installTranslator(self.qtbasetranslator)

    # events.
    def changeEvent(self, e):
        """
        Retranslate the app when called event LanguageChange.
        :param e:
        """
        if e.type() == QtCore.QEvent.LanguageChange:
            self.ui.retranslateUi(self)
            self.retranslateUi()  # my function.
            self.ui.lwdgOutput.setFocus()
        else:
            QtWidgets.QWidget.changeEvent(self, e)

    def keyPressEvent(self, e):
        """
        Override methon in QWidget.
        On Key_Escape press - Quit.
        :param e: event
        :return QtWidgets.QWidget.keyPressEvent(self, e):
        """
        if e.type() == QtCore.QEvent.KeyPress:
            if e.key() == QtCore.Qt.Key_Escape:
                self.close()

    def eventFilter(self, obj, e):
        """
        My events for ledSearch and buttons.
        :param obj:
        :param e:
        :return QtWidgets.QWidget.eventFilter(self, obj, e):
        """
        if obj == self.ui.ledSearch:
            if e.type() == QtCore.QEvent.MouseButtonPress:
                if e.button() == QtCore.Qt.LeftButton:
                    self.ledSearch_focusIn()
                    return True
            elif e.type() == QtCore.QEvent.FocusIn:
                self.ledSearch_focusIn()
                return True
            elif e.type() == QtCore.QEvent.FocusOut:
                self.ledSearch_focusOut()
                return True
        elif obj == self.ui.lwdgOutput:  # context menu on right button click.
            if e.type() == QtCore.QEvent.ContextMenu:
                self.createActions()
                self.createMenu()
                self.menu.popup(e.globalPos())  # , self.actAboutQt)  # cursor on actAboutQt
                self.menu.exec_()
                return True
            if e.type() == QtCore.QEvent.KeyPress:  # delete by pressing key 'delete'.
                if e.key() == QtCore.Qt.Key_Delete:
                    self.btnDelSelectedRecords_clicked()
                    return True
                # magnify and minify font size in the lwdgOutputg.
                if e.modifiers() & QtCore.Qt.ControlModifier:  # by ctrl+(=/-)
                    if e.key() == QtCore.Qt.Key_Equal:
                        self.lblZoomIn_clicked()
                    elif e.key() == QtCore.Qt.Key_Minus:
                        self.lblZoomOut_clicked()
                    return True
            if e.type() == QtCore.QEvent.Wheel:
                if e.modifiers() & QtCore.Qt.ControlModifier:  # by ctrl+mouseWheel
                    if e.angleDelta().y() > 0:
                        self.lblZoomIn_clicked()
                    else:
                        self.lblZoomOut_clicked()
                    return True
        elif obj == self.ui.btnAddRecords:
            if e.type() == QtCore.QEvent.KeyPress:
                if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                    self.btnAddRecords_clicked()
                    return True
        elif obj == self.ui.btnDelSelectedRecords:
            if e.type() == QtCore.QEvent.KeyPress:
                if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                    self.btnDelSelectedRecords_clicked()
                    return True
        elif obj == self.ui.btnEditRecord:
            if e.type() == QtCore.QEvent.KeyPress:
                if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                    self.btnEditRecord_clicked()
                    return True
        elif obj == self.ui.btnShowAllRecords:
            if e.type() == QtCore.QEvent.KeyPress:
                if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                    self.btnShowAllRecords_clicked()
                    return True
        elif obj == self.ui.btnCleanAll:
            if e.type() == QtCore.QEvent.KeyPress:
                if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                    self.btnCleanAll_clicked()
                    return True
        elif obj == self.ui.btnExit:
            if e.type() == QtCore.QEvent.KeyPress:
                if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                    self.btnExit_clicked()
        # emit signal clicked on the lblZoomIn and lblZoomOut.
        elif obj == self.ui.lblZoomIn:
            if e.type() == QtCore.QEvent.MouseButtonPress:
                if e.buttons() & QtCore.Qt.LeftButton:
                    self.lblZoomInClicked.emit()
                    return True
        elif obj == self.ui.lblZoomOut:
            if e.type() == QtCore.QEvent.MouseButtonPress:
                if e.buttons() & QtCore.Qt.LeftButton:
                    self.lblZoomOutClicked.emit()
                    return True
        # pass the event on to the parent class.
        return QtWidgets.QWidget.eventFilter(self, obj, e)



    # def wheelEvent(self, e):
    #     if e.modifiers() & QtCore.Qt.ControlModifier:  # by ctrl+mouseWheel
    #         if e.angleDelta().y() > 0:
    #             print("wheelEvent +++")
    #             # self.lblZoomIn_clicked()
    #         else:
    #             print("wheelEvent ---")
    #             # self.lblZoomOut_clicked()
    #         e.accept()
    #         return
    #     QtWidgets.QWidget.wheelEvent(self, e)



    def ledSearch_focusIn(self):
        """
        Do when ledSearch got focus.
        """
        # Create myPhoneBook INSTANCE and load data from the db.
        myPhoneBook = cPhoneBook.PhoneBook()
        try:  # open db and get dict.
            myPhoneBook.funOpenDbAndGetDict()
        except sqlite3.DatabaseError as err:
            QtWidgets.QMessageBox.critical(self,
            self._translate("fMain", "Открытие базы данных"),
            self._translate("fMain", "Ошибка при обращении к базе данных."))
        else:
            if len(myPhoneBook.phoneBook) != 0:
                # connect signal & slot when ledSearch left mouse button clicked.
                self.ui.ledSearch.textChanged.connect(self.ledSearch_textChanged)  # searching...
                self.__isLedSearchConnected = True
                self.ui.ledSearch.clear()
                # font = QtGui.QFont(self.__fontFamily, 12, QtGui.QFont.Bold)
                font = QtGui.QFont(self.__fontFamily, self.__fontSize, QtGui.QFont.Normal)
                self.ui.ledSearch.setFont(font)

    def ledSearch_focusOut(self):
        """
        Do when ledSearch lost focus.
        """
        # disconnect signal and slot when editingFinished.
        if self.__isLedSearchConnected:
            self.ui.ledSearch.textChanged.disconnect(self.ledSearch_textChanged)  # searching...
            self.__isLedSearchConnected = False

        self.ui.ledSearch.clear()
        font = QtGui.QFont(self.__fontFamily, self.__fontSize)
        font.setItalic(True)
        # font.setBold(True)
        font.setBold(False)
        self.ui.ledSearch.setFont(font)
        self.ui.ledSearch.setText(self._translate("fMain", "Поиск..."))

    def closeEvent(self, e):
        """
        Save settings before close app.
        :param e:
        """
        self.saveSettings()


if __name__ == "__main__":
    import sys
    import time
    app = QtWidgets.QApplication(sys.argv)

    splashPix = QtGui.QPixmap(":/iconsOther/Icons/splashScreen.png")
    splashScreen = QtWidgets.QSplashScreen(splashPix)  # , QtCore.Qt.WindowStaysOnTopHint)
    # splashScreen.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
    # splashScreen.setEnabled(False)
    #
    # progressBar = QtWidgets.QProgressBar(splashScreen)
    # progressBar.setMaximum(10)
    # progressBar.setGeometry(0, splashPix.height() - 50, splashPix.width(), 20)

    splashScreen.show()
    # splashScreen.showMessage("\n\n\n\n                        Hello, PhoneBook", QtCore.Qt.AlignLeft, QtCore.Qt.white)

    # for i in range(1, 11):
    #     progressBar.setValue(i)
    #     t = time.time()
    #     while time.time() < t + 0.1:
    #         app.processEvents()  # deliver accumulated events.

    app.processEvents()  # deliver accumulated events.
    time.sleep(1.0)

    window = MyWindow()
    window.showMaximized()

    splashScreen.finish(window)
    sys.exit(app.exec_())
