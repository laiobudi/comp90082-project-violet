# unit tests for interpolation

import math

# TODO: improve the issue of import module

from backend.utility.interpolation import interpolation


BEAMS = [
    {"beam_id": "Filter1", "kvp": 60, "hvl_measured_al": 1.268},
    {"beam_id": "Filter2", "kvp": 80, "hvl_measured_al": 2.321},
    {"beam_id": "Filter3", "kvp": 100, "hvl_measured_al": 2.881},
    {
        "beam_id": "Filter4",
        "kvp": 120,
        "hvl_measured_al": 5.123,
        "hvl_measured_cu": 0.227,
    },
    {"beam_id": "Filter5", "kvp": 150, "hvl_measured_cu": 0.339},
    {"beam_id": "Filter6", "kvp": 180, "hvl_measured_cu": 0.504},
    {"beam_id": "Filter7", "kvp": 200, "hvl_measured_cu": 1.042},
    {"beam_id": "Filter8", "kvp": 250, "hvl_measured_cu": 2.117},
]

REF_BEAMS = [
    {
        "beam_farmer_id": "NXJ60",
        "kvp": 60,
        "hvl_measured_cu": None,
        "hvl_measured_al": 0.788813791651093,
        "nk_3587": 49.8986656857429,
        "nk_5447": 50.7,
        "nk_5448": 51.5,
    },
    {
        "beam_farmer_id": "NXK60",
        "kvp": 60,
        "hvl_measured_cu": None,
        "hvl_measured_al": 1.28860110150315,
        "nk_3587": 48.3988130247751,
        "nk_5447": 49.3,
        "nk_5448": 50.1,
    },
]

REF_BEAMS2 = [
    {
        "beam_farmer_id": "NXB120",
        "kvp": 120,
        "hvl_measured_cu": 0.229716813754473,
        "hvl_measured_al": 5.55599697591481,
        "nk_3587": 47.7093008745159,
        "nk_5447": 47.8597516857949,
        "nk_5448": 48.5210001193312,
    },
    {
        "beam_farmer_id": "NXC120",
        "kvp": 120,
        "hvl_measured_cu": 0.280623113903494,
        "hvl_measured_al": 6.37697784783916,
        "nk_3587": 47.7411047431016,
        "nk_5447": 47.8406595597577,
        "nk_5448": 48.4969968164535,
    },
]

REF_BEAMS3 = [
    {
        "beam_farmer_id": "NXE250",
        "kvp": 250,
        "hvl_measured_cu": 1.61280416689842,
        "hvl_measured_al": None,
        "nk_3587": 48.0926889791271,
        "nk_5447": 47.8694372925679,
        "nk_5448": 48.1739224296041,
    },
    {
        "beam_farmer_id": "NXF250",
        "kvp": 250,
        "hvl_measured_cu": 2.13567218440762,
        "hvl_measured_al": None,
        "nk_3587": 48.115151223515,
        "nk_5447": 47.9021260939212,
        "nk_5448": 48.1429169731479,
    },
]

REF_BEAMS4 = [
    {
        "beam_plainparallel_id": "RT5",
        "kvp": 55,
        "hvl_measured_al": 0.8060,
        "nk_1508": 1033.92690609361,
        "nk_858": 82.0878589140421,
    },
    {
        "beam_plainparallel_id": "RT6",
        "kvp": 70,
        "hvl_measured_al": 1.3040,
        "nk_1508": 1025.75342949661,
        "nk_858": 81.7610639245557,
    },
]


# test case: [Farmer] only get hvl_al without hvl_cu (interpolation)
def test_interpo1():
    ans = interpolation(
        REF_BEAMS[0]["nk_3587"],
        REF_BEAMS[1]["nk_3587"],
        REF_BEAMS[0]["hvl_measured_al"],
        REF_BEAMS[1]["hvl_measured_al"],
        BEAMS[0]["hvl_measured_al"],
    )
    assert math.isclose(ans, 48.4606365571043)
    # assert round(ans,5) == round(48.4606365571043, 5)
    # assert abs(ans-48.4606365571043)/48.4606365571043<0.000001


# test case: [Farmer] only get hvl_al without hvl_cu (extrap)
def test_interpo2():
    ans = interpolation(
        REF_BEAMS2[0]["nk_5447"],
        REF_BEAMS2[1]["nk_5447"],
        REF_BEAMS2[0]["hvl_measured_al"],
        REF_BEAMS2[1]["hvl_measured_al"],
        BEAMS[3]["hvl_measured_al"],
    )
    assert math.isclose(ans, 47.8698211443177)


# test case: [Farmer] only get hvl_cu without hvl_al (interpolation)
def test_interpo3():
    ans = interpolation(
        REF_BEAMS3[0]["nk_3587"],
        REF_BEAMS3[1]["nk_3587"],
        REF_BEAMS3[0]["hvl_measured_cu"],
        REF_BEAMS3[1]["hvl_measured_cu"],
        BEAMS[-1]["hvl_measured_cu"],
    )
    assert math.isclose(ans, 48.1143490723882)


# test case: [Farmer] only get hvl_cu without hvl_al (extrap)
def test_interpo4():
    ans = interpolation(
        REF_BEAMS2[0]["nk_5447"],
        REF_BEAMS2[1]["nk_5447"],
        REF_BEAMS2[0]["hvl_measured_cu"],
        REF_BEAMS2[1]["hvl_measured_cu"],
        BEAMS[3]["hvl_measured_cu"],
    )
    assert math.isclose(ans, 47.8607706117524)


# test case: [Farmer] get both hvl_al and hvl_cu (Average nk value)
def test_interpo5():
    ans_al = interpolation(
        REF_BEAMS2[0]["nk_5447"],
        REF_BEAMS2[1]["nk_5447"],
        REF_BEAMS2[0]["hvl_measured_al"],
        REF_BEAMS2[1]["hvl_measured_al"],
        BEAMS[3]["hvl_measured_al"],
    )
    ans_cu = interpolation(
        REF_BEAMS2[0]["nk_5447"],
        REF_BEAMS2[1]["nk_5447"],
        REF_BEAMS2[0]["hvl_measured_cu"],
        REF_BEAMS2[1]["hvl_measured_cu"],
        BEAMS[3]["hvl_measured_cu"],
    )
    ans = (ans_al + ans_cu) / 2
    assert math.isclose(ans, 47.8652958780351)


# test case: [Plain Parallel] interpolation
def test_interpo6():
    ans = interpolation(
        REF_BEAMS4[0]["nk_1508"],
        REF_BEAMS4[1]["nk_1508"],
        REF_BEAMS4[0]["hvl_measured_al"],
        REF_BEAMS4[1]["hvl_measured_al"],
        BEAMS[0]["hvl_measured_al"],
    )
    assert math.isclose(ans, 1026.34428322651)


# TODO test case: [Plain Parallel] extrap
