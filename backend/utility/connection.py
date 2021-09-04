import datetime

import pyodbc

"""
This function is used to connect to the database, call it before you query
Output: cursor
"""


def DB_connect():
    connection = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=34.126.203.116,1433;"
        "Database=violet_main;"
        "Uid=SA;"
        "PWD=ProjViolet!1;"
        "Trusted_Connection=no;"
    )
    return connection.cursor()


al_table = [
    {"hvl_al": 0.10, "murho": 1.044},
    {"hvl_al": 0.12, "murho": 1.043},
    {"hvl_al": 0.15, "murho": 1.041},
    {"hvl_al": 0.2, "murho": 1.039},
    {"hvl_al": 0.3, "murho": 1.035},
    {"hvl_al": 0.4, "murho": 1.031},
    {"hvl_al": 0.5, "murho": 1.028},
    {"hvl_al": 0.6, "murho": 1.026},
    {"hvl_al": 0.8, "murho": 1.022},
    {"hvl_al": 1.0, "murho": 1.020},
    {"hvl_al": 1.2, "murho": 1.018},
    {"hvl_al": 1.5, "murho": 1.017},
    {"hvl_al": 2.0, "murho": 1.018},
    {"hvl_al": 3.0, "murho": 1.021},
    {"hvl_al": 4.0, "murho": 1.025},
    {"hvl_al": 5.0, "murho": 1.029},
    {"hvl_al": 6.0, "murho": 1.034}]


def getMurhoTable(connection, type):
    try:
        query = "SELECT * FROM murho_{} ".format(type)
        cursor = connection.execute(query)

        columns = [column[0] for column in connection.description]
        rows = cursor.fetchall()
        murho_table = []
        for row in rows:
            murho_table.append(dict(zip(columns, row)))
        return murho_table

    except Exception as err:
        print(err)
        return err

currentLength = len(getMurhoTable(DB_connect(), "al"))
print(currentLength)

#This part is for inserting data to murho_al/murho_cu only
# try:
#     connection = DB_connect()
#     for arow in al_table:
#         print(arow)
#         currentLength = len(getMurhoTable(DB_connect(), "al"))
#         connection.execute("INSERT INTO murho_al(murho_al_id, hvl_al, murho, date_updated) values (?, ?, ?, ?)",
#                            (currentLength + 1, arow["hvl_al"], arow["murho"], datetime.datetime.now()))
#         connection.commit()
# except Exception as e:
#     print(e)
