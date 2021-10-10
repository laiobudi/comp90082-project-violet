from interpolation import interpolation

CHAMBER_LIST = ["1508", "858"]

###########################
#### Main Calculation #####
###########################

def cal_pstem_value(beams: list, cones: list, beam_cones_list: list, pstem_list: list):

    beams_list = []
    for beam_cones in beam_cones_list:
       if beam_cones[0] not in beams_list:
           beams_list.append(beam_cones[0])

    beam_cones_dict = {}
    for beams in beams_list:
        cones_list = []
        for beam_cones in beam_cones_list:
            if beam_cones[0] == beams:
                cones_list.append(beam_cones[1])
        beam_cones_dict[beams] = cones_list

    beam_dict = {}
    for beam in beams:
        beam_id = beam[0]
        m_hvl = beam[2]
        cones_list = beam_cones_dict[beams]

        d_list = []
        for cone_id in cones_list:
            for cone in cones:
                if cone_id == cone[0]:
                    d_list.append(cone[3])

        p_dict = {}
        if m_hvl > 2.2040:
            return 1.000, 1.000, 1.000, 1.000, 1.000, 1.000
        elif m_hvl == 0.2 and m_hvl == 0.8 and m_hvl == 2.2:
            for chamber in CHAMBER_LIST:
                p_temp_list = []
                for d in d_list:
                    d_1, d_2, d1, d2, d3, d4 = locate_d(chamber, m_hvl, d, pstem_list)
                    p = interpolation(d1, d2, d_1, d, d_2)
                    p_temp_list.append(p)
                p_dict[chamber] = p_temp_list
            beam_dict[beam_id] = p_dict
   
        elif m_hvl < 0.8:
            for chamber in CHAMBER_LIST:
                p_temp_list = []
                for d in d_list:
                    d_1, d_2, d1, d2, d3, d4 = locate_d(chamber, m_hvl, d, pstem_list)
                    p1 = interpolation(d1, d2, d_1, d, d_2)
                    p2 = interpolation(d3, d4, d_1, d, d_2)
                    p = interpolation(p1, p2, 0.2, m_hvl, 0.8)
                    p_temp_list.append(p)
                p_dict[chamber] = p_temp_list
            beam_dict[beam_id] = p_dict

        elif m_hvl > 0.8:
            for chamber in CHAMBER_LIST:
                p_temp_list = []
                for d in d_list:
                    d_1, d_2, d1, d2, d3, d4 = locate_d(chamber, m_hvl, d, pstem_list)
                    p1 = interpolation(d1, d2, d_1, d, d_2)
                    p2 = interpolation(d3, d4, d_1, d, d_2)
                    p = interpolation(p1, p2, 0.8, m_hvl, 2.2)
                    p_temp_list.append(p)
                p_dict[chamber] = p_temp_list
            beam_dict[beam_id] = p_dict

    return beam_dict


