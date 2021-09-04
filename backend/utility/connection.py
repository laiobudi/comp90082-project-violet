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

# def getMurhoTable(connection, type):
#     try:
#         query = "SELECT * FROM murho_{} ".format(type)
#         cursor = connection.execute(query)
#
#         columns = [column[0] for column in connection.description]
#         rows = cursor.fetchall()
#         murho_table = []
#         for row in rows:
#             murho_table.append(dict(zip(columns, row)))
#         return murho_table
#
#     except Exception as err:
#         print(err)
#         return err
#
# connection = DB_connect()
# currentLength = len(getMurhoTable(DB_connect(), "cu"))
# print(currentLength)
# # connection.execute("truncate table murho_cu")
# connection.commit()

# This part is for inserting data to murho_al/murho_cu only
# try:
#     connection = DB_connect()
#     for arow in cu_table:
#         print(arow)
#         currentLength = len(getMurhoTable(DB_connect(), "cu"))
#         connection.execute("INSERT INTO murho_cu(murho_cu_id, hvl_cu, murho, date_updated) values (?, ?, ?, ?)",
#                            (currentLength + 1, arow["hvl_cu"], arow["murho"], datetime.datetime.now()))
#         connection.commit()
# except Exception as e:
#     print(e)
