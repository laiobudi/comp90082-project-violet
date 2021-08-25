from interpolation import interpolation
# Interpolation/Extrapolation function

#                        c     /    a
#                             /                         a - target_val           c - d
#	    					 /                         ---------------   =   ---------------
# (target_known_val) d	    /    (target_val)               a - b                c - e
#                          /
#                         /
#                 e      /     b

# input data from the `identification` sheet
beams = [
    {"beam_id": "Filter1", "kvp": 60, "hvl_measured_al": 1.268},
    {"beam_id": "Filter2", "kvp": 80, "hvl_measured_al": 2.321},
    {"beam_id": "Filter3", "kvp": 100, "hvl_measured_al": 2.881},
    {"beam_id": "Filter4", "kvp": 120, "hvl_measured_al": 5.123, "hvl_measured_cu": 0.227},
    {"beam_id": "Filter5", "kvp": 150, "hvl_measured_cu": 0.339},
    {"beam_id": "Filter6", "kvp": 180, "hvl_measured_cu": 0.504},
    {"beam_id": "Filter7", "kvp": 200, "hvl_measured_cu": 1.042},
    {"beam_id": "Filter8", "kvp": 250, "hvl_measured_cu": 2.117}
]


###########################
#### Main Calculation #####
###########################
def cal_nk_value(beams: list):

    for beam in beams:
        # step 0.5
        # CHECK if it's Al or Cu or Both
        hvl_type = checkType(beam)

        # step 1
        # SELECT search info from DB (including their data e.g. measured HVL, Nk...)
        # step 2
        # given previous 2 points' nk values (a, b), and hvl values (c, e), and beam["hvl_measured_al(cu)"] (d) -> do interpolation

        # both Al and Cu exist, need to calculate average value
        if hvl_type["Al"] and hvl_type["Cu"]:
            ref_value_al = selectDbFarmer(beam["kvp"], beam["hvl_measured_al"])
            ref_value_cu = selectDbFarmer(beam["kvp"], beam["hvl_measured_cu"])
            # TODO: Average interpolation
        
        # otherwise
        elif hvl_type["Al"]:
            ref_value_al = selectDbFarmer(beam["kvp"], beam["hvl_measured_al"])
            # TODO: Interpolation
        elif hvl_type["Cu"]:
            ref_value_cu = selectDbFarmer(beam["kvp"], beam["hvl_measured_cu"])
            # TODO: Interpolation

        # also need to find Nk for Plane-Parallel-Type
        if hvl_type["Al"] and beam["hvl_measured_al"]<=2.204:
            ref_value_pp = selectDbPP(beam["kvp"], beam["hvl_measured_al"])
            # TODO: Interpolation

        # step 3
        # INSERT ... store the nk value back into the database
        storeIntoDb()
    

###########################
#### Helper functions #####
###########################

# check type of measured_hvl
def checkType(info: dict) -> dict:
    hvl_type = {"Al": False, "Cu": False}
    if info["hvl_measured_al"]: hvl_type["Al"]=True
    if info["hvl_measured_cu"]: hvl_type["Cu"]=True

    return hvl_type

# DB query: Look up farmer type chamber table
def selectDbFarmer(kvp: int, hvl: float)->list:
    # TODO: SELECT ... 

    return ["hvl_1", "hvl_2", "nk_1", "nk_2"]

# DB query: Look up plain parallel type table
def selectDbPP(kvp: int, hvl: float)->list:
    # TODO: SELECT ... 

    return ["hvl_1", "hvl_2", "nk_1", "nk_2"]

# DB query: Store data into Db
def storeIntoDb():
    #TODO: INSERT ...
    
    return 0