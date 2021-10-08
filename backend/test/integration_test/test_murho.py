import sys
import numpy

sys.path.append("../..")
import pytest
from backend.utility.murho import add_murho

"""
Since correct data from Client's excel files are less,
it is easy to test them all, just do it first.
Then boundary test will be applied.
"""


@pytest.mark.parametrize("beams_hogwarts, beams_hogwarts_excel", [
    ([
         {"beam_id": "Filter1", "kvp": 60, "hvl_measured_al": 1.268, "hvl_measured_cu": None},
         {"beam_id": "Filter2", "kvp": 80, "hvl_measured_al": 2.321, "hvl_measured_cu": None},
         {"beam_id": "Filter3", "kvp": 100, "hvl_measured_al": 2.881, "hvl_measured_cu": None},
         {"beam_id": "Filter4", "kvp": 120, "hvl_measured_al": 5.123, "hvl_measured_cu": 0.227},
         {"beam_id": "Filter5", "kvp": 150, "hvl_measured_al": None, "hvl_measured_cu": 0.339},
         {"beam_id": "Filter6", "kvp": 180, "hvl_measured_al": None, "hvl_measured_cu": 0.504},
         {"beam_id": "Filter7", "kvp": 200, "hvl_measured_al": None, "hvl_measured_cu": 1.042},
         {"beam_id": "Filter8", "kvp": 250, "hvl_measured_al": None, "hvl_measured_cu": 2.117}
     ],
     [
         {"al_murho": 1.018, "cu_murho": None, "murho": 1.018},
         {"al_murho": 1.019, "cu_murho": None, "murho": 1.019},
         {"al_murho": 1.021, "cu_murho": None, "murho": 1.021},
         {"al_murho": 1.030, "cu_murho": 1.030, "murho": 1.030},
         {"al_murho": None, "cu_murho": 1.038, "murho": 1.038},
         {"al_murho": None, "cu_murho": 1.050, "murho": 1.050},
         {"al_murho": None, "cu_murho": 1.077, "murho": 1.077},
         {"al_murho": None, "cu_murho": 1.090, "murho": 1.090}
     ])
])
def test_hogwarts(beams_hogwarts, beams_hogwarts_excel):
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


