import json
import uuid, ast
from datetime import datetime
import sqlite3 as db


class Generator:

    def __init__(self):

        self.db = db.connect("database", check_same_thread=False)  # connecting to database
        self.cursor = self.db.cursor()  # instantiating the database cursor

    def insertData(self, values):
        """


        :param values: The values to execute inside the sql statement
        :return: boolean (True or False)
        """

        sql = "insert into table_name(datas) values (?)"
        val = (values,)
        self.cursor.execute(sql, val)
        self.db.commit()
        if self.cursor.rowcount == 1:
            return True
        else:
            return False

    def selectMultipleData(self):

        """
            This method gets multiple datas from the designated row of the table

        :param sql: The sql statement to execute
        :param value: The values to execute inside the sql statement
        :return: if the data is found it returns a List containing the data  else it returns a False

        """

        sql = "select datas from table_name order by id desc "
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if result is not None:
            return result
        else:
            return False

    def cleanup(self):
        """
        This block of code actually clean up the table and then resets it ID
        RUN THIS CODE IF YOU WANT TO CLEAN UP THE TABLE

        :return: True if the cleanup was successfully
        """
        self.cursor.execute(f'delete from table_name')
        self.cursor.execute(f'UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME="table_name"')
        self.db.commit()
        return True

    def callback(self):
        """

        :return: a dictionary data
        """
        key = str(uuid.uuid4()).replace("-", "")  # generating the uuid code
        timestamp = str(datetime.today())  # generating the key using a timestamp of today's date
        data = json.dumps({timestamp: key})  # dumping the generated timestamp and uuid as key : value respectively
        self.insertData(data)  # inserting the generated json into the sqlite database
        res = self.selectMultipleData()  # selecting all generated data from the database
        dd = {}  # An empty dummy dict to hold all the returned data from the database
        for x in res:  # looping through the returned data from the database
            reform = json.loads(x[0])  # converting each and every data back to json format
            dd.update(reform)  # updating the dummy dict with all converted json
        return dd  # return the data
