# -*- coding:UTF-8 -*-

from flask import Flask, jsonify, request
import pyodbc

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["SECRET_KEY"] = "123456"

# read me
"""
你们负责完成formula function的构建

你们需要自定义一个function，要写清楚，需要的参数从哪个框框里读哪个字段，算出来的结果存哪个字段
我来负责在这些function外面查询数据库并传入调用，一些简单的逻辑最好自己写
但如果需要特殊的功能，也写清楚就可以了，比如获取某框框中的某个字段中，距离10.7最近的两个值
你就直接定义：
def xxx_function(arg1, arg2):
    return XXX
我去找这两个值传进去

这里是一个例子，比如说我们要根据field_test001 和 field_test002去计算并且填入 field_test003
计算公式为：field_test003 = (field_test001 + field_test002) * 2
我在下面的下面写了一个 cal_Nk_test(arg1, arg2)，可供参考
table name: dbo.test001_by_redback

field_test001   field_test002   field_test003
1.0             2.0             Null
11.0            22.0            Null
111.0           222.0           Null

运行结果
before table
[(1.0, 2.0, None), (11.0, 22.0, None), (111.0, 222.0, None)]
after table
[(1.0, 2.0, 6.0), (11.0, 22.0, 66.0), (111.0, 222.0, 666.0)]

"""


# START finish the formula ############################################################

# all the calculation functions
def cal_Nk_test(arg1, arg2):
    # 下面这个打三个"，敲回车，可以自动出来
    """
    :param arg1: arg1 is the Beam ID from No.X table // No.X refers to the excel file (send you later),
                                                        which has tag number for each green block

    :param arg2: arg2 is the nk_value from No.X table
    :return: the value to be stored to database
    """
    result = (arg1 + arg2) * 2
    return result
# END finish the formula ##############################################################

# START Grizz Huang part, you may ignore ##############################################

# test
conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=34.126.203.116,1433;"
    "Database=violet_main;"
    "Uid=SA;"
    "PWD=ProjViolet!1;"
    "Trusted_Connection=no;"
)

cursor = conn.cursor()
current_table = cursor.execute("SELECT * FROM" + " dbo.test001_by_redback").fetchall()

print("before table")
print(current_table)

for rowNum, content in enumerate(current_table):
    cursor.execute(
        "UPDATE dbo.test001_by_redback SET "
        + "field_test003 = "
        + str(cal_Nk_test(current_table[rowNum][0], current_table[rowNum][1]))
        + " WHERE field_test001  = "
        + str(current_table[rowNum][0])
    )

# 存档
# cursor.commit()

current_table = cursor.execute("SELECT * FROM" + " dbo.test001_by_redback").fetchall()

print("after table")
print(current_table)

# END test


# front end interfaces
@app.route("/")
def index():
    cursor.execute("SELECT * FROM" + " dbo.test001_by_redback")
    print("hahaha")
    for i in cursor:
        print(i)

    return jsonify(status=1)

# END Grizz Huang part, you may ignore ##############################################


if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=5001, host="127.0.0.1")
