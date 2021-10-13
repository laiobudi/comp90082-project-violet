import datetime

import pyodbc

"""
This function is used to connect to the database, call it before you query
Output: cursor
"""


def DB_connect():
    connection = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=13.70.131.250,1433;"
        "Database=violet_main;"
        "Uid=SA;"
        "PWD=ProjViolet_1;"
        "Trusted_Connection=no;"
    )
    return connection.cursor()

