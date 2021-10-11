from backend.utility.interpolation import interpolation

CHAMBER_SN_PP = ["1508", "858"]

def cal_pstem_value(cursor, beams, cones, beam_cone_list):

    # Initialize result dict
    results = []

    # only calculate with Plane Parallel
    for beam in beams:
        hvl_al = beam["hvl_measured_al"]
        beam_id = beam["beam_id"]
        if hvl_al and hvl_al <= 2.204:
            cone_ref_list = check_diameter_from_cone(beam_id, cones, beam_cone_list)
            for cone in cone_ref_list:
                cone_id = cone["cone_id"]
                for chamber in CHAMBER_SN_PP:
                    diameter = cone["diameter"]

                    # TODO: can do extrapolation
                    if diameter > 10: diameter = 10

                    # Extract the reference diameters from table
                    d_ref_1, d_ref_2 = select_from_pstem_d(cursor, chamber, diameter)
                    # Extract the reference pstem from table
                    first, second, third, forth = select_from_pstem(cursor, chamber, hvl_al, d_ref_1, d_ref_2)

                    # Interpolation - three times
                    first_interpo = interpolation(
                        first["pstem"],
                        third["pstem"],
                        first["diameter"],
                        third["diameter"],
                        diameter)
                    second_interpo = interpolation(
                        second["pstem"],
                        forth["pstem"],
                        second["diameter"],
                        forth["diameter"],
                        diameter)
                    final_interpo = interpolation(
                        first_interpo,
                        second_interpo,
                        first["hvl_al"],
                        second["hvl_al"],
                        hvl_al)

                    # TODO: Store the result
                    results.append({
                        "beam_cone_id": beam_id + "_" + cone_id,
                        "chamber": chamber,
                        "pstem": final_interpo
                    })

    return results

def check_diameter_from_cone(beam_id, cones, beam_cone_list):
    temp = []
    for item in beam_cone_list:
        if item["beam_id"] == beam_id:
            temp.append(item["cone_id"])

    res = [x for x in cones if x["cone_id"] in temp]
    return res

def select_from_pstem_d(cursor, chamber, diameter):

    #TODO: date_updated

    (d_ref_1, ) = cursor.execute("SELECT TOP 1 diameter "
                                 "FROM pstem_measured "
                                 "WHERE diameter<={} ".format(diameter) +
                                 "AND beam_pp_chamber_id "
                                 "LIKE '%{}' ".format(chamber) +
                                 "AND pstem_option='measured' "
                                 "ORDER BY diameter DESC").fetchone()
    (d_ref_2, ) = cursor.execute("SELECT TOP 1 diameter "
                                 "FROM pstem_measured "
                                 "WHERE diameter>={} ".format(diameter) +
                                 "AND beam_pp_chamber_id "
                                 "LIKE '%{}' ".format(chamber) +
                                 "AND pstem_option='measured' "
                                 "ORDER BY diameter").fetchone()
    return d_ref_1, d_ref_2

def select_from_pstem(cursor, chamber, hvl_al, d_ref_1, d_ref_2):

    # retrieve the latest lookup table
    (latest_date,) = cursor.execute("SELECT TOP 1 date_updated "
                                    "FROM pstem_measured "
                                    "WHERE pstem_option='measured' "
                                    "ORDER BY date_updated "
                                    "DESC").fetchone()
    latest_date = latest_date.strftime('%Y-%m-%d')

    # TODO: hvl_al<0.2?
    if hvl_al<0.2: hvl_al=0.2

    # Find the hvl boundary for different diameters
    first_lower_table = cursor.execute("SELECT TOP 1 * "
                                     "FROM pstem_measured "
                                     "WHERE "
                                     "hvl_measured_mm_al<={} ".format(hvl_al) +
                                     "AND pstem_option='measured' "
                                     "AND diameter={} ".format(d_ref_1) +
                                     "AND beam_pp_chamber_id "
                                     "LIKE '%{}' ".format(chamber) +
                                     "AND date_updated='{}' ".format(latest_date) +
                                     "ORDER BY hvl_measured_mm_al "
                                     "DESC").fetchone()
    first_lower = {
        "chamber": chamber,
        "diameter": first_lower_table[2],
        "hvl_al": first_lower_table[3],
        "pstem": first_lower_table[4]
    }

    first_upper_table = cursor.execute("SELECT TOP 1 * "
                                     "FROM pstem_measured "
                                     "WHERE "
                                     "hvl_measured_mm_al>={} ".format(hvl_al) +
                                     "AND pstem_option='measured' "
                                     "AND diameter={} ".format(d_ref_1) +
                                     "AND beam_pp_chamber_id "
                                     "LIKE '%{}' ".format(chamber) +
                                     "AND date_updated='{}' ".format(latest_date) +
                                     "ORDER BY hvl_measured_mm_al").fetchone()
    first_upper = {
        "chamber": chamber,
        "diameter": first_upper_table[2],
        "hvl_al": first_upper_table[3],
        "pstem": first_upper_table[4]
    }

    second_lower_table = cursor.execute("SELECT TOP 1 * "
                                     "FROM pstem_measured "
                                     "WHERE "
                                     "hvl_measured_mm_al<={} ".format(hvl_al) +
                                     "AND pstem_option='measured' "
                                     "AND diameter={} ".format(d_ref_2) +
                                     "AND beam_pp_chamber_id "
                                     "LIKE '%{}' ".format(chamber) +
                                     "AND date_updated='{}' ".format(latest_date) +
                                     "ORDER BY hvl_measured_mm_al "
                                     "DESC").fetchone()
    second_lower = {
        "chamber": chamber,
        "diameter": second_lower_table[2],
        "hvl_al": second_lower_table[3],
        "pstem": second_lower_table[4]
    }

    second_upper_table = cursor.execute("SELECT TOP 1 * "
                                     "FROM pstem_measured "
                                     "WHERE "
                                     "hvl_measured_mm_al>={} ".format(hvl_al) +
                                     "AND pstem_option='measured' "
                                     "AND diameter={} ".format(d_ref_2) +
                                     "AND beam_pp_chamber_id "
                                     "LIKE '%{}' ".format(chamber) +
                                     "AND date_updated='{}' ".format(latest_date) +
                                     "ORDER BY hvl_measured_mm_al").fetchone()
    second_upper = {
        "chamber": chamber,
        "diameter": second_upper_table[2],
        "hvl_al": second_upper_table[3],
        "pstem": second_upper_table[4]
    }

    return first_lower, first_upper, second_lower, second_upper
