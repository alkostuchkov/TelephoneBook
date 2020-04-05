#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui
import dlgAddRecordsUI  # Dialog Add Record UI
import cPhoneBook  # Class PhoneBook
import sqlite3


class DlgAddRecords(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = dlgAddRecordsUI.Ui_dlgAddRecords()
        self.ui.setupUi(self)
        self.name = ""
        self.phoneNumber = ""
        # for Translation.
        self._translate = QtCore.QCoreApplication.translate

        self.ui.btnAddNumberToList.clicked.connect(self.btnAddNumberToList_clicked)
        self.ui.btnDelNumberFromList.clicked.connect(self.btnDelNumberFromList_clicked)
        self.ui.btnFinishAndSave.clicked.connect(self.btnFinishAndSave_clicked)
        self.ui.btnCancel.clicked.connect(self.close)

        # my event filters.
        self.ui.ledName.installEventFilter(self)
        self.ui.ledPhoneNumber.installEventFilter(self)
        self.ui.lwdgPhonesForAdd.installEventFilter(self)

    # def __del__(self):  # TODO: delete after ALL corrections.
    #     print("DlgAddRecord Class's destructor  called...")

    def createActions(self):
        """ Creates actions. """
        self.actClearList = QtWidgets.QAction(QtGui.QIcon(":/iconsOther/Icons/clear_3.png"),
                                              self._translate("dlgAddRecords", "Очистить список"), self)
        self.actDelSelectedNumbers = QtWidgets.QAction(QtGui.QIcon(":/iconsOneBit/Icons/OneBit/onebit_32.png"),
                                                       self._translate("dlgAddRecords", "Удалить выбранные номера"), self)
        self.actFinishAndSave = QtWidgets.QAction(QtGui.QIcon(":/iconsBasic/Icons/BasicSet/save_64.png"),
                                                       self._translate("dlgAddRecords", "Закончить и сохранить"), self)
        self.actCancel = QtWidgets.QAction(QtGui.QIcon(":/iconsBasic/Icons/BasicSet/block_64.png"),
                                         self._translate("dlgAddRecords", "Отмена"), self)

        # actions' connections.
        self.actClearList.triggered.connect(lambda: self.ui.lwdgPhonesForAdd.clear())
        self.actDelSelectedNumbers.triggered.connect(self.btnDelNumberFromList_clicked)
        self.actFinishAndSave.triggered.connect(self.btnFinishAndSave_clicked)
        self.actCancel.triggered.connect(self.close)

    def createMenu(self):
        """ Creates context menu. """
        self.menu = QtWidgets.QMenu(self)
        self.menu.setCursor(QtCore.Qt.PointingHandCursor)
        self.menu.addAction(self.actClearList)
        self.menu.addAction(self.actDelSelectedNumbers)
        self.menu.addAction(self.actFinishAndSave)
        self.menu.addAction(self.actCancel)

    @QtCore.pyqtSlot()
    def btnAddNumberToList_clicked(self):
        """ Adding phone numbers from ledPhoneNumber to the lwdgPhonesForAdd. """
        totalPhones = self.ui.lwdgPhonesForAdd.count()
        # Getting the phoneNumber and check it.
        self.phoneNumber = self.ui.ledPhoneNumber.text().strip()
        # replace ' to " if entered. For sql requests.
        if "'" in self.phoneNumber:
            self.phoneNumber = self.phoneNumber.replace("'", '"')
        if self.phoneNumber == "":
            QtWidgets.QMessageBox.information(self,
            self._translate("dlgAddRecords", "Добавление записи"),
            self._translate("dlgAddRecords", "Необходимо ввести номер телефона."))
            self.ui.ledPhoneNumber.setFocus()
        else:  # add the phone number to the lwdgPhonesForAdd
            # check if the adding phone exists in the lwdgPhonesForAdd.
            isPhoneExists = False
            for i in range(totalPhones):
                self.ui.lwdgPhonesForAdd.setCurrentRow(i)
                if self.ui.lwdgPhonesForAdd.currentItem().text() == self.phoneNumber:
                    isPhoneExists = True
                    QtWidgets.QMessageBox.warning(self,
                    self._translate("dlgAddRecords", "Добавление записи"),
                    self._translate("dlgAddRecords", "Номер {} уже есть в списке.".format(self.phoneNumber)))
                    self.ui.ledPhoneNumber.setFocus()
                    break
            if not isPhoneExists:
                self.ui.lwdgPhonesForAdd.addItem(self.phoneNumber)
                self.ui.lwdgPhonesForAdd.clearSelection()
                self.ui.ledPhoneNumber.setFocus()

    @QtCore.pyqtSlot()
    def btnDelNumberFromList_clicked(self):
        """ Deleting a wrong number from lwdgPhonesForAdd. """
        totalPhones = self.ui.lwdgPhonesForAdd.count()
        if totalPhones == 0:  # lwdgPhonesForAdd is empty.
            QtWidgets.QMessageBox.warning(self,
            self._translate("dlgAddRecords", "Добавление записи"),
            self._translate("dlgAddRecords", "Нечего удалять.\nСписок добавляемых номеров пуст."))
            self.ui.ledPhoneNumber.setFocus()
        elif self.ui.lwdgPhonesForAdd.currentRow() == -1:  #  or no selection.
            QtWidgets.QMessageBox.warning(self,
            self._translate("dlgAddRecords", "Добавление записи"),
            self._translate("dlgAddRecords", "Для удаления выберите номер в списке."))
        else:  # not empty.
            for item in self.ui.lwdgPhonesForAdd.selectedItems():
                self.ui.lwdgPhonesForAdd.takeItem(self.ui.lwdgPhonesForAdd.row(item))
                # item = None

    @QtCore.pyqtSlot()
    def btnFinishAndSave_clicked(self):
        """
        Save the name and all added numbers from lwdgPhonesForAdd to the PhoneBook
        and then to the file.
        """
        # Create myPhoneBook INSTANCE and load data from the db.
        myPhoneBook = cPhoneBook.PhoneBook()
        try:  # open db and get dict.
            myPhoneBook.funOpenDbAndGetDict()
        except sqlite3.DatabaseError:
            QtWidgets.QMessageBox.critical(self,
            self._translate("dlgAddRecords", "Открытие базы данных"),
            self._translate("dlgAddRecords", "Ошибка при обращении к базе данных."))
        else:
            # Getting the name and check it.
            self.name = self.ui.ledName.text().strip()
            # replace ' to " if entered. For sql requests.
            if "'" in self.name:
                self.name = self.name.replace("'", '"')
            if self.name == "":
                QtWidgets.QMessageBox.warning(self,
                self._translate("dlgAddRecords", "Добавление записи"),
                self._translate("dlgAddRecords", "Необходимо ввести имя."))
                self.ui.ledName.setFocus()
            else:  # != ""
                # to avoid duplicates of names in the different case such as John and john.
                isNameEqualKey = False
                for key in myPhoneBook.phoneBook.keys():
                    if self.name.lower() == str(key).lower():
                        isNameEqualKey = True
                        break
                if isNameEqualKey:
                    QtWidgets.QMessageBox.warning(self,
                    self._translate("dlgAddRecords", "Добавление записи"),
                    self._translate("dlgAddRecords", "Имя {} уже есть в справочнике.\n"
                                                    "Для редактирования нажмите 'Отмена'\nи"
                                                    " выберите в главном окне "
                                                    "'Редактировать запись'.".format(self.name)))
                else:  # name not in myPhoneBook
                    phonesList = []  # list of adding phones to pass to the funInsertIntoDb.
                    # Checking if the lwdgPhonesForAdd is not empty.
                    totalPhones = self.ui.lwdgPhonesForAdd.count()
                    if totalPhones == 0:  # lwdgPhonesForAdd is empty.
                        QtWidgets.QMessageBox.warning(self,
                        self._translate("dlgAddRecords", "Добавление записи"),
                        self._translate("dlgAddRecords", "Список добавляемых номеров пуст.\n"
                                                        "Добавьте хотя бы один номер."))
                        self.ui.ledPhoneNumber.setFocus()
                    else:  # not empty.
                        myPhoneBook.phoneBook[self.name] = []
                        for idxNumber in range(totalPhones):
                            myPhoneBook.phoneBook[self.name].append(self.ui.lwdgPhonesForAdd.item(idxNumber).text())
                            phonesList.append(self.ui.lwdgPhonesForAdd.item(idxNumber).text())
                        # call funInsertIntoDb in the class PhoneBook.
                        try:
                            myPhoneBook.funInsertIntoDb(self.name, phonesList)
                        except sqlite3.DatabaseError:
                            QtWidgets.QMessageBox.critical(self,
                            self._translate("dlgAddRecords", "Добавление записи"),
                            self._translate("dlgAddRecords", "Ошибка при добавлении записи."))
                        else:
                            QtWidgets.QMessageBox.information(self,
                            self._translate("dlgAddRecords", "Добавление записи"),
                            self._translate("dlgAddRecords", "Запись успешно добалена в справочник."))
                            self.ui.lwdgPhonesForAdd.clear()
                            self.ui.ledName.clear()
                            self.ui.ledPhoneNumber.clear()
                            self.ui.ledName.setFocus()

    # my eventFilters.
    def eventFilter(self, obj, e):
        """
        My events for ledName and ledPhoneNumber.
        :param obj:
        :param e:
        :return QtWidgets.QWidget.eventFilter(self, obj, e):
        """
        if obj == self.ui.ledName:
            if e.type() == QtCore.QEvent.KeyPress:
                if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                    self.ui.ledPhoneNumber.setFocus()
                    return True
        elif obj == self.ui.ledPhoneNumber:
            if e.type() == QtCore.QEvent.KeyPress:
                if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                    # add the phone number into the lwdgPhonesForAdd by pressing Enter.
                    self.btnAddNumberToList_clicked()
                    return True
        elif obj == self.ui.lwdgPhonesForAdd:
            if e.type() == QtCore.QEvent.ContextMenu:
                self.createActions()
                self.createMenu()
                self.menu.popup(e.globalPos())
                self.menu.exec_()
                return True
            if e.type() == QtCore.QEvent.KeyPress:
                if e.key() == QtCore.Qt.Key_Delete:
                    self.btnDelNumberFromList_clicked()
                    return True
        # pass the event on to the parent class.
        return QtWidgets.QDialog.eventFilter(self, obj, e)