def locate_d(chamber, m_hvl, d, pstem_list):
    c1_d_14_02 = pstem_list[0]
    c1_d_14_08 = pstem_list[14]
    c1_d_14_22 = pstem_list[28]
    c1_d_28_02 = pstem_list[1]
    c1_d_28_08 = pstem_list[15]
    c1_d_28_22 = pstem_list[29]
    c1_d_42_02 = pstem_list[2]
    c1_d_42_08 = pstem_list[16]
    c1_d_42_22 = pstem_list[30]
    c1_d_50_02 = pstem_list[3]
    c1_d_50_08 = pstem_list[17]
    c1_d_50_22 = pstem_list[31]
    c1_d_75_02 = pstem_list[4]
    c1_d_75_08 = pstem_list[18]
    c1_d_75_22 = pstem_list[32]
    c1_d_84_02 = pstem_list[5]
    c1_d_84_08 = pstem_list[19]
    c1_d_84_22 = pstem_list[33]
    c1_d_100_02 = pstem_list[6]
    c1_d_100_08 = pstem_list[20]
    c1_d_100_22 = pstem_list[34]

    c2_d_14_02 = pstem_list[7]
    c2_d_14_08 = pstem_list[21]
    c2_d_14_22 = pstem_list[35]
    c2_d_28_02 = pstem_list[8]
    c2_d_28_08 = pstem_list[22]
    c2_d_28_22 = pstem_list[36]
    c2_d_42_02 = pstem_list[9]
    c2_d_42_08 = pstem_list[23]
    c2_d_42_22 = pstem_list[37]
    c2_d_50_02 = pstem_list[10]
    c2_d_50_08 = pstem_list[24]
    c2_d_50_22 = pstem_list[38]
    c2_d_75_02 = pstem_list[11]
    c2_d_75_08 = pstem_list[25]
    c2_d_75_22 = pstem_list[39]
    c2_d_84_02 = pstem_list[12]
    c2_d_84_08 = pstem_list[26]
    c2_d_84_22 = pstem_list[40]
    c2_d_100_02 = pstem_list[13]
    c2_d_100_08 = pstem_list[27]
    c2_d_100_22 = pstem_list[41]


    if chamber == 858:
        if m_hvl < 0.8 and m_hvl != 0.2:
            if d < 2.8:
                return 1.4, 2.8, c1_d_14_02['pstem_value'], c1_d_28_02['pstem_value'], c1_d_14_08['pstem_value'], c1_d_28_08['pstem_value']
            elif d >= 2.8 and d < 4.2:
                return 2.8, 4.2, c1_d_28_02['pstem_value'], c1_d_42_02['pstem_value'], c1_d_28_08['pstem_value'], c1_d_42_08['pstem_value']
            elif d >= 4.2 and d < 5.0:
                return 4.2, 5.0, c1_d_42_02['pstem_value'], c1_d_50_02['pstem_value'], c1_d_42_08['pstem_value'], c1_d_50_08['pstem_value']
            elif d >= 5.0 and d < 7.5:
                return 5.0, 7.5, c1_d_50_02['pstem_value'], c1_d_75_02['pstem_value'], c1_d_50_08['pstem_value'], c1_d_75_08['pstem_value']
            elif d >= 7.5 and d < 8.4:
                return 7.5, 8.4, c1_d_75_02['pstem_value'], c1_d_84_02['pstem_value'], c1_d_75_08['pstem_value'], c1_d_84_08['pstem_value']
            elif d >= 8.4:
                return 8.4, 10.0, c1_d_84_02['pstem_value'], c1_d_100_02['pstem_value'], c1_d_84_08['pstem_value'], c1_d_100_08['pstem_value']
        elif m_hvl > 0.8 and m_hvl != 2.2:
            if d < 2.8:
                return 2.8, 4.2, c1_d_14_08['pstem_value'], c1_d_28_08['pstem_value'], c1_d_14_22['pstem_value'], c1_d_28_22['pstem_value']
            elif d >= 2.8 and d < 4.2:
                return 2.8, 4.2, c1_d_28_08['pstem_value'], c1_d_42_08['pstem_value'], c1_d_28_22['pstem_value'], c1_d_42_22['pstem_value']
            elif d >= 4.2 and d < 5.0:
                return 4.2, 5.0, c1_d_42_08['pstem_value'], c1_d_50_08['pstem_value'], c1_d_42_22['pstem_value'], c1_d_50_22['pstem_value']
            elif d >= 5.0 and d < 7.5:
                return 5.0, 7.5, c1_d_50_08['pstem_value'], c1_d_75_08['pstem_value'], c1_d_50_22['pstem_value'], c1_d_75_22['pstem_value']
            elif d >= 7.5 and d < 8.4:
                return 7.5, 8.4, c1_d_75_08['pstem_value'], c1_d_84_08['pstem_value'], c1_d_75_22['pstem_value'], c1_d_84_22['pstem_value']
            elif d >= 8.4:
                return 8.4, 10.0, c1_d_84_08['pstem_value'], c1_d_100_08['pstem_value'], c1_d_84_22['pstem_value'], c1_d_100_22['pstem_value']
        elif m_hvl == 0.2:
            if d < 2.8:
                return 1.4, 2.8, c1_d_14_02['pstem_value'], c1_d_28_02['pstem_value'], 0, 0
            elif d >= 2.8 and d < 4.2:
                return 2.8, 4.2, c1_d_28_02['pstem_value'], c1_d_42_02['pstem_value'], 0, 0
            elif d >= 4.2 and d < 5.0:
                return 4.2, 5.0, c1_d_42_02['pstem_value'], c1_d_50_02['pstem_value'], 0, 0
            elif d >= 5.0 and d < 7.5:
                return 5.0, 7.5, c1_d_50_02['pstem_value'], c1_d_75_02['pstem_value'], 0, 0
            elif d >= 7.5 and d < 8.4:
                return 7.5, 8.4, c1_d_75_02['pstem_value'], c1_d_84_02['pstem_value'], 0, 0
            elif d >= 8.4:
                return 8.4, 10.0, c1_d_84_02['pstem_value'], c1_d_100_02['pstem_value'], 0, 0
        elif m_hvl == 0.8:
            if d < 2.8:
                return 1.4, 2.8, c1_d_14_08['pstem_value'], c1_d_28_08['pstem_value'], 0, 0
            elif d >= 2.8 and d < 4.2:
                return 2.8, 4.2, c1_d_28_08['pstem_value'], c1_d_42_08['pstem_value'], 0, 0
            elif d >= 4.2 and d < 5.0:
                return 4.2, 5.0, c1_d_42_08['pstem_value'], c1_d_50_08['pstem_value'], 0, 0
            elif d >= 5.0 and d < 7.5:
                return 5.0, 7.5, c1_d_50_08['pstem_value'], c1_d_75_08['pstem_value'], 0, 0
            elif d >= 7.5 and d < 8.4:
                return 7.5, 8.4, c1_d_75_08['pstem_value'], c1_d_84_08['pstem_value'], 0, 0
            elif d >= 8.4:
                return 8.4, 10.0, c1_d_84_08['pstem_value'], c1_d_100_08['pstem_value'], 0, 0
        elif m_hvl == 2.2:
            if d < 2.8:
                return 1.4, 2.8, c1_d_14_22['pstem_value'], c1_d_28_22['pstem_value'], 0, 0
            elif d >= 2.8 and d < 4.2:
                return 2.8, 4.2, c1_d_28_22['pstem_value'], c1_d_42_22['pstem_value'], 0, 0
            elif d >= 4.2 and d < 5.0:
                return 4.2, 5.0, c1_d_42_22['pstem_value'], c1_d_50_22['pstem_value'], 0, 0
            elif d >= 5.0 and d < 7.5:
                return 5.0, 7.5, c1_d_50_22['pstem_value'], c1_d_75_22['pstem_value'], 0, 0
            elif d >= 7.5 and d < 8.4:
                return 7.5, 8.4, c1_d_75_22['pstem_value'], c1_d_84_22['pstem_value'], 0, 0
            elif d >= 8.4:
                return 8.4, 10.0, c1_d_84_22['pstem_value'], c1_d_100_22['pstem_value'], 0, 0
    elif chamber == 1508:
        if m_hvl < 0.8 and m_hvl != 0.2:
            if d < 2.8:
                return 1.4, 2.8, c2_d_14_02['pstem_value'], c2_d_28_02['pstem_value'], c2_d_14_08['pstem_value'], c2_d_28_08['pstem_value']
            elif d >= 2.8 and d < 4.2:
                return 2.8, 4.2, c2_d_28_02['pstem_value'], c2_d_42_02['pstem_value'], c2_d_28_08['pstem_value'], c2_d_42_08['pstem_value']
            elif d >= 4.2 and d < 5.0:
                return 4.2, 5.0, c2_d_42_02['pstem_value'], c2_d_50_02['pstem_value'], c2_d_42_08['pstem_value'], c2_d_50_08['pstem_value']
            elif d >= 5.0 and d < 7.5:
                return 5.0, 7.5, c2_d_50_02['pstem_value'], c2_d_75_02['pstem_value'], c2_d_50_08['pstem_value'], c2_d_75_08['pstem_value']
            elif d >= 7.5 and d < 8.4:
                return 7.5, 8.4, c2_d_75_02['pstem_value'], c2_d_84_02['pstem_value'], c2_d_75_08['pstem_value'], c2_d_84_08['pstem_value']
            elif d >= 8.4:
                return 8.4, 10.0, c2_d_84_02['pstem_value'], c2_d_100_02['pstem_value'], c2_d_84_08['pstem_value'], c2_d_100_08['pstem_value']
        elif m_hvl > 0.8 and m_hvl != 2.2:
            if d < 2.8:
                return 2.8, 4.2, c2_d_14_08['pstem_value'], c2_d_28_08['pstem_value'], c2_d_14_22['pstem_value'], c2_d_28_22['pstem_value']
            elif d >= 2.8 and d < 4.2:
                return 2.8, 4.2, c2_d_28_08['pstem_value'], c2_d_42_08['pstem_value'], c2_d_28_22['pstem_value'], c2_d_42_22['pstem_value']
            elif d >= 4.2 and d < 5.0:
                return 4.2, 5.0, c2_d_42_08['pstem_value'], c2_d_50_08['pstem_value'], c2_d_42_22['pstem_value'], c2_d_50_22['pstem_value']
            elif d >= 5.0 and d < 7.5:
                return 5.0, 7.5, c2_d_50_08['pstem_value'], c2_d_75_08['pstem_value'], c2_d_50_22['pstem_value'], c2_d_75_22['pstem_value']
            elif d >= 7.5 and d < 8.4:
                return 7.5, 8.4, c2_d_75_08['pstem_value'], c2_d_84_08['pstem_value'], c2_d_75_22['pstem_value'], c2_d_84_22['pstem_value']
            elif d >= 8.4:
                return 8.4, 10.0, c2_d_84_08['pstem_value'], c2_d_100_08['pstem_value'], c2_d_84_22['pstem_value'], c2_d_100_22['pstem_value']
        elif m_hvl == 0.2:
            if d < 2.8:
                return 1.4, 2.8, c2_d_14_02['pstem_value'], c2_d_28_02['pstem_value'], 0, 0
            elif d >= 2.8 and d < 4.2:
                return 2.8, 4.2, c2_d_28_02['pstem_value'], c2_d_42_02['pstem_value'], 0, 0
            elif d >= 4.2 and d < 5.0:
                return 4.2, 5.0, c2_d_42_02['pstem_value'], c2_d_50_02['pstem_value'], 0, 0
            elif d >= 5.0 and d < 7.5:
                return 5.0, 7.5, c2_d_50_02['pstem_value'], c2_d_75_02['pstem_value'], 0, 0
            elif d >= 7.5 and d < 8.4:
                return 7.5, 8.4, c2_d_75_02['pstem_value'], c2_d_84_02['pstem_value'], 0, 0
            elif d >= 8.4:
                return 8.4, 10.0, c2_d_84_02['pstem_value'], c2_d_100_02['pstem_value'], 0, 0
        elif m_hvl == 0.8:
            if d < 2.8:
                return 1.4, 2.8, c2_d_14_08['pstem_value'], c2_d_28_08['pstem_value'], 0, 0
            elif d >= 2.8 and d < 4.2:
                return 2.8, 4.2, c2_d_28_08['pstem_value'], c2_d_42_08['pstem_value'], 0, 0
            elif d >= 4.2 and d < 5.0:
                return 4.2, 5.0, c2_d_42_08['pstem_value'], c2_d_50_08['pstem_value'], 0, 0
            elif d >= 5.0 and d < 7.5:
                return 5.0, 7.5, c2_d_50_08['pstem_value'], c2_d_75_08['pstem_value'], 0, 0
            elif d >= 7.5 and d < 8.4:
                return 7.5, 8.4, c2_d_75_08['pstem_value'], c2_d_84_08['pstem_value'], 0, 0
            elif d >= 8.4:
                return 8.4, 10.0, c2_d_84_08['pstem_value'], c2_d_100_08['pstem_value'], 0, 0
        elif m_hvl == 2.2:
            if d < 2.8:
                return 1.4, 2.8, c2_d_14_22['pstem_value'], c2_d_28_22['pstem_value'], 0, 0
            elif d >= 2.8 and d < 4.2:
                return 2.8, 4.2, c2_d_28_22['pstem_value'], c2_d_42_22['pstem_value'], 0, 0
            elif d >= 4.2 and d < 5.0:
                return 4.2, 5.0, c2_d_42_22['pstem_value'], c2_d_50_22['pstem_value'], 0, 0
            elif d >= 5.0 and d < 7.5:
                return 5.0, 7.5, c2_d_50_22['pstem_value'], c2_d_75_22['pstem_value'], 0, 0
            elif d >= 7.5 and d < 8.4:
                return 7.5, 8.4, c2_d_75_22['pstem_value'], c2_d_84_22['pstem_value'], 0, 0
            elif d >= 8.4:
                return 8.4, 10.0, c2_d_84_22['pstem_value'], c2_d_100_22['pstem_value'], 0, 0

