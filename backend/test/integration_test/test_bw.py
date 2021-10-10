from backend.utility.Bw_value import cal_Bw_value
import pytest, math
import pyodbc# from backend.utility.start_calculate import connect_to_db
def connect_to_db():
    try:
        connection = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=13.70.131.250,1433;"
            "Database=violet_dev;"
            "Uid=SA;"
            "PWD=ProjViolet_1;"
            "Trusted_Connection=no;"
        )
        # Create cursor object
        return connection.cursor()

    except pyodbc.Error as ex:
        raise Exception(ex.args[1])
cursor = connect_to_db()

@pytest.mark.parametrize("beam, cone, expect", [
    ([
        {"beam_id": "Filter1", "kvp": 60, "hvl_measured_al": 1.2, "hvl_measured_cu": None},
        {"beam_id": "Filter4", "kvp": 120, "hvl_measured_al": 5, "hvl_measured_cu": 0.2},
        {"beam_id": "Filter5", "kvp": 150, "hvl_measured_al": None, "hvl_measured_cu": 0.3}
    ], 
    [
        {"cone_id": "E", "SSD": 30, "diameter": 5}
    ], 
    {
        "Filter1_E" : {"Bw_Al" : 1.142, "Bw_Combined" : 1.142}, 
        "Filter4_E" : {"Bw_Al" : 1.242, "Bw_Cu" : 1.242, "Bw_Combined" : 1.242}, 
        "Filter5_E" : {"Bw_Cu" : 1.242, "Bw_Combined" : 1.242}
    })
])
def test_no_interpolation(beam, cone, expect):
    bw_res = cal_Bw_value(cursor, beam, cone)
    for beam_cone in bw_res:
        for bw in bw_res[beam_cone]:
            assert math.isclose(bw_res[beam_cone][bw], expect[beam_cone][bw])

@pytest.mark.parametrize("beam, cone, expect", [
    ([
        {"beam_id": "Filter1", "kvp": 60, "hvl_measured_al": 1.268, "hvl_measured_cu": None},
        {"beam_id": "Filter4", "kvp": 120, "hvl_measured_al": 5.123, "hvl_measured_cu": 0.227},
        {"beam_id": "Filter5", "kvp": 150, "hvl_measured_al": None, "hvl_measured_cu": 0.339}
    ], 
    [
        {"cone_id": "E", "SSD": 30, "diameter": 5}
    ], 
    {
        "Filter1_E" : {"Bw_Al" : 1.1454, "Bw_Combined" : 1.1454}, 
        "Filter4_E" : {"Bw_Al" : 1.242, "Bw_Cu" : 1.242, "Bw_Combined" : 1.242}, 
        "Filter5_E" : {"Bw_Cu" : 1.24083, "Bw_Combined" : 1.24083}
    })
])
def test_hvl_interpolation(beam, cone, expect):
    bw_res = cal_Bw_value(cursor, beam, cone)
    for beam_cone in bw_res:
        for bw in bw_res[beam_cone]:
            assert math.isclose(bw_res[beam_cone][bw], expect[beam_cone][bw])


@pytest.mark.parametrize("beam, cone, expect", [
    ([
        {"beam_id": "Filter1", "kvp": 60, "hvl_measured_al": 1.2, "hvl_measured_cu": None},
        {"beam_id": "Filter4", "kvp": 120, "hvl_measured_al": 5, "hvl_measured_cu": 0.2},
        {"beam_id": "Filter5", "kvp": 150, "hvl_measured_al": None, "hvl_measured_cu": 0.3}
    ], 
    [
        {"cone_id": "E", "SSD": 35, "diameter": 5}
    ], 
    {
        "Filter1_E" : {"Bw_Al" : 1.14225, "Bw_Combined" : 1.14225}, 
        "Filter4_E" : {"Bw_Al" : 1.24175, "Bw_Cu" : 1.2415, "Bw_Combined" : 1.241625}, 
        "Filter5_E" : {"Bw_Cu" : 1.24325, "Bw_Combined" : 1.24325}
    })
])
def test_ssd_interpolation(beam, cone, expect):
    bw_res = cal_Bw_value(cursor, beam, cone)
    for beam_cone in bw_res:
        for bw in bw_res[beam_cone]:
            assert math.isclose(bw_res[beam_cone][bw], expect[beam_cone][bw])

@pytest.mark.parametrize("beam, cone, expect", [
    ([
        {"beam_id": "Filter1", "kvp": 60, "hvl_measured_al": 1.2, "hvl_measured_cu": None},
        {"beam_id": "Filter4", "kvp": 120, "hvl_measured_al": 5, "hvl_measured_cu": 0.2},
        {"beam_id": "Filter5", "kvp": 150, "hvl_measured_al": None, "hvl_measured_cu": 0.3}
    ], 
    [
        {"cone_id": "E", "SSD": 30, "diameter": 8}
    ], 
    {
        "Filter1_E" : {"Bw_Al" : 1.1618, "Bw_Combined" : 1.1618}, 
        "Filter4_E" : {"Bw_Al" : 1.3068, "Bw_Cu" : 1.3056, "Bw_Combined" : 1.3062}, 
        "Filter5_E" : {"Bw_Cu" : 1.3146, "Bw_Combined" : 1.3146}
    })
])
def test_diameter_interpolation(beam, cone, expect):
    bw_res = cal_Bw_value(cursor, beam, cone)
    for beam_cone in bw_res:
        for bw in bw_res[beam_cone]:
            assert math.isclose(bw_res[beam_cone][bw], expect[beam_cone][bw])



