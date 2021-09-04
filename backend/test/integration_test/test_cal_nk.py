from backend.utility.nk_value import cal_nk_value
import pytest, math

# Later on, cal_nk_value won't return result list, instead stores into db
# basic interpolation (mm Al) (Farmer + PP)
@pytest.mark.parametrize("beams, chambers, expected_nk", [
	([{
		"beam_id": "Filter1",
		"kvp": 60,
		"hvl_measured_al": 1.268,
		"hvl_measured_cu": 0,
	}], ["3587", "5447", "5448", "1508", "858"], [48.46063655710431,
												  49.3166175139252,
												  50.1855243241834,
												  1026.34428322651,
												  81.7846876587354])
])
def test_cal_nk_value1(beams, chambers, expected_nk):
    result = cal_nk_value(beams)

    for i in range(len(result)):
        assert math.isclose(result[i]["nk_"+chambers[i]], expected_nk[i])

# basic interpolation (mm Cu)
@pytest.mark.parametrize("beams, chambers, expected_nk", [
	([{
		"beam_id": "Filter7",
		"kvp": 200,
		"hvl_measured_al": 0,
		"hvl_measured_cu": 1.042,
	}], ["3587", "5447", "5448"], [48.0483942095272,
								   47.8738855378819,
								   48.2376105400211])
])
def test_cal_nk_value2(beams, chambers, expected_nk):
    result = cal_nk_value(beams)

    for i in range(len(result)):
        assert math.isclose(result[i]["nk_" + chambers[i]], expected_nk[i])


# basic interpolation (Average Cu & Al)
@pytest.mark.parametrize("beams, chambers, expected_nk", [
	([{
		"beam_id": "Filter9",
		"kvp": 120,
		"hvl_measured_al": 6.0,
		"hvl_measured_cu": 0.25,
	}], ["3587", "5447", "5448"], [47.7242369531991,
								   47.8507854339079,
								   48.5097274271595])
])
def test_cal_nk_value3(beams, chambers, expected_nk):
    result = cal_nk_value(beams)

    for i in range(len(result)):
        assert math.isclose(result[i]["nk_" + chambers[i]], expected_nk[i])


# Extrapolation (mm Al)
@pytest.mark.parametrize("beams, chambers, expected_nk", [
	([{
		"beam_id": "Filter10",
		"kvp": 120,
		"hvl_measured_al": 5.123,
		"hvl_measured_cu": 0,
	}], ["3587", "5447", "5448"], [47.6925270623713,
								   47.8698211443177,
								   48.5336598022952])
])
def test_cal_nk_value4(beams, chambers, expected_nk):
    result = cal_nk_value(beams)

    for i in range(len(result)):
        assert math.isclose(result[i]["nk_" + chambers[i]], expected_nk[i])


# Extrapolation (mm Cu)
@pytest.mark.parametrize("beams, chambers, expected_nk", [
	([{
		"beam_id": "Filter5",
		"kvp": 150,
		"hvl_measured_al": 0,
		"hvl_measured_cu": 0.339,
	}], ["3587", "5447", "5448"], [47.7766767345878,
								   47.7964424644076,
								   48.3922090028646])
])
def test_cal_nk_value5(beams, chambers, expected_nk):
    result = cal_nk_value(beams)

    for i in range(len(result)):
        assert math.isclose(result[i]["nk_" + chambers[i]], expected_nk[i])


# Extrapolation (Average Cu & Al )
@pytest.mark.parametrize("beams, chambers, expected_nk", [
	([{
		"beam_id": "Filter4",
		"kvp": 120,
		"hvl_measured_al": 5.123,
		"hvl_measured_cu": 0.227,
	}], ["3587", "5447", "5448"], [47.7000652995424,
								   47.8652958780351,
								   48.5279704758695])
])
def test_cal_nk_value5(beams, chambers, expected_nk):
    result = cal_nk_value(beams)

    for i in range(len(result)):
        assert math.isclose(result[i]["nk_" + chambers[i]], expected_nk[i])