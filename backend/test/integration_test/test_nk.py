from backend.utility.nk_value import select_from_farmer, select_from_planeparallel, connect_to_db
import pytest, math

cursor = connect_to_db()
CHAMBER_F = ["nk_3587", "nk_5447", "nk_5448"]
CHAMBER_PP = ["nk_1508", "nk_858"]

# Later on, cal_nk_value won't return result list, instead stores into db
# selection from lookup table (mm Al) (Farmer) (0.789<x<1.289)
@pytest.mark.parametrize("beam, chambers, expected_1, expected_2", [
	({
		 "beam_id": "Filter1",
		 "kvp": 60,
		 "hvl_measured_al": 1.268,
		 "hvl_measured_cu": 0,
	 }, CHAMBER_F, {'nk_3587': 49.8986656857429,
					'nk_5447': 50.7091582474078,
					'nk_5448': 51.5333222138005},
	 {'nk_3587': 48.3988130247751,
	  'nk_5447': 49.2567496118489,
	  'nk_5448': 50.1275799997309})
])
def test_nk0(beam, chambers, expected_1, expected_2):
	first, second = select_from_farmer(cursor, beam["kvp"], beam["hvl_measured_al"], "al")
	for chamber in chambers:
		assert math.isclose(first[chamber], expected_1[chamber])
		assert math.isclose(second[chamber], expected_2[chamber])


# selection from lookup table (mm Al) (PP) (0.8060<x<1.3040)
@pytest.mark.parametrize("beam, chambers, expected_1, expected_2", [
	({
		 "beam_id": "Filter1",
		 "kvp": 60,
		 "hvl_measured_al": 1.268,
		 "hvl_measured_cu": 0,
	 }, CHAMBER_PP, {'nk_1508': 1033.92690609361,
					'nk_858': 82.0878589140421},
	 {'nk_1508': 1025.75342949661,
	  'nk_858': 81.7610639245557})
])
def test_nk1(beam, chambers, expected_1, expected_2):
	first, second = select_from_planeparallel(cursor, beam["kvp"], beam["hvl_measured_al"])
	for chamber in chambers:
		assert math.isclose(first[chamber], expected_1[chamber])
		assert math.isclose(second[chamber], expected_2[chamber])


# selection from lookup table (mm Cu) (Farmer) (0.732<x<1.207)
@pytest.mark.parametrize("beam, chambers, expected_1, expected_2", [
	({
		"beam_id": "Filter7",
		"kvp": 200,
		"hvl_measured_al": 0,
		"hvl_measured_cu": 1.042,
	}, CHAMBER_F, {'nk_3587': 47.9552891833685,
					'nk_5447': 47.8296588552133,
					'nk_5448': 48.2507170572958},
	 {'nk_3587': 48.0980679819206,
	  'nk_5447': 47.8974815375743,
	  'nk_5448': 48.2306178975952})
])
def test_nk2(beam, chambers, expected_1, expected_2):
	first, second = select_from_farmer(cursor, beam["kvp"], beam["hvl_measured_cu"], "cu")
	for chamber in chambers:
		assert math.isclose(first[chamber], expected_1[chamber])
		assert math.isclose(second[chamber], expected_2[chamber])


# selection from lookup table (mm Al) (Farmer) (x<5.556<6.377)
@pytest.mark.parametrize("beam, chambers, expected_1, expected_2", [
	({
		"beam_id": "Filter10",
		"kvp": 120,
		"hvl_measured_al": 5.123,
		"hvl_measured_cu": 0,
	}, CHAMBER_F, {'nk_3587': 47.7093008745159,
					'nk_5447': 47.8597516857949,
					'nk_5448': 48.5210001193312},
	 {'nk_3587': 47.7411047431016,
	  'nk_5447': 47.8406595597577,
	  'nk_5448': 48.4969968164535})
])
def test_nk3(beam, chambers, expected_1, expected_2):
	first, second = select_from_farmer(cursor, beam["kvp"], beam["hvl_measured_al"], "al")
	for chamber in chambers:
		assert math.isclose(first[chamber], expected_1[chamber])
		assert math.isclose(second[chamber], expected_2[chamber])


# selection from lookup table (mm Al) (Farmer) (7.588<10.31<x)
@pytest.mark.parametrize("beam, chambers, expected_1, expected_2", [
	({
		"beam_id": "Filter11",
		"kvp": 120,
		"hvl_measured_al": 11.0,
		"hvl_measured_cu": 0,
	}, CHAMBER_F, {'nk_3587': 47.8983043309663,
					'nk_5447': 47.8525442910740,
					'nk_5448': 48.4140442071126},
	 {'nk_3587': 47.9864799045217,
	  'nk_5447': 47.7827168186771,
	  'nk_5448': 48.2155357397939})
])
def test_nk4(beam, chambers, expected_1, expected_2):
	first, second = select_from_farmer(cursor, beam["kvp"], beam["hvl_measured_al"], "al")
	for chamber in chambers:
		assert math.isclose(first[chamber], expected_2[chamber])
		assert math.isclose(second[chamber], expected_1[chamber])


# selection from lookup table (mm Cu) (Farmer) (x<0.379<0.493)
@pytest.mark.parametrize("beam, chambers, expected_1, expected_2", [
	({
		"beam_id": "Filter5",
		"kvp": 150,
		"hvl_measured_al": 0,
		"hvl_measured_cu": 0.339,
	}, CHAMBER_F, {'nk_3587': 47.8056873399266,
					'nk_5447': 47.8054768418585,
					'nk_5448': 48.3824100048601},
	 {'nk_3587': 47.8894143470063,
	  'nk_5447': 47.8315508026033,
	  'nk_5448': 48.3541292859397})
])
def test_nk5(beam, chambers, expected_1, expected_2):
	first, second = select_from_farmer(cursor, beam["kvp"], beam["hvl_measured_cu"], "cu")
	for chamber in chambers:
		assert math.isclose(first[chamber], expected_1[chamber])
		assert math.isclose(second[chamber], expected_2[chamber])


# selection from lookup table (mm Cu) (Farmer) (1.125<1.383<x)
@pytest.mark.parametrize("beam, chambers, expected_1, expected_2", [
	({
		"beam_id": "Filter5",
		"kvp": 150,
		"hvl_measured_al": 0,
		"hvl_measured_cu": 1.4,
	}, CHAMBER_F, {'nk_3587': 48.0752383270639,
					'nk_5447': 47.8840249463610,
					'nk_5448': 48.1712468469417},
	 {'nk_3587': 47.8920083363291,
	  'nk_5447': 47.6075647943272,
	  'nk_5448': 47.8193210966529})
])
def test_nk5(beam, chambers, expected_1, expected_2):
	first, second = select_from_farmer(cursor, beam["kvp"], beam["hvl_measured_cu"], "cu")
	for chamber in chambers:
		assert math.isclose(first[chamber], expected_2[chamber])
		assert math.isclose(second[chamber], expected_1[chamber])


# Database connection error
# Data read failure
# Data write failure