@pytest.mark.parametrize("beam, cone, expect", [
    ([
        {"beam_id": "Filter1", "kvp": 60, "hvl_measured_al": 1.268, "hvl_measured_cu": None},
        {"beam_id": "Filter4", "kvp": 120, "hvl_measured_al": 5.123, "hvl_measured_cu": 0.227},
        {"beam_id": "Filter5", "kvp": 150, "hvl_measured_al": None, "hvl_measured_cu": 0.339}
    ], 
    [
        {"cone_id": "E", "SSD": 35, "diameter": 5}
    ], 
    {
        "Filter1_E" : {"Bw_Al" : 1.145706666667, "Bw_Combined" : 1.145706666667}, 
        "Filter4_E" : {"Bw_Al" : 1.24190375, "Bw_Cu" : 1.2419725, "Bw_Combined" : 1.241938125}, 
        "Filter5_E" : {"Bw_Cu" : 1.24208, "Bw_Combined" : 1.24208}
    })
])
def test_hvl_ssd_interpolation(beam, cone, expect):
    bw_res = cal_Bw_value(cursor, beam, cone)
    for beam_cone in bw_res:
        for bw in bw_res[beam_cone]:
            assert math.isclose(bw_res[beam_cone][bw], expect[beam_cone][bw])


@pytest.mark.parametrize("beam, cone, expect", [
    ([
        {"beam_id": "Filter1", "kvp": 60, "hvl_measured_al": 1.268, "hvl_measured_cu": None},
        {"beam_id": "Filter4", "kvp": 120, "hvl_measured_al": 5.123, "hvl_measured_cu": 0.227},
        {"beam_id": "Filter5", "kvp": 150, "hvl_measured_al": None, "hvl_measured_cu": 0.339}
    ], 
    [
        {"cone_id": "E", "SSD": 30, "diameter": 8}
    ], 
    {
        "Filter1_E" : {"Bw_Al" : 1.166424, "Bw_Combined" : 1.166424}, 
        "Filter4_E" : {"Bw_Al" : 1.307538, "Bw_Cu" : 1.30803, "Bw_Combined" : 1.307784}, 
        "Filter5_E" : {"Bw_Cu" : 1.314834, "Bw_Combined" : 1.314834}
    })
])
def test_hvl_diameter_interpolation(beam, cone, expect):
    bw_res = cal_Bw_value(cursor, beam, cone)
    for beam_cone in bw_res:
        for bw in bw_res[beam_cone]:
            assert math.isclose(bw_res[beam_cone][bw], expect[beam_cone][bw])


@pytest.mark.parametrize("beam, cone, expect", [
    ([
        {"beam_id": "Filter1", "kvp": 60, "hvl_measured_al": 1.2, "hvl_measured_cu": None},
        {"beam_id": "Filter4", "kvp": 120, "hvl_measured_al": 5, "hvl_measured_cu": 0.2},
        {"beam_id": "Filter5", "kvp": 150, "hvl_measured_al": None, "hvl_measured_cu": 0.3}
    ], 
    [
        {"cone_id": "E", "SSD": 35, "diameter": 8}
    ], 
    {
        "Filter1_E" : {"Bw_Al" : 1.1622, "Bw_Combined" : 1.1622}, 
        "Filter4_E" : {"Bw_Al" : 1.307, "Bw_Cu" : 1.3057, "Bw_Combined" : 1.30635}, 
        "Filter5_E" : {"Bw_Cu" : 1.3157, "Bw_Combined" : 1.3157}
    })
])
def test_ssd_diameter_interpolation(beam, cone, expect):
    bw_res = cal_Bw_value(cursor, beam, cone)
    for beam_cone in bw_res:
        for bw in bw_res[beam_cone]:
            assert math.isclose(bw_res[beam_cone][bw], expect[beam_cone][bw])


@pytest.mark.parametrize("beam, cone, expect", [
    ([
        {"beam_id": "Filter1", "kvp": 60, "hvl_measured_al": 1.268, "hvl_measured_cu": None},
        {"beam_id": "Filter4", "kvp": 120, "hvl_measured_al": 5.123, "hvl_measured_cu": 0.227},
        {"beam_id": "Filter5", "kvp": 150, "hvl_measured_al": None, "hvl_measured_cu": 0.339}
    ], 
    [
        {"cone_id": "E", "SSD": 35, "diameter": 8}
    ], 
    {
        "Filter1_E" : {"Bw_Al" : 1.166880666667, "Bw_Combined" : 1.166880666667}, 
        "Filter4_E" : {"Bw_Al" : 1.30781795, "Bw_Cu" : 1.3084, "Bw_Combined" : 1.308108975}, 
        "Filter5_E" : {"Bw_Cu" : 1.316051, "Bw_Combined" : 1.316051}
    })
])
def test_hvl_ssd_diameter_interpolation(beam, cone, expect):
    bw_res = cal_Bw_value(cursor, beam, cone)
    for beam_cone in bw_res:
        for bw in bw_res[beam_cone]:
            assert math.isclose(bw_res[beam_cone][bw], expect[beam_cone][bw])
# Check diameter calculation.