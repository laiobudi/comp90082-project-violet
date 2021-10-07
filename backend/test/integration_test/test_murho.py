import sys
import numpy
sys.path.append("../..")
import pytest
from backend.utility.murho import add_murho

beams_hogwarts=[
    {"beam_id": "Filter1", "kvp": 60, "hvl_measured_al": 1.268, "hvl_measured_cu": None},
    {"beam_id": "Filter2", "kvp": 80, "hvl_measured_al": 2.321, "hvl_measured_cu": None},
    {"beam_id": "Filter3", "kvp": 100, "hvl_measured_al": 2.881, "hvl_measured_cu": None},
    {"beam_id": "Filter4", "kvp": 120, "hvl_measured_al": 5.123, "hvl_measured_cu": 0.227},
    {"beam_id": "Filter5", "kvp": 150, "hvl_measured_al": None, "hvl_measured_cu": 0.339},
    {"beam_id": "Filter6", "kvp": 180, "hvl_measured_al": None, "hvl_measured_cu": 0.504},
    {"beam_id": "Filter7", "kvp": 200, "hvl_measured_al": None, "hvl_measured_cu": 1.042},
    {"beam_id": "Filter8", "kvp": 250, "hvl_measured_al": None, "hvl_measured_cu": 2.117}
]
beams_hogwarts_excel=[
     {"al_murho": 1.018, "cu_murho": None, "murho": 1.018},
     {"al_murho": 1.019, "cu_murho": None, "murho": 1.019},
     {"al_murho": 1.021, "cu_murho": None, "murho": 1.021},
     {"al_murho": 1.030, "cu_murho":1.030, "murho": 1.030},
     {"al_murho": None, "cu_murho": 1.038, "murho": 1.038},
     {"al_murho": None, "cu_murho": 1.050, "murho": 1.050},
     {"al_murho": None, "cu_murho": 1.077, "murho": 1.077},
     {"al_murho": None, "cu_murho": 1.090, "murho": 1.090}
]
@pytest.mark.parametrize("beams_hogwarts, beams_hogwarts_excel", [
	(beams_hogwarts, beams_hogwarts_excel)
])
def test_murho1(beams_hogwarts, beams_hogwarts_excel):
    res_beams = add_murho(beams_hogwarts)
    for i in range(len(res_beams)):
        if res_beams[i]["al_murho"] is None:
            assert_al = (res_beams[i]["al_murho"] == beams_hogwarts_excel[i]["al_murho"])
        else:
            assert_al = (round(res_beams[i]["al_murho"], 3) == beams_hogwarts_excel[i]["al_murho"])
        if res_beams[i]["cu_murho"] is None:
            assert_cu = (res_beams[i]["cu_murho"] == beams_hogwarts_excel[i]["cu_murho"])
        else:
            assert_cu = (round(res_beams[i]["cu_murho"], 3) == beams_hogwarts_excel[i]["cu_murho"])
        assert assert_al
        assert assert_cu
        assert round(res_beams[i]["murho"], 3) == beams_hogwarts_excel[i]["murho"]

test_murho1(beams_hogwarts, beams_hogwarts_excel)