from backend.utility.interpolation import cal_k_closed_cone

'''
Main function for calculating NK
@:param bw_res: nested dictionary, the output of cal_Bw_value
@:param cones: dictionary of cone information retrieved from db
@:param beams: dictionary of beam data retrieved from db

@:return results: list of dictionaries containing beam_id. cone_id, and k_closed_cone value
'''
def cal_ccc_value(bw_res, cones, beams):

    results = {}
    for cone in cones:
        for beam in beams:
            beam_cone_id = beam["beam_id"] + "_" + cone["cone_id"]
            if cone["open"] == "Open":

                result = {"k_closed_cone": 1.000}
                results[beam_cone_id] = result

            elif cone["open"] == "Closed":
                bw_open = bw_res[beam_cone_id]["Bw_Combined"]
                result = {"k_closed_cone": cal_k_closed_cone(bw_open)}
                results[beam_cone_id] = result
    return results
