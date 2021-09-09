from backend.utility.interpolation import interpolation

import pyodbc

CHAMBER_SN_FARMER = ["3587", "5447", "5448"]
CHAMBER_SN_PP = ["1508", "858"]

"""
###########################
#### Main Calculation #####
###########################
"""

def cal_nk_value(beams):
    # Connect to database
    cursor = connect_to_db()
    # Initialize warn_msg_list
    warn_msg_list = []
    # Loop through each input beam
    for beam in beams:

        # Initialize result list
        result_list = []

        # CHECK if it's Al or Cu or Both
        HVL_type = check_HVL_Al_Cu(beam)

        # DEBUG
        # print(beam["beam_id"], beam)

        # Both HVL_Al and HVL_Cu exist
        if HVL_type["Al"] and HVL_type["Cu"]:
            first_beam_al, second_beam_al, warn_status_al = select_from_farmer(
                cursor, beam["kvp"], beam["hvl_measured_al"], "al"
            )
            first_beam_cu, second_beam_cu, warn_status_cu = select_from_farmer(
                cursor, beam["kvp"], beam["hvl_measured_cu"], "cu"
            )
            # Warning message
            if not warn_status_al:
                warn_msg = {}
                warn_msg["beam_id"] = beam["beam_id"]
                warn_msg["message"] = "Extrapolation_Nk_Al"
                warn_msg_list.append(warn_msg)

            if not warn_status_cu:
                warn_msg = {}
                warn_msg["beam_id"] = beam["beam_id"]
                warn_msg["message"] = "Extrapolation_Nk_Cu"
                warn_msg_list.append(warn_msg)

            for chamber in CHAMBER_SN_FARMER:
                nk_al = interpolation(
                    first_beam_al["nk_" + chamber],
                    second_beam_al["nk_" + chamber],
                    first_beam_al["hvl_al"],
                    second_beam_al["hvl_al"],
                    beam["hvl_measured_al"]
                )
                nk_cu = interpolation(
                    first_beam_cu["nk_" + chamber],
                    second_beam_cu["nk_" + chamber],
                    first_beam_cu["hvl_cu"],
                    second_beam_cu["hvl_cu"],
                    beam["hvl_measured_cu"]
                )
                # Average the results
                result = {"id": beam["beam_id"],
                          "nk_" + chamber: (nk_al + nk_cu) / 2}
                result_list.append(result)

        # Only HVL_Al
        elif HVL_type["Al"]:
            first_beam, second_beam, warn_status_al = select_from_farmer(
                cursor, beam["kvp"], beam["hvl_measured_al"], "al"
            )
            # Warning message
            if not warn_status_al:
                warn_msg = {}
                warn_msg["beam_id"] = beam["beam_id"]
                warn_msg["message"] = "Extrapolation_Nk_Al"
                warn_msg_list.append(warn_msg)

            for chamber in CHAMBER_SN_FARMER:
                result = {
                    "id": beam["beam_id"],
                    "nk_"
                    + chamber: interpolation(
                        first_beam["nk_" + chamber],
                        second_beam["nk_" + chamber],
                        first_beam["hvl_al"],
                        second_beam["hvl_al"],
                        beam["hvl_measured_al"]
                    )
                }
                result_list.append(result)

        # Only HVL_Cu
        elif HVL_type["Cu"]:
            first_beam, second_beam, warn_status_cu = select_from_farmer(
                cursor, beam["kvp"], beam["hvl_measured_cu"], "cu"
            )
            # Warning message
            if not warn_status_cu:
                warn_msg = {}
                warn_msg["beam_id"] = beam["beam_id"]
                warn_msg["message"] = "Extrapolation_Nk_Cu"
                warn_msg_list.append(warn_msg)

            for chamber in CHAMBER_SN_FARMER:
                result = {
                    "id": beam["beam_id"],
                    "nk_"
                    + chamber: interpolation(
                        first_beam["nk_" + chamber],
                        second_beam["nk_" + chamber],
                        first_beam["hvl_cu"],
                        second_beam["hvl_cu"],
                        beam["hvl_measured_cu"]
                    )
                }
                result_list.append(result)

        # Check Plane-Parallel-Type
        if HVL_type["Al"] and beam["hvl_measured_al"] <= 2.204:
            first_beam, second_beam = select_from_planeparallel(
                cursor, beam["kvp"], beam["hvl_measured_al"]
            )
            for chamber in CHAMBER_SN_PP:
                result = {
                    "id": beam["beam_id"],
                    "nk_"
                    + chamber: interpolation(
                        first_beam["nk_" + chamber],
                        second_beam["nk_" + chamber],
                        first_beam["hvl_al"],
                        second_beam["hvl_al"],
                        beam["hvl_measured_al"]
                    )
                }
                result_list.append(result)

        # TODO: Insert results into database
        storeIntoDb()
        # DEBUG
        print(result_list)
        print("----------------------")

    # DEBUG
    print(warn_msg_list)