@pytest.mark.parametrize("beams_springfield, beams_springfield_excel", [
    ([
         {"beam_id": "F1", "kvp": 30, "hvl_measured_al": 0.190, "hvl_measured_cu": None},
         {"beam_id": "F2", "kvp": 50, "hvl_measured_al": 0.810, "hvl_measured_cu": None},
         {"beam_id": "F3", "kvp": 80, "hvl_measured_al": 2.010, "hvl_measured_cu": None},
         {"beam_id": "F4", "kvp": 95, "hvl_measured_al": 2.610, "hvl_measured_cu": None},
         {"beam_id": "F5", "kvp": 100, "hvl_measured_al": 4.020, "hvl_measured_cu": None}
     ],
     [
         {"al_murho": 1.039, "cu_murho": None, "murho": 1.039},
         {"al_murho": 1.022, "cu_murho": None, "murho": 1.022},
         {"al_murho": 1.018, "cu_murho": None, "murho": 1.018},
         {"al_murho": 1.020, "cu_murho": None, "murho": 1.020},
         {"al_murho": 1.025, "cu_murho": None, "murho": 1.025}
     ])
])
def test_springfield(beams_springfield, beams_springfield_excel):
    res_beams = add_murho(beams_springfield)
    for i in range(len(res_beams)):
        if res_beams[i]["al_murho"] is None:
            assert_al = (res_beams[i]["al_murho"] == beams_springfield_excel[i]["al_murho"])
        else:
            assert_al = (round(res_beams[i]["al_murho"], 3) == beams_springfield_excel[i]["al_murho"])
        if res_beams[i]["cu_murho"] is None:
            assert_cu = (res_beams[i]["cu_murho"] == beams_springfield_excel[i]["cu_murho"])
        else:
            assert_cu = (round(res_beams[i]["cu_murho"], 3) == beams_springfield_excel[i]["cu_murho"])
        assert assert_al
        assert assert_cu
        assert round(res_beams[i]["murho"], 3) == beams_springfield_excel[i]["murho"]


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Boundary Tests:
boundaries:
0.03 <= First HVL(mm Al) <= 8.0
0.1 <= First HVL(mm Cu) <= 5.0
#IMPORTANT#: The expected results of boundary tests are calculated by
Client's algorithm from excel files.
According to Client Fayz, murho and bw have no situation that hvls are out of the boundary.
#IMPORTANT#: 
If hvl is out of boundary, cu_murho(or al_murho), murho will be None
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# First HVL(mm Al) == 0.030
# First HVL(mm Al) = 0.029 < 0.030
# First HVL(mm Al) = 8.000
# First HVL(mm Al) = 8.001 > 8.000
@pytest.mark.parametrize("beam_al_boundary, beam_al_boundary_result", [
    ([
         {"hvl_measured_al": 0.030, "hvl_measured_cu": None},
         {"hvl_measured_al": 0.029, "hvl_measured_cu": None},
         {"hvl_measured_al": 8.000, "hvl_measured_cu": None},
         {"hvl_measured_al": 8.001, "hvl_measured_cu": None}
     ],
     [
         {"al_murho": 1.047, "cu_murho": None, "murho": 1.047},
         {"al_murho": None, "cu_murho": None, "murho": None},
         {"al_murho": 1.045, "cu_murho": None, "murho": 1.045},
         {"al_murho": None, "cu_murho": None, "murho": None},
     ])
])
def test_al_boundary(beam_al_boundary, beam_al_boundary_result):
    res_beams = add_murho(beam_al_boundary)
    for i in range(len(res_beams)):
        if res_beams[i]["al_murho"] is None:
            assert_al = (res_beams[i]["al_murho"] == beam_al_boundary_result[i]["al_murho"])
        else:
            assert_al = (round(res_beams[i]["al_murho"], 3) == beam_al_boundary_result[i]["al_murho"])
        if res_beams[i]["cu_murho"] is None:
            assert_cu = (res_beams[i]["cu_murho"] == beam_al_boundary_result[i]["cu_murho"])
        else:
            assert_cu = (round(res_beams[i]["cu_murho"], 3) == beam_al_boundary_result[i]["cu_murho"])
        if res_beams[i]["murho"] is None:
            asser_murho = res_beams[i]["murho"] == beam_al_boundary_result[i]["murho"]
        else:
            asser_murho = round(res_beams[i]["murho"], 3) == beam_al_boundary_result[i]["murho"]
        assert assert_al
        assert assert_cu
        assert asser_murho


# First HVL(mm Cu) == 0.100
# First HVL(mm Cu) = 0.099 < 0.100
# First HVL(mm Cu) == 5.000
# First HVL(mm Cu) = 5.001 > 5.000
@pytest.mark.parametrize("beam_cu_boundary, beam_cu_boundary_result", [
    ([
         {"hvl_measured_al": None, "hvl_measured_cu": 0.100},
         {"hvl_measured_al": None, "hvl_measured_cu": 0.099},
         {"hvl_measured_al": None, "hvl_measured_cu": 5.000},
         {"hvl_measured_al": None, "hvl_measured_cu": 5.001}
     ],
     [
         {"al_murho": None, "cu_murho": 1.020, "murho": 1.020},
         {"al_murho": None, "cu_murho": None, "murho": None},
         {"al_murho": None, "cu_murho": 1.109, "murho": 1.109},
         {"al_murho": None, "cu_murho": None, "murho": None}
     ])
])
def test_cu_boundary(beam_cu_boundary, beam_cu_boundary_result):
    res_beams = add_murho(beam_cu_boundary)
    for i in range(len(res_beams)):
        if res_beams[i]["al_murho"] is None:
            assert_al = (res_beams[i]["al_murho"] == beam_cu_boundary_result[i]["al_murho"])
        else:
            assert_al = (round(res_beams[i]["al_murho"], 3) == beam_cu_boundary_result[i]["al_murho"])
        if res_beams[i]["cu_murho"] is None:
            assert_cu = (res_beams[i]["cu_murho"] == beam_cu_boundary_result[i]["cu_murho"])
        else:
            assert_cu = (round(res_beams[i]["cu_murho"], 3) == beam_cu_boundary_result[i]["cu_murho"])
        if res_beams[i]["murho"] is None:
            asser_murho = res_beams[i]["murho"] == beam_cu_boundary_result[i]["murho"]
        else:
            asser_murho = round(res_beams[i]["murho"], 3) == beam_cu_boundary_result[i]["murho"]
        assert assert_al
        assert assert_cu
        assert asser_murho
