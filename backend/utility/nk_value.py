from backend.utility.interpolation import interpolation

import pyodbc

# TODO: collect input data from DB?
# input data from the `identification` sheet

BEAMS = [
    {
        "beam_id": "Filter1",
        "kvp": 60,
        "hvl_measured_al": 1.268,
        "hvl_measured_cu": None,
    },
    {
        "beam_id": "Filter2",
        "kvp": 80,
        "hvl_measured_al": 2.321,
        "hvl_measured_cu": None,
    },
    {
        "beam_id": "Filter3",
        "kvp": 100,
        "hvl_measured_al": 2.881,
        "hvl_measured_cu": None,
    },
    {
        "beam_id": "Filter4",
        "kvp": 120,
        "hvl_measured_al": 5.123,
        "hvl_measured_cu": 0.227,
    },
    {
        "beam_id": "Filter5",
        "kvp": 150,
        "hvl_measured_al": None,
        "hvl_measured_cu": 0.339,
    },
    {
        "beam_id": "Filter6",
        "kvp": 180,
        "hvl_measured_al": None,
        "hvl_measured_cu": 0.504,
    },
    {
        "beam_id": "Filter7",
        "kvp": 200,
        "hvl_measured_al": None,
        "hvl_measured_cu": 1.042,
    },
    {
        "beam_id": "Filter8",
        "kvp": 250,
        "hvl_measured_al": None,
        "hvl_measured_cu": 2.117,
    },
]

CHAMBER_SN_FARMER = ["3587", "5447", "5448"]
CHAMBER_SN_PP = ["1508", "858"]

"""
###########################
#### Main Calculation #####
###########################
"""

def cal_nk_value(beams):

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
    cursor = connection.cursor()

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
            first_beam_al, second_beam_al = select_from_farmer(
                cursor, beam["kvp"], beam["hvl_measured_al"], "al"
            )
            first_beam_cu, second_beam_cu = select_from_farmer(
                cursor, beam["kvp"], beam["hvl_measured_cu"], "cu"
            )

            for chamber in CHAMBER_SN_FARMER:
                nk_al = interpolation(
                    first_beam_al["nk_" + chamber],
                    second_beam_al["nk_" + chamber],
                    first_beam_al["hvl_al"],
                    second_beam_al["hvl_al"],
                    beam["hvl_measured_al"],
                )
                nk_cu = interpolation(
                    first_beam_cu["nk_" + chamber],
                    second_beam_cu["nk_" + chamber],
                    first_beam_cu["hvl_cu"],
                    second_beam_cu["hvl_cu"],
                    beam["hvl_measured_cu"],
                )
                # Average the results
                result = {"id": beam["beam_id"],
                          "nk_" + chamber: (nk_al + nk_cu) / 2}
                result_list.append(result)

        # Only HVL_Al
        elif HVL_type["Al"]:
            first_beam, second_beam = select_from_farmer(
                cursor, beam["kvp"], beam["hvl_measured_al"], "al"
            )

            for chamber in CHAMBER_SN_FARMER:
                result = {
                    "id": beam["beam_id"],
                    "nk_"
                    + chamber: interpolation(
                        first_beam["nk_" + chamber],
                        second_beam["nk_" + chamber],
                        first_beam["hvl_al"],
                        second_beam["hvl_al"],
                        beam["hvl_measured_al"],
                    ),
                }
                result_list.append(result)

        # Only HVL_Cu
        elif HVL_type["Cu"]:
            first_beam, second_beam = select_from_farmer(
                cursor, beam["kvp"], beam["hvl_measured_cu"], "cu"
            )

            for chamber in CHAMBER_SN_FARMER:
                result = {
                    "id": beam["beam_id"],
                    "nk_"
                    + chamber: interpolation(
                        first_beam["nk_" + chamber],
                        second_beam["nk_" + chamber],
                        first_beam["hvl_cu"],
                        second_beam["hvl_cu"],
                        beam["hvl_measured_cu"],
                    ),
                }
                result_list.append(result)

        # Check Plane-Parallel-Type
        if HVL_type["Al"] and beam["hvl_measured_al"] <= 2.204:
            first_beam, second_beam = selectDbPP(
                cursor, beam["kvp"], beam["hvl_measured_al"]
            )
            # TODO: Interpolation

        # TODO: Insert results into database
        storeIntoDb()
        # DEBUG
        # print(result_list)
        # print("----------------------")

        return result_list  # for testing


"""
###########################
#### Helper functions #####
###########################
<<<<<<< HEAD
"""

def check_HVL_Al_Cu(input):
    HVL_type = {"Al": False, "Cu": False}
    if input["hvl_measured_al"] is not None:
        HVL_type["Al"] = True
    if input["hvl_measured_cu"] is not None:
        HVL_type["Cu"] = True

    return HVL_type


# Select 2 closest beams from Farmer-Type-Chamber table
def select_from_farmer(cursor, kvp, hvl, type):

    # Kvp not be bound in the table
    if not cursor.execute(
        "SELECT * FROM beam_farmer_list WHERE kV={}".format(kvp)
    ).fetchall():
        (lower_kvp,) = cursor.execute(
            "SELECT TOP 1 kV FROM beam_farmer_list "
            "WHERE kV<={} ORDER BY kV DESC".format(kvp)
        ).fetchone()
        (upper_kvp,) = cursor.execute(
            "SELECT TOP 1 kV FROM beam_farmer_list "
            "WHERE kV>={} ORDER BY kV".format(kvp)
        ).fetchone()
        first_lower_beam, second_lower_beam = select_from_farmer(
            cursor, lower_kvp, hvl, type
        )
        first_upper_beam, second_upper_beam = select_from_farmer(
            cursor, upper_kvp, hvl, type
        )

        lower_beam, upper_beam = {
            "id": first_lower_beam["id"] + "+" + first_upper_beam["id"]
        }, {"id": second_lower_beam["id"] + "+" + second_upper_beam["id"]}
        for k, v in first_lower_beam.items():
            if k != "id":
                lower_beam[k] = interpolation(
                    first_lower_beam[k],
                    first_upper_beam[k],
                    lower_kvp,
                    upper_kvp,
                    kvp
                )
                upper_beam[k] = interpolation(
                    second_lower_beam[k],
                    second_upper_beam[k],
                    lower_kvp,
                    upper_kvp,
                    kvp,
                )
                # lower_beam[k] = interpolation(first_lower_beam[k],
                # second_lower_beam[k], first_lower_beam["hvl_cu"],
                # second_lower_beam["hvl_cu"], hvl)
                # upper_beam[k] = interpolation(first_upper_beam[k],
                # second_upper_beam[k], first_upper_beam["hvl_cu"],
                # second_upper_beam["hvl_cu"], hvl)

        return lower_beam, upper_beam

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

        return lower_beam, upper_beam

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

    return first_beam, second_beam


# DB query: Look up plain parallel type table


def selectDbPP(cursor, kvp, hvl, type="al"):
    # TODO: SELECT ...
    return "first", "second"


# DB query: Store data into Db
def storeIntoDb():
    # TODO: INSERT ...
    return 0


# DEBUG
# if __name__ == "__main__":
#     cal_nk_value(BEAMS)
