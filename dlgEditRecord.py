#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui
import dlgEditRecordUI  # Dialog Edit Record UI
import cPhoneBook  # Class PhoneBook
import sqlite3


class DlgEditRecord(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = dlgEditRecordUI.Ui_dlgEditRecord()
        self.ui.setupUi(self)
        self.name = ""
        # for Translation.
        self._translate = QtCore.QCoreApplication.translate

        self.ui.btnAddNumberToList.clicked.connect(self.btnAddNumberToList_clicked)
        self.ui.btnDelSelectedNumbers.clicked.connect(self.btnDelSelectedNumbers_clicked)
        self.ui.btnFinishAndSave.clicked.connect(self.btnFinishAndSave_clicked)
        self.ui.btnCancel.clicked.connect(self.close)
        self.ui.lwdgPhonesForEdit.itemClicked.connect(self.lwdgPhonesForEdit_itemClicked)

        # my event filters.
        self.ui.ledName.installEventFilter(self)
        self.ui.ledPhoneNumber.installEventFilter(self)
        self.ui.lwdgPhonesForEdit.installEventFilter(self)

    # def __del__(self):  # TODO: delete after ALL corrections.
    #     print("DlgEditRecord Class's destructor  called...")

    def createActions(self):
        """ Creates actions. """
        self.actClearList = QtWidgets.QAction(QtGui.QIcon(":/iconsOther/Icons/clear_3.png"),
                                              self._translate("dlgEditRecord", "Очистить список"), self)
        self.actDelSelectedNumbers = QtWidgets.QAction(QtGui.QIcon(":/iconsOneBit/Icons/OneBit/onebit_32.png"),
                                                       self._translate("dlgEditRecord", "Удалить выбранные номера"),
                                                       self)
        self.actFinishAndSave = QtWidgets.QAction(QtGui.QIcon(":/iconsBasic/Icons/BasicSet/save_64.png"),
                                                  self._translate("dlgEditRecord", "Закончить и сохранить"), self)
        self.actCancel = QtWidgets.QAction(QtGui.QIcon(":/iconsBasic/Icons/BasicSet/block_64.png"),
                                           self._translate("dlgEditRecord", "Отмена"), self)

        # actions' connections.
        self.actClearList.triggered.connect(lambda: self.ui.lwdgPhonesForEdit.clear())
        self.actDelSelectedNumbers.triggered.connect(self.btnDelSelectedNumbers_clicked)
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

    @QtCore.pyqtSlot(str, list)
    def fMain_btnDelOrEditCalled(self, name, phonesList):
        """
        My slot for fMain_btnDelOrEditCalled signal.
        Gets the record (name(key)  phonesList(value)).
        :param name:
        :param phonesList:
        """
        self.ui.lwdgPhonesForEdit.clear()
        self.name = name  # save name to self.name for btnFinishAndSave_clicked
        self.ui.ledName.setText(name)
        for phone in phonesList:
            self.ui.lwdgPhonesForEdit.addItem(phone)
        self.ui.lwdgPhonesForEdit.setCurrentRow(0)
        self.ui.ledPhoneNumber.setText(self.ui.lwdgPhonesForEdit.currentItem().text())

    @QtCore.pyqtSlot()  # pass phone to ledPhoneNumber after click in lwdgPhonesForEdit
    def lwdgPhonesForEdit_itemClicked(self):
        # if lwdgPhonesForEdit is NOT empty.
        if self.ui.lwdgPhonesForEdit.count() != 0:
            self.ui.ledPhoneNumber.clear()
            self.ui.ledPhoneNumber.setText(self.ui.lwdgPhonesForEdit.currentItem().text())

    @QtCore.pyqtSlot()
    def btnAddNumberToList_clicked(self):
        """ Adding phone numbers from ledPhoneNumber to the lwdgPhonesForEdit. """
        totalPhones = self.ui.lwdgPhonesForEdit.count()
        # Getting the phoneNumber and check it.
        phoneNumber = self.ui.ledPhoneNumber.text().strip()
        # replace ' to " if entered. For sql requests.
        if "'" in phoneNumber:
            phoneNumber = phoneNumber.replace("'", '"')
        if phoneNumber == "":
            QtWidgets.QMessageBox.information(self,
            self._translate("dlgEditRecord", "Редактирование записи"),
            self._translate("dlgEditRecord", "Необходимо ввести номер телефона."))
            self.ui.ledPhoneNumber.setFocus()
        else:  # add the phone number to the lwdgPhonesForAdd
            # check if the adding phone exists in the lwdgPhonesForAdd.
            isPhoneExists = False
            for i in range(totalPhones):
                self.ui.lwdgPhonesForEdit.setCurrentRow(i)
                if self.ui.lwdgPhonesForEdit.currentItem().text() == phoneNumber:
                    isPhoneExists = True
                    QtWidgets.QMessageBox.warning(self,
                    self._translate("dlgEditRecord", "Редактирование записи"),
                    self._translate("dlgEditRecord", "Номер {} уже есть в списке.".format(phoneNumber)))
                    self.ui.ledPhoneNumber.setFocus()
                    break
            if not isPhoneExists:
                self.ui.lwdgPhonesForEdit.addItem(phoneNumber)
                self.ui.lwdgPhonesForEdit.clearSelection()
                self.ui.ledPhoneNumber.setFocus()

    @QtCore.pyqtSlot()
    def btnDelSelectedNumbers_clicked(self):
        """
        Deleting selected phone for this record.
        """
        totalSelectedItems = 0  # count selected items.
        for _ in self.ui.lwdgPhonesForEdit.selectedItems():
            totalSelectedItems += 1
        if totalSelectedItems == self.ui.lwdgPhonesForEdit.count():  # if all items selected.
            self.ui.lwdgPhonesForEdit.clear()
            self.ui.lwdgPhonesForEdit.setFocus()
        else:  # if selected not all items.
            if self.ui.lwdgPhonesForEdit.currentRow() == -1:  # if no selection.
                QtWidgets.QMessageBox.information(self,
                self._translate("dlgEditRecord", "Редактирование записи"),
                self._translate("dlgEditRecord", "Для удаления выберите номер в списке."))
            else:
                # delete selected phones from selected record.
                for phone in self.ui.lwdgPhonesForEdit.selectedItems():
                    # get rows of deleting phones from lwdgPhonesForEdit.
                    rowItem = self.ui.lwdgPhonesForEdit.row(phone)  # rowItem is int
                    self.ui.lwdgPhonesForEdit.setCurrentRow(rowItem)
                    self.ui.lwdgPhonesForEdit.takeItem(self.ui.lwdgPhonesForEdit.row(phone))

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
            self._translate("dlgEditRecord", "Открытие базы данных"),
            self._translate("dlgEditRecord", "Ошибка при обращении к базе данных."))
        else:
            newPhonesList = []  # phone's list for saving.
            # Checking if the lwdgPhonesForAdd is not empty.
            totalPhones = self.ui.lwdgPhonesForEdit.count()
            if totalPhones == 0:  # lwdgPhonesForEdit is empty.
                QtWidgets.QMessageBox.warning(self,
                self._translate("dlgEditRecord", "Редактирование записи"),
                self._translate("dlgEditRecord", "Список добавляемых номеров пуст.\n"
                                                 "Добавьте хотя бы один номер."))
                self.ui.ledPhoneNumber.setFocus()
            else:  # not empty.
                for idxNumber in range(totalPhones):
                    newPhonesList.append(self.ui.lwdgPhonesForEdit.item(idxNumber).text())
                # get newName (key).
                newName = self.ui.ledName.text().strip()
                # replace ' to " if entered. For sql requests.
                if "'" in newName:
                    newName = newName.replace("'", '"')
                if newName == "":
                    QtWidgets.QMessageBox.warning(self,
                    self._translate("dlgEditRecord", "Редактирование записи"),
                    self._translate("dlgEditRecord", "Необходимо ввести имя."))
                    self.ui.ledName.setFocus()
                # check if the name was changed.
                elif newName == self.name:  # self.name NOT changed.
                    # call funDeleteOldThenInsertNewRecord in the class PhoneBook.
                    try:
                        myPhoneBook.funDeleteOldThenInsertNewRecord(self.name, newName, newPhonesList)
                    except sqlite3.DatabaseError:
                        QtWidgets.QMessageBox.critical(self,
                        self._translate("dlgEditRecord", "Редактирование записи"),
                        self._translate("dlgEditRecord", "Ошибка при редактировании записи."))
                    else:
                        # delete old record with self.name from the myPhoneBook.phoneBook.
                        del myPhoneBook.phoneBook[self.name]
                        # create new record with newName and newPhonesList in the myPhoneBook.phoneBook.
                        myPhoneBook.phoneBook[newName] = newPhonesList
                        QtWidgets.QMessageBox.information(self,
                        self._translate("dlgEditRecord", "Редактирование записи"),
                        self._translate("dlgEditRecord", "Запись успешно отредактирована."))

                        # close the Deleting dialog window.
                        self.close()
                else:  # newName != self.name   => self.name changed.
                    # to avoid duplicates of names in the different case such as John and john.
                    isNameEqualKey = False
                    for key in myPhoneBook.phoneBook.keys():
                        if newName.lower() == str(key).lower():
                            isNameEqualKey = True
                            break
                    # if newName belongs to another record in the myPhoneBook.phoneBook
                    if isNameEqualKey:
                        QtWidgets.QMessageBox.critical(self,
                        self._translate("dlgEditRecord", "Редактирование записи"),
                        self._translate("dlgEditRecord", "Имя {} принадлежит другой записи в справочнике .\n"
                                                                    "Выберите другое имя.".format(newName)))
                    else:  # name CHANGED and doesn't belong another one.
                        # call funDeleteOldThenInsertNewRecord in the class PhoneBook.
                        try:
                            myPhoneBook.funDeleteOldThenInsertNewRecord(self.name, newName, newPhonesList)
                        except sqlite3.DatabaseError:
                            QtWidgets.QMessageBox.critical(self,
                            self._translate("dlgEditRecord", "Редактирование записи"),
                            self._translate("dlgEditRecord", "Ошибка при редактировании записи."))
                        else:
                            # create new record with newName and newPhonesList in the myPhoneBook.phoneBook.
                            myPhoneBook.phoneBook[newName] = newPhonesList
                            # delete old record with self.name from the myPhoneBook.phoneBook.
                            del myPhoneBook.phoneBook[self.name]
                            QtWidgets.QMessageBox.information(self,
                            self._translate("dlgEditRecord", "Редактирование записи"),
                            self._translate("dlgEditRecord", "Запись успешно отредактирована."))

                            # close the Deleting dialog window.
                            self.close()

    def eventFilter(self, obj, e):
        """
        My eventFilter.
        :param obj:
        :param e:
        :return: QtWidgets.QDialog.eventFilter(self, obj, e)
        """
        if obj == self.ui.ledName:
            if e.type() == QtCore.QEvent.KeyPress:
                if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                    self.ui.ledPhoneNumber.setFocus()
                    return True
        if obj == self.ui.ledName:
            if e.type() == QtCore.QEvent.KeyPress:
                if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
                    self.ui.btnAddNumberToList()
                    return True
        if obj == self.ui.lwdgPhonesForEdit:
            if e.type() == QtCore.QEvent.ContextMenu:
                self.createActions()
                self.createMenu()
                self.menu.popup(e.globalPos())
                self.menu.exec_()
                return True
            if e.type() == QtCore.QEvent.KeyPress:
                if e.key() == QtCore.Qt.Key_Delete:
                    self.btnDelSelectedNumbers_clicked()
                    return True
        # pass the event on to the parent class.
        return QtWidgets.QDialog.eventFilter(self, obj, e)