"""
###########################
#### Helper functions #####
###########################
"""

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


def select_input_from_db(cursor):
    beams = []
    input_table = cursor.execute('SELECT beam_id, '
                                 'nom_energy, '
                                 'hvl_measured_mm_al, '
                                 'hvl_measured_mm_cu '
                                 'FROM beam_data')
    for key, value in enumerate(input_table):
        beam = {"beam_id": (value)[0],
                "kvp": (value)[1],
                "hvl_measured_al": (value)[2],
                "hvl_measured_cu": (value)[3]}
        beams.append(beam)
    # DEBUG
    # print(beams)
    return beams


def check_HVL_Al_Cu(input):
    HVL_type = {"Al": False, "Cu": False}
    if input["hvl_measured_al"] != 0:
        HVL_type["Al"] = True
    if input["hvl_measured_cu"] != 0:
        HVL_type["Cu"] = True

    return HVL_type


# Select 2 closest beams from Farmer-Type-Chamber table
def select_from_farmer(cursor, kvp, hvl, type):

    # Kvp not be bound in the existed kvp
    if not cursor.execute(
        "SELECT * FROM beam_farmer_list WHERE kV={}".format(kvp)
    ).fetchall():
        (closest_kvp,) = cursor.execute('SELECT kV FROM beam_farmer_list '
                                'WHERE (kV - {})>=0 '
                                'ORDER BY (kV - {})'
                                .format(kvp, kvp)).fetchone()
        kvp = int(closest_kvp)

    # Kvp is bound
    lower_check = cursor.execute(
        "SELECT * FROM beam_farmer_list "
        "WHERE hvl_measured_mm_{}<={} AND kV={}".format(type, hvl, kvp)
    ).fetchall()
    upper_check = cursor.execute(
        "SELECT * FROM beam_farmer_list "
        "WHERE hvl_measured_mm_{}>={} AND kV={}".format(type, hvl, kvp)
    ).fetchall()

    # HVL in the scope (INTERPOLATION)
    if lower_check != [] and upper_check != []:
        lower_table = cursor.execute(
            "SELECT beam_farmer_id, chamber_SN, nk_value FROM "
            + "beam_farmer_chamber "
            + "WHERE "
            + "beam_farmer_id "
            + "IN "
            + "( SELECT TOP 1 "
            + "beam_farmer_id "
            + "FROM "
            + "beam_farmer_list "
            + "WHERE "
            + "hvl_measured_mm_{}<={} AND kV={} ".format(type, hvl, kvp)
            + "ORDER BY "
            + "hvl_measured_mm_{} ".format(type)
            + "DESC)"
        ).fetchall()
        upper_table = cursor.execute(
            "SELECT beam_farmer_id, chamber_SN, nk_value FROM "
            + "beam_farmer_chamber "
            + "WHERE "
            + "beam_farmer_id "
            + "IN "
            + "( SELECT TOP 1 "
            + "beam_farmer_id "
            + "FROM "
            + "beam_farmer_list "
            + "WHERE "
            + "hvl_measured_mm_{}>={} AND kV={} ".format(type, hvl, kvp)
            + "ORDER BY "
            + "hvl_measured_mm_{} ".format(type)
            + "ASC)"
        ).fetchall()
        lower_beam, upper_beam = {}, {}
        # TODO: REFACTOR
        # Extract NK from each Chamber_SN
        for beam_id, chamber_SN, nk in lower_table:
            lower_beam["id"] = beam_id
            lower_beam["nk_" + chamber_SN] = nk
        for beam_id, chamber_SN, nk in upper_table:
            upper_beam["id"] = beam_id
            upper_beam["nk_" + chamber_SN] = nk

        # Extract HVL
        (lower_hvl,) = cursor.execute(
            "SELECT hvl_measured_mm_{} FROM beam_farmer_list "
            "WHERE beam_farmer_id='{}'".format(type, lower_beam["id"])
        ).fetchone()
        (upper_hvl,) = cursor.execute(
            "SELECT hvl_measured_mm_{} FROM beam_farmer_list "
            "WHERE beam_farmer_id='{}'".format(type, upper_beam["id"])
        ).fetchone()
        lower_beam["hvl_" + type], upper_beam["hvl_" + type] = \
            lower_hvl, upper_hvl

        return lower_beam, upper_beam, True

    # HVL not in the scope (EXTRAPOLATION)
    first_beam, second_beam, extrap_table = {}, {}, []
    if not lower_check:
        extrap_table = cursor.execute(
            "SELECT beam_farmer_id, chamber_SN, nk_value FROM "
            + "beam_farmer_chamber "
            + "WHERE "
            + "beam_farmer_id "
            + "IN (SELECT TOP 2 beam_farmer_id "
            + "FROM "
            + "beam_farmer_list "
            + "WHERE "
            + "hvl_measured_mm_{}>={} AND kV={} ".format(type, hvl, kvp)
            + "ORDER BY "
            + "hvl_measured_mm_{})".format(type)
        ).fetchall()
        (first_beam["id"], _, _), (second_beam["id"], _, _) = (
            extrap_table[0],
            extrap_table[1],
        )
    if not upper_check:
        extrap_table = cursor.execute(
            "SELECT beam_farmer_id, chamber_SN, nk_value FROM "
            + "beam_farmer_chamber "
            + "WHERE "
            + "beam_farmer_id "
            + "IN (SELECT TOP 2 beam_farmer_id "
            + "FROM "
            + "beam_farmer_list "
            + "WHERE "
            + "hvl_measured_mm_{}<={} AND kV={} ".format(type, hvl, kvp)
            + "ORDER BY "
            + "hvl_measured_mm_{} DESC)".format(type)
        ).fetchall()

        (first_beam["id"], _, _), (second_beam["id"], _, _) = (
            extrap_table[1],
            extrap_table[0],
        )

    # Extract Nk from each Chamber_SN
    for beam_id, chamber_SN, nk in extrap_table:
        if beam_id == first_beam["id"]:
            first_beam["nk_" + chamber_SN] = nk
        if beam_id == second_beam["id"]:
            second_beam["nk_" + chamber_SN] = nk

    # Extract HVL
    (first_hvl,) = cursor.execute(
        "SELECT hvl_measured_mm_{} FROM beam_farmer_list "
        "WHERE beam_farmer_id='{}'".format(type, first_beam["id"])
    ).fetchone()
    (second_hvl,) = cursor.execute(
        "SELECT hvl_measured_mm_{} FROM beam_farmer_list "
        "WHERE beam_farmer_id='{}'".format(type, second_beam["id"])
    ).fetchone()
    first_beam["hvl_" + type], second_beam["hvl_" + type] = \
        first_hvl, second_hvl

    return first_beam, second_beam, False


