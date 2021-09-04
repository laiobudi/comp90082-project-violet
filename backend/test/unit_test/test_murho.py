import sys
sys.path.append("../..")
from backend.utility.murho import cal_murho

"""
This variable is used for testing the logic of the function
@data type: list[dicts]
@variable name: beams_sample
"""
beams_sample = [
    {"beam_id": "Filter1", "kvp": 60, "hvl_measured_al": 1.268, "hvl_measured_cu": None},
    {"beam_id": "Filter2", "kvp": 80, "hvl_measured_al": 2.321, "hvl_measured_cu": None},
    {"beam_id": "Filter3", "kvp": 100, "hvl_measured_al": 2.881, "hvl_measured_cu": None},
    {"beam_id": "Filter4", "kvp": 120, "hvl_measured_al": 5.123, "hvl_measured_cu": 0.227},
    {"beam_id": "Filter5", "kvp": 150, "hvl_measured_al": None, "hvl_measured_cu": 0.339},
    {"beam_id": "Filter6", "kvp": 180, "hvl_measured_al": None, "hvl_measured_cu": 0.504},
    {"beam_id": "Filter7", "kvp": 200, "hvl_measured_al": None, "hvl_measured_cu": 1.042},
    {"beam_id": "Filter8", "kvp": 250, "hvl_measured_al": None, "hvl_measured_cu": 2.117}
]

"""
This variable is used for testing the logic of the function
since database does not have enough data, this look up table is taken from excel
@data type: dict
@variable name: murho_table
"""
al_table = [
    {"hvl_al": 0.03, "murho": 1.047},
    {"hvl_al": 0.04, "murho": 1.047},
    {"hvl_al": 0.05, "murho": 1.046},
    {"hvl_al": 0.06, "murho": 1.046},
    {"hvl_al": 0.08, "murho": 1.044},
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
    {"hvl_al": 6.0, "murho": 1.034},
    {"hvl_al": 8.0, "murho": 1.045}]
cu_table = [
    {"hvl_cu": 0.1, "murho": 1.020},
    {"hvl_cu": 0.2, "murho": 1.028},
    {"hvl_cu": 0.3, "murho": 1.035},
    {"hvl_cu": 0.4, "murho": 1.043},
    {"hvl_cu": 0.5, "murho": 1.050},
    {"hvl_cu": 0.6, "murho": 1.056},
    {"hvl_cu": 0.8, "murho": 1.068},
    {"hvl_cu": 1.0, "murho": 1.076},
    {"hvl_cu": 1.5, "murho": 1.085},
    {"hvl_cu": 2.0, "murho": 1.089},
    {"hvl_cu": 3.0, "murho": 1.100},
    {"hvl_cu": 4.0, "murho": 1.106},
    {"hvl_cu": 5.0, "murho": 1.109}
]


"""
EC1: 
"""
def test1():
    #...
    return