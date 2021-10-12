from backend.utility.interpolation import interpolation


CHAMBER_SN_FARMER = ["3587", "5447", "5448"]
CHAMBER_SN_PP = ["1508", "858"]


###########################
#### Main Calculation #####
###########################

'''
Main function for calculating NK
@:param beams: a list of dictionaries
'''
def cal_nk_value(cursor, beams):
    # Initialize result_list, warn_msg_list
    result_list, warn_msg_list = [], []
    # Loop through each input beam
    for beam in beams:

        # CHECK if it's Al or Cu or Both
        HVL_type = check_HVL_Al_Cu(beam)

        # DEBUG
        # print(beam["beam_id"], beam)

        # Both HVL_Al and HVL_Cu exist
        if HVL_type["Al"] and HVL_type["Cu"]:
            first_beam_al, second_beam_al, warn_status_al = \
                select_from_farmer(
                cursor, beam["kvp"], beam["hvl_measured_al"], "al"
            )
            first_beam_cu, second_beam_cu, warn_status_cu = \
                select_from_farmer(
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
                          chamber: (nk_al + nk_cu) / 2}
                result_list.append(result)

        # Only HVL_Al
        elif HVL_type["Al"]:
            first_beam, second_beam, warn_status_al = \
                select_from_farmer(
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
                    chamber: interpolation(
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
                    chamber: interpolation(
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
                    chamber: interpolation(
                        first_beam["nk_" + chamber],
                        second_beam["nk_" + chamber],
                        first_beam["hvl_al"],
                        second_beam["hvl_al"],
                        beam["hvl_measured_al"]
                    )
                }
                result_list.append(result)

        # DEBUG
        # print(beam_result_list)
        # print("----------------------")

    # DEBUG
    # print(warn_msg_list)
    return result_list, warn_msg_list


"""
###########################
#### Helper functions #####
###########################
"""

'''
Check the type of HVL
@:param input: dictionary, the data of a beam
@:return HVL_type: dictionary, hvl type
'''
def check_HVL_Al_Cu(input):
    HVL_type = {"Al": False, "Cu": False}
    if input["hvl_measured_al"]:
        HVL_type["Al"] = True
    if input["hvl_measured_cu"]:
        HVL_type["Cu"] = True

    return HVL_type


'''
Select 2 closest beams from Farmer-Type-Chamber table
@:param cursor: Object, a cursor object
@:param kvp: float, kvp value
@:param hvl: float, hvl value
@:param type: string, the type of hvl (al or cu)
@:return first_beam: the lower boundary 
@:return second_beam: the upper boundary
@:return boolean, extrap or not
'''
def select_from_farmer(cursor, kvp, hvl, type):

    # retrieve latest lookup table
    (latest_date,) = cursor.execute("SELECT TOP 1 date_updated "
                                    "FROM beam_farmer_chamber "
                                    "ORDER BY date_updated "
                                    "DESC").fetchone()
    latest_date = latest_date.strftime('%Y-%m-%d')

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
            + "DESC) "
            + "AND date_updated='{}'".format(latest_date)
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
            + "ASC) "
            + "AND date_updated='{}'".format(latest_date)
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

        if lower_beam == {} or upper_beam == {}:
            raise Exception("Invalid Lookup data from database")

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
            + "hvl_measured_mm_{}) ".format(type)
            + "AND date_updated='{}'".format(latest_date)
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
            + "hvl_measured_mm_{} DESC) ".format(type)
            + "AND date_updated='{}'".format(latest_date)
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

    if first_beam == {} or second_beam == {}:
        raise Exception("Invalid Lookup data from database")

    return first_beam, second_beam, False


'''
Select 2 closest beams from PlaneParallel-Type-Chamber table
@:param cursor: Object, a cursor object
@:param kvp: float, kvp value
@:param hvl: float, hvl value
@:param type: string, the type of hvl (default: al) 
@:return lower_beam: the lower boundary 
@:return upper_beam: the upper boundary
'''
def select_from_planeparallel(cursor, kvp, hvl, type="al"):
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
    # retrieve the latest lookup table
    (latest_date,) = cursor.execute("SELECT TOP 1 date_updated "
                                 "FROM beam_planeparallel_nk "
                                 "ORDER BY date_updated "
                                 "DESC").fetchone()
    latest_date = latest_date.strftime('%Y-%m-%d')

    # TODO: REFACTOR
    # Extract value from results
    for beam_chamber_id, beam_id, chamber_SN, ref_hvl in lower_table:
        (lower_nk,) = cursor.execute(
            "SELECT nk_value FROM beam_planeparallel_nk "
            "WHERE beam_pp_chamber_id='{}' ".format(beam_chamber_id)+
            "AND date_updated='{}'".format(latest_date)
        ).fetchone()
        lower_beam["id"] = beam_id
        lower_beam["hvl_al"] = ref_hvl
        lower_beam["nk_" + chamber_SN] = lower_nk
    for beam_chamber_id, beam_id, chamber_SN, ref_hvl in upper_table:
        (upper_nk,) = cursor.execute(
            "SELECT nk_value FROM beam_planeparallel_nk "
            "WHERE beam_pp_chamber_id='{}' ".format(beam_chamber_id)+
            "AND date_updated='{}'".format(latest_date)
        ).fetchone()
        upper_beam["id"] = beam_id
        upper_beam["hvl_al"] = ref_hvl
        upper_beam["nk_" + chamber_SN] = upper_nk

    if lower_beam == {} or upper_beam == {}:
        raise Exception("Invalid Lookup data from database")

    return lower_beam, upper_beam
