#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ====== PhoneBook for my own using ======
# = Example how my PhoneBook looks like. =
# phoneBook = {
#     "Аптека (ул. Оськина)": ["55-35-77"],
#     "Аптека (ул. Свиридова)": ["45-32-65"],
#     "Аптека (ул. Мазурова)": ["87-43-11"],
#     "Gym (ул. Свиридова)": ["45-32-65"],
#     "Пупкин Вася": ["+375(29) 156-55-33"],
#     "Петя Горшков": ["+375(25) 945-00-11", "53-11-85"]}

import shelve
import os
import sqlite3


class PhoneBook:
    """
    Class PhoneBook for my own using.
    """

    def __init__(self):
        self.phoneBook = {}
        # self.__pathToDB = os.getcwd() + os.path.sep + "Database" + os.path.sep
        self.__pathToDB = os.path.abspath(".") + os.path.sep + "Database" + os.path.sep
        # print(os.path.abspath("."))

    # def __del__(self):  # TODO: delete after ALL corrections.
    #     print("PhoneBook Class's destructor  called...")

    def funOpenDbAndGetDict(self):
        """
        Create database and tables if they not exist.
        Get data from sqlite3 db and transform it into dict self.phoneBook.
        """
        # if dir 'Database' not exists or not a dir, create this.
        if not os.path.exists(self.__pathToDB) or not os.path.isdir(self.__pathToDB):
            os.makedirs(self.__pathToDB)

        conn = sqlite3.connect(self.__pathToDB + "PhoneBook.sqlite3")
        conn.execute("PRAGMA foreign_keys=1")  # enable cascade deleting and updating.
        cur = conn.cursor()
        sql = """\
        CREATE TABLE IF NOT EXISTS names(
           id INTEGER PRIMARY KEY NOT NULL,
           name TEXT UNIQUE NOT NULL COLLATE NOCASE
        );
        CREATE TABLE IF NOT EXISTS phoneNumbers(
           id INTEGER PRIMARY KEY NOT NULL,
           phoneNumber TEXT NOT NULL,
           names_id INTEGER NOT NULL,
           FOREIGN KEY(names_id) REFERENCES names(id) ON DELETE CASCADE ON UPDATE CASCADE
        );
        """
        try:
            cur.executescript(sql)
        except sqlite3.DatabaseError:
            raise sqlite3.DatabaseError  # ("Не удалось создать DB.")
        else:  # transform data to dict.
            sql = """\
            SELECT names.name, phoneNumbers.phoneNumber FROM names, phoneNumbers
            WHERE phoneNumbers.names_id=names.id;
            """
            try:
                cur.execute(sql)
            except sqlite3.DatabaseError:
                raise sqlite3.DatabaseError  # ("Не удалось выполнить запрос.")
            else:
                for name, phoneNumber in cur:
                    if name not in self.phoneBook:
                        self.phoneBook[name] = [phoneNumber]
                    else:
                        self.phoneBook[name].append(phoneNumber)
                # self.isDictLoaded = True
        finally:
            cur.close()
            conn.close()
            # return self.isDictLoaded

    def funInsertIntoDb(self, name, phonesList):
        """ Insert data to the database. """
        conn = sqlite3.connect(self.__pathToDB + "PhoneBook.sqlite3")
        conn.execute("PRAGMA foreign_keys=1")  # enable cascade deleting and updating.
        cur = conn.cursor()
        try:  # insert a new name into names.
            cur.execute("INSERT INTO names(name) VALUES(:name)", {"name": name})
        except sqlite3.DatabaseError as err:
            raise sqlite3.DatabaseError("funInsertIntoDb: INSERT INTO names(name) VALUES(:name)", err)
        else:
            # don't do conn.commit() because
            # if error will occur in the next inserting (for phoneNumbers)
            # name will be without any phoneNumber!!!
            try:  # get names_id by the name.
                cur.execute("SELECT id FROM names WHERE name=:name", {"name": name})
            except sqlite3.DatabaseError as err:
                raise sqlite3.DatabaseError("funInsertIntoDb: SELECT id FROM names WHERE name=:name", err)
            else:  # insert phoneNumbers into the PhoneBook's database.
                # get names_id from the list[0]
                names_id = cur.fetchone()[0]
                for phoneNumber in phonesList:
                    try:
                        cur.execute("INSERT INTO phoneNumbers(phoneNumber, names_id) VALUES(:phoneNumber, :names_id)",
                                    {"phoneNumber": phoneNumber, "names_id": names_id})
                    except sqlite3.DatabaseError as err:
                        raise sqlite3.DatabaseError("funInsertIntoDb: INSERT INTO phoneNumbers(phoneNumber, names_id)", err)
                    else:
                        conn.commit()  # complete transactions for BOTH inserting: names and phoneNumbers.
        finally:
            cur.close()
            conn.close()

    def funMultiRecordDeleting(self, namesList):
        """
        Delete records with all phone numbers from the database.
        :param namesList:
        """
        conn = sqlite3.connect(self.__pathToDB + "PhoneBook.sqlite3")
        conn.execute("PRAGMA foreign_keys=1")  # enable cascade deleting and updating.
        cur = conn.cursor()
        try:
            for name in namesList:
                try:  # cascade deleting all records from names and phoneNumbers for THIS name.
                    cur.execute("DELETE FROM names WHERE name=:name", {"name": name})
                except sqlite3.DatabaseError as err:
                    raise sqlite3.DatabaseError("funDeleteOneRecord: DELETE FROM names WHERE name=:name", err)
            conn.commit()  # commit transactions after completion all deleting.
        finally:
            cur.close()
            conn.close()

    def funDeleteOldThenInsertNewRecord(self, oldName, newName, phonesList):
        """
        Delete and then insert data.
        Using ONE TRANSACTION for both: deleting and inserting.
        :param oldName:
        :param newName:
        :param phonesList:
        """
        conn = sqlite3.connect(self.__pathToDB + "PhoneBook.sqlite3")
        conn.execute("PRAGMA foreign_keys=1")  # enable cascade deleting and updating.
        cur = conn.cursor()
        try:
            # cascade deleting all records from names and phoneNumbers for the oldName
            cur.execute("DELETE FROM names WHERE name=:oldName", {"oldName": oldName})
            # inserting newName into the names
            cur.execute("INSERT INTO names(name) VALUES(:newName)", {"newName": newName})
            # get id by the newName.
            cur.execute("SELECT id FROM names WHERE name=:newName", {"newName": newName})
        except sqlite3.DatabaseError as err:
            raise sqlite3.DatabaseError("funDeleteOldThenInsertNewRecord: DELETE FROM names WHERE name=:name", err)
        else:
            # get id from the list[0]
            id = cur.fetchone()[0]
            # and then cascade inserting new phones for the newName.
            for phoneNumber in phonesList:
                try:
                    cur.execute("INSERT INTO phoneNumbers(phoneNumber, names_id) VALUES(:phoneNumber, :names_id)",
                                {"phoneNumber": phoneNumber, "names_id": id})
                except sqlite3.DatabaseError as err:
                    raise sqlite3.DatabaseError("funInsertIntoDb: INSERT INTO phoneNumbers(phoneNumber, names_id)", err)
            # only if all inserting completed successfully, commit!!!
            conn.commit()  # complete transactions for BOTH inserting: names and phoneNumbers.
        finally:
            cur.close()
            conn.close()

    def funClearDb(self):
        """ Delete all data from the database. """
        conn = sqlite3.connect(self.__pathToDB + "PhoneBook.sqlite3")
        conn.execute("PRAGMA foreign_keys=1")  # enable cascade deleting and updating.
        cur = conn.cursor()
        sql = """\
        DELETE FROM names;
        """
        try:
            cur.executescript(sql)
        except sqlite3.DatabaseError:
            raise sqlite3.DatabaseError  # ("Не удалось выполнить запрос.")
        else:
            conn.commit()  # complete transaction.
        finally:
            cur.close()
            conn.close()

    # def funDeleteSeveralPhonesFromRecord(self, name, phonesList):
    #     """ Delete several phones from the record. """
    #     conn = sqlite3.connect(self.__pathToDB + "PhoneBook.sqlite3")
    #     conn.execute("PRAGMA foreign_keys=1")  # enable cascade deleting and updating.
    #     cur = conn.cursor()
    #     try:  # get names_id by the name.
    #         cur.execute("SELECT id FROM names WHERE name=:name", {"name": name})
    #     except sqlite3.DatabaseError as err:
    #         raise sqlite3.DatabaseError("funDeleteSeveralPhonesFromRecord: SELECT id FROM names...", err)
    #     else:  # deleting phoneNumbers from the PhoneBook's database.
    #         # get id from the list[0]
    #         id = cur.fetchone()[0]
    #         for phoneNumber in phonesList:
    #             try:
    #                 cur.execute("DELETE FROM phoneNumbers WHERE names_id=:id AND phoneNumber=:phoneNumber",
    #                             {"id": id, "phoneNumber": phoneNumber})
    #             except sqlite3.DatabaseError as err:
    #                 raise sqlite3.DatabaseError("funDeleteSeveralPhonesFromRecord: DELETE FROM phoneNumbers...", err)
    #             else:
    #                 conn.commit()  # commit transactions.
    #     finally:
    #         cur.close()
    #         conn.close()
