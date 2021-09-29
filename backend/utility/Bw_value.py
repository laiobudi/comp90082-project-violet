from backend.utility.interpolation import interpolation
import numpy as np
import pyodbc

# input data from the `identification` sheet
beams = [
    {"beam_id": "Filter1", "kvp": 60, "hvl_measured_al": 1.268, "hvl_measured_cu": None},
    {"beam_id": "Filter2", "kvp": 80, "hvl_measured_al": 2.321, "hvl_measured_cu": None},
    {"beam_id": "Filter3", "kvp": 100, "hvl_measured_al": 2.881, "hvl_measured_cu": None},
    {"beam_id": "Filter4", "kvp": 120, "hvl_measured_al": 5.123, "hvl_measured_cu": 0.227},
    {"beam_id": "Filter5", "kvp": 150, "hvl_measured_al": None, "hvl_measured_cu": 0.339},
    {"beam_id": "Filter6", "kvp": 180, "hvl_measured_al": None, "hvl_measured_cu": 0.504},
    {"beam_id": "Filter7", "kvp": 200, "hvl_measured_al": None, "hvl_measured_cu": 1.042},
    {"beam_id": "Filter8", "kvp": 250, "hvl_measured_al": None, "hvl_measured_cu": 2.117}
]

cones = [
    {"cone_id": "F", "SSD": 30, "diameter": 10},
    {"cone_id": "K", "SSD": 50, "diameter": 11.2837916709551},
    {"cone_id": "E", "SSD": 30, "diameter": 5}
]

diameter_axis = [1, 2, 3, 5, 10, 15, 20]
ssd_al_axis = [1.5, 3, 5, 7, 10, 20, 30, 50, 100]
ssd_cu_axis = [10, 20, 30, 50, 100]
hvl_al_axis = [0.04, 0.05, 0.06, 0.08, 0.1, 0.12, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1, 1.2, 1.5, 2, 3, 4, 5, 6, 8]
hvl_cu_axis = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1, 1.5, 2, 3, 4, 5]




###########################
#### Main Calculation #####
###########################
def cal_Bw_value(cursor, beams, cones):
    # get beams and cones input values from database.
    # beams, cones = get_input_value()

    # Start calculation.
    for cone in cones:
        for beam in beams:
            # step 0.5
            # CHECK if it's Al or Cu or Both
            hvl_type = checkType(beam)

            # step 1
            # SELECT search info from DB (including their data e.g. measured HVL, Nk...)
            # step 2
            # given previous 2 points' nk values (a, b), and hvl values (c, e), and beam["hvl_measured_al(cu)"] (d) -> do interpolation

            # both Al and Cu exist, need to calculate average value
            bw_res = []

            if hvl_type["Al"]:
                al_res = calculation(cursor, cone["SSD"], cone["diameter"], beam["hvl_measured_al"], "Al")
                bw_res.append(al_res)
                print('beam: ' + str(beam) + ', cone: ' + str(cone) + 'Al: ', str(al_res))
                # storeIntoDb(table_name, Al_column_name, al_res)
            if hvl_type["Cu"]:
                cu_res = calculation(cursor, cone["SSD"], cone["diameter"], beam["hvl_measured_cu"], "Cu")
                bw_res.append(cu_res)
                print("beam: " + str(beam) + ", cone: " + str(cone) + 'Cu: ', str(cu_res))
                # storeIntoDb(table_name, Cu_column_name, cu_res)

            # storeIntoDb(table_name, Combined_column_name, sum(bw_res) / len(bw_res))
            print("beam: " + str(beam) + ", cone: " + str(cone) + 'Combined: ', str(sum(bw_res) / len(bw_res)))

def calculation(cursor, ssd: float, diameter: float, hvl: float, type: str):
    if type == "Al":
        ssd_axis = ssd_al_axis
        hvl_axis = hvl_al_axis
    elif type == "Cu":
        ssd_axis = ssd_cu_axis
        hvl_axis = hvl_cu_axis
    else:
        raise Exception('The type should be Al or Cu.')

    if (ssd < ssd_axis[0] or ssd > ssd_axis[-1] or diameter < diameter_axis[0] or diameter > diameter_axis[-1] or
    hvl < hvl_axis[0] or hvl > hvl_axis[-1]):
        raise Exception('Illegal inputs.')

    ssd_list = check_exist(ssd, ssd_axis)
    hvl_list = check_exist(hvl, hvl_axis)
    diameter_list = check_exist(diameter, diameter_axis)

    # ssd_len = len(ssd_list)
    # hvl_len = len(hvl_list)
    # diameter_len = len(diameter_list)

    # 如果全部能匹配上，直接查询返回。
    # if (len(ssd_list) == 1 and len(diameter_list) == 1 and len(hvl_list) == 1):
    #     return select_from_DB(ssd_list[0], diameter_list[0], hvl_list[0], type)

    if (ssd_list[0] == ssd_list[1] and diameter_list[0] == diameter_list[1] and hvl_list[0] == hvl_list[1]):
        return select_from_DB(cursor, ssd_list[0], hvl_list[0], diameter_list[0], type)

    # 至少一个匹配不上，建立3D数组存值。
    required_values = np.zeros((len(ssd_list), len(hvl_list), len(diameter_list)))

    # 可能有重复查询，最多四次。
    for i in range(len(ssd_list)):
        for j in range(len(hvl_list)):
            for k in range(len(diameter_list)):
                # print((i,j,k))
                required_values[i, j, k] = select_from_DB(cursor, ssd_list[i], hvl_list[j], diameter_list[k], type)

    hvl1 = interpolation(required_values[0,0,0], required_values[0,1,0], hvl_list[0], hvl_list[1], hvl)
    hvl2 = interpolation(required_values[0,0,1], required_values[0,1,1], hvl_list[0], hvl_list[1], hvl)

    hvl3 = interpolation(required_values[1,0,0], required_values[1,1,0], hvl_list[0], hvl_list[1], hvl)
    hvl4 = interpolation(required_values[1,0,1], required_values[1,1,1], hvl_list[0], hvl_list[1], hvl)

    d1 = interpolation(hvl1, hvl2, diameter_list[0], diameter_list[1], diameter)
    d2 = interpolation(hvl3, hvl4, diameter_list[0], diameter_list[1], diameter)

    ssd1 = interpolation(d1, d2, ssd_list[0], ssd_list[1], ssd)

    return ssd1

