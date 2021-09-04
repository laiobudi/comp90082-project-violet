"""
This file is for calculating murho
@Author: Hongyang Lyu
"""
import operator
from itertools import islice
from interpolation import interpolation
from connection import DB_connect
connection = DB_connect()

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



print(getMurhoTable(connection, "al"))


"""
This function is to convert dict to list and get first N elements
@Parameter Type: int, dictItem
@Output Type: List[tuple]
@Output Example: [(hvl1,murho), (hvl2,murho)...] e.g.[(0.1,1.020), (0.2,1.028)...]
"""
def first_N_dictitems(n, dictItem):
    return list(islice(dictItem, n))

"""
Noting special, just used to sort the dict by Key and return a dict
"""
def sort_dict_by_key_ascending(sorting_dict):
    return dict(sorted(sorting_dict.items(), key=operator.itemgetter(0)))


"""
This function is to get the hvl list for Cu/Al from look up table, it return a sorted dict by key(i.e. hvl)
@Parameter Type: String
@Parameter Example: ["first_hvl_al", "first_hvl_cu"]
@Output Type: Dict
@Output Example: {hvl1:murho, hvl2:murho...} e.g {0.1:1.020, 0.2:1.028, 0.3:1.035...} for first_hvl_cu
"""

# def get_first_hvl(hvl_type):
#     result = {}
#     for row in murho_table:
#         if row[hvl_type] is not None:
#             result[row[hvl_type]] = row["murho"]
#     return sort_dict_by_key_ascending(result)

"""
This function is to get the murho result for Cu/Al from look up table, it return a Float number
@Parameter Type: Dict, String
@Parameter Example: {"beam_id": "Filter1", "kvp": 60, "hvl_measured_al": None, "hvl_measured_cu": 1.268}, "first_hvl_cu"
@Output Type: Float
@Output Example: 1.090287
"""
def cal_murho(beam_measured, hvl_type):
    hvls = getMurhoTable(hvl_type)
    hvls_list = first_N_dictitems(len(hvls), hvls.items())

    # if hvl matched look up table, just return the murho
    for row in hvls_list:
        if beam_measured == row[0]:
            return row[1]

    min_hvl = hvls_list[0][0]
    max_hvl = hvls_list[-1][0]
    if beam_measured < min_hvl:
        a = hvls_list[0][1]
        b = hvls_list[1][1]
        c = hvls_list[0][0]
        target_known_val = beam_measured
        e = hvls_list[1][0]
        return interpolation(a, b, c, e, target_known_val)
    elif beam_measured > min_hvl and beam_measured < max_hvl:
        for index in range(len(hvls_list)):
            if (beam_measured - hvls_list[index][0]) < 0:
                e = hvls_list[index][0]
                b = hvls_list[index][1]
                c = hvls_list[index - 1][0]
                a = hvls_list[index - 1][1]
                target_known_val = beam_measured
                return interpolation(a, b, c, e, target_known_val)
    elif beam_measured > max_hvl:
        e = hvls_list[-1][0]
        b = hvls_list[-1][1]
        c = hvls_list[-2][0]
        a = hvls_list[-2][1]
        target_known_val = beam_measured
        return interpolation(a, b, c, e, target_known_val)
    else:
        return "Error!"

"""
This function is to add the murho to the dict and return the updated dict
@Parameter Type: Dict
@Parameter Example: [{"beam_id": "Filter1", "kvp": 60, "hvl_measured_al": None, "hvl_measured_cu": 1.268},{...},...]
@Output Type: Dict
@Output Example: 
{'beam_id': 'Filter7', 
    'kvp': 200, 
    'hvl_measured_al': None, 
    'hvl_measured_cu': 1.042, 
    'al_murho': None, 
    'cu_murho': 1.076756, 
    'murho': 1.076756} 
,{...},...]
"""
def add_murho(beams_sample):
    temp = beams_sample
    for beam in temp:
        al_murho, cu_murho = None, None
        if beam["hvl_measured_al"] is not None:
            al_murho = cal_murho(beam["hvl_measured_al"], "hvl_al")

        if beam["hvl_measured_cu"] is not None:
            cu_murho = cal_murho(beam["hvl_measured_cu"], "hvl_cu")

        beam["al_murho"], beam["cu_murho"] = al_murho, cu_murho
        if isinstance(al_murho, str) or isinstance(cu_murho, str):
            return "Error!"
        elif al_murho is None and cu_murho is not None:
            beam["murho"] = cu_murho
        elif cu_murho is None and al_murho is not None:
            beam["murho"] = al_murho
        elif cu_murho is not None and al_murho is not None:
            beam["murho"] = (cu_murho + al_murho) / 2
        else:
            beam["murho"] = None
    return temp