# Select 2 closest beams from PlaneParallel-Type-Chamber table
def select_from_planeparallel(cursor, kvp, hvl, type="al"):
    # TODO: Scenario that hvl is smaller than 0.1122?
    lower_table = cursor.execute("SELECT TOP 2 "
                                 "beam_pp_chamber_id, "
                                 "a.beam_planeparallel_id, "
                                 "chamber_SN, "
                                 "hvl_measured_mm_al "
                                 "FROM "
                                 "beam_planeparallel_chamber as a "
                                 "LEFT JOIN "
                                 "beam_planeparallel_list as b "
                                 "ON a.beam_planeparallel_id"
                                 "=b.beam_planeparallel_id "
                                 "WHERE "
                                 "hvl_measured_mm_al <={} ".format(hvl)+
                                 "ORDER BY "
                                 "hvl_measured_mm_al "
                                 "DESC").fetchall()
    upper_table = cursor.execute("SELECT TOP 2 "
                                 "beam_pp_chamber_id, "
                                 "a.beam_planeparallel_id, "
                                 "chamber_SN, "
                                 "hvl_measured_mm_al "
                                 "FROM "
                                 "beam_planeparallel_chamber as a "
                                 "LEFT JOIN "
                                 "beam_planeparallel_list as b "
                                 "ON a.beam_planeparallel_id"
                                 "=b.beam_planeparallel_id "
                                 "WHERE "
                                 "hvl_measured_mm_al >={} ".format(hvl)+
                                 "ORDER BY "
                                 "hvl_measured_mm_al").fetchall()

    lower_beam, upper_beam = {}, {}
    # TODO: REFACTOR
    # Extract value from results
    for beam_chamber_id, beam_id, chamber_SN, ref_hvl in lower_table:
        (lower_nk,) = cursor.execute(
            "SELECT nk_value FROM beam_planeparallel_nk "
            "WHERE beam_pp_chamber_id='{}'".format(beam_chamber_id)
        ).fetchone()
        lower_beam["id"] = beam_id
        lower_beam["hvl_al"] = ref_hvl
        lower_beam["nk_" + chamber_SN] = lower_nk
    for beam_chamber_id, beam_id, chamber_SN, ref_hvl in upper_table:
        (upper_nk,) = cursor.execute(
            "SELECT nk_value FROM beam_planeparallel_nk "
            "WHERE beam_pp_chamber_id='{}'".format(beam_chamber_id)
        ).fetchone()
        upper_beam["id"] = beam_id
        upper_beam["hvl_al"] = ref_hvl
        upper_beam["nk_" + chamber_SN] = upper_nk

    return lower_beam, upper_beam


# DB query: Store data into Db
def storeIntoDb():
    # TODO: INSERT ...
    return 0


# DEBUG
if __name__ == "__main__":
    cursor = connect_to_db()

    # Retrieve input data
    beams = select_input_from_db(cursor)
    # SpringfieldElementary examples
    # beams = [{'beam_id': 'BEAM_FILTER1', 'kvp': 30.0, 'hvl_measured_al': 0.19, 'hvl_measured_cu': 0.0},
    #          {'beam_id': 'BEAM_FILTER2', 'kvp': 50.0, 'hvl_measured_al': 0.81, 'hvl_measured_cu': 0.0},
    #          {'beam_id': 'BEAM_FILTER3', 'kvp': 80.0, 'hvl_measured_al': 2.01, 'hvl_measured_cu': 0.0},
    #          {'beam_id': 'BEAM_FILTER4', 'kvp': 95.0, 'hvl_measured_al': 2.61, 'hvl_measured_cu': 0.0},
    #          {'beam_id': 'BEAM_FILTER5', 'kvp': 100.0, 'hvl_measured_al': 4.02, 'hvl_measured_cu': 0.0}]

    cal_nk_value(beams)