###########################
#### Helper functions #####
###########################

def connect_to_db():
    try:
        # connect to database
        connection = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=34.126.203.116,1433;"
            "Database=violet_main;"
            "Uid=SA;"
            "PWD=ProjViolet!1;"
            "Trusted_Connection=no;"
        )
        # Create cursor object
        return connection.cursor()

    except pyodbc.Error as ex:
        raise Exception(ex.args[1])


def select_input_from_db(cursor, audit_id):
    # 加了cones。

    cones = []
    beams = []
    input_beams_table = cursor.execute('SELECT beam_id, '
                                + 'nom_energy, '
                                + 'hvl_measured_mm_al, '
                                + 'hvl_measured_mm_cu '
                                + "FROM beam_data "
                                + "WHERE beam_id "
                                + "LIKE '{}%'".format(audit_id)
                                       ).fetchall()
    for key, value in enumerate(input_beams_table):
        beam = {"beam_id": (value)[0],
                "kvp": (value)[1],
                "hvl_measured_al": (value)[2],
                "hvl_measured_cu": (value)[3]}
        beams.append(beam)
    # DEBUG
    # print(beams)

    #不考虑必要值为空的情况。
    input_cones_table = cursor.execute('SELECT cone_id, ssd, '
                                + "CASE WHEN shape = 'circular' THEN field_diameter "
                                + "	WHEN shape = 'square' THEN 2*SQRT(field_area/PI()) "
                                + "	WHEN shape = 'rectangular' THEN 2*SQRT(field_dimension_1*field_dimension_2/PI()) "
                                # + "ELSE要加吗？"
                                + "END AS diameter "
                                + "FROM cone "
                                + "WHERE cone_id "
                                + "LIKE '{}%'".format(audit_id)
                                       ).fetchall()
    for key, value in enumerate(input_cones_table):
        cone = {"cone_id": (value)[0],
                "SSD": (value)[1],
                "diameter": (value)[2]}
        cones.append(cone)
    # Check for null value!!!


    return beams, cones


def check_exist(target, axis):
    for i in range(len(axis)):
        if axis[i] == target:
            return [target, target]
        elif axis[i] > target:
            return [axis[i-1], axis[i]]



def select_from_DB(cursor, ssd, hvl, diameter, type):
    #SQL query.

    bw_lookup_value = cursor.execute("SELECT bw "
                                + "FROM bw_al_cu "
                                + "WHERE type = '{}' ".format(type)
                                + "AND ssd = {} ".format(ssd)
                                + "AND diameter = {} ".format(diameter)
                                + "AND hvl_{} = {}".format(type.lower(), hvl)).fetchall() #未完成。

    # Check return 数量？
    # rowcount.

    for row in bw_lookup_value:
        return row.bw

# check type of measured_hvl
def checkType(info: dict):
    hvl_type = {"Al": False, "Cu": False}
    if info["hvl_measured_al"]: hvl_type["Al"]=True
    if info["hvl_measured_cu"]: hvl_type["Cu"]=True

    return hvl_type


# DB query: Store data into Db
def storeIntoDb():
    # TODO: INSERT ...
    return 0


if __name__ == "__main__":
    cursor = connect_to_db()

    audit_id = 'ACDS-kV-5014'
    beams, cones = select_input_from_db(cursor, audit_id)
    print(beams, cones)

    beams = [
    {"beam_id": "Filter1", "kvp": 60, "hvl_measured_al": 1.268, "hvl_measured_cu": None},
    {"beam_id": "Filter2", "kvp": 80, "hvl_measured_al": 2.321, "hvl_measured_cu": None},
    {"beam_id": "Filter3", "kvp": 100, "hvl_measured_al": 2.881, "hvl_measured_cu": None},
    {"beam_id": "Filter4", "kvp": 120, "hvl_measured_al": 5.123, "hvl_measured_cu": 0.227},
    {"beam_id": "Filter5", "kvp": 150, "hvl_measured_al": None, "hvl_measured_cu": 0.339},
    {"beam_id": "Filter6", "kvp": 180, "hvl_measured_al": None, "hvl_measured_cu": 0.504},
    {"beam_id": "Filter7", "kvp": 200, "hvl_measured_al": None, "hvl_measured_cu": 1.042},
    {"beam_id": "Filter8", "kvp": 250, "hvl_measured_al": None, "hvl_measured_cu": 2.117}
]
    cal_Bw_value(beams, cones)