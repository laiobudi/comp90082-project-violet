#  interpolation(a, b, c, d, e) -> return target
def interpolation(a, b, c, e, d):
    return a - (((c - d) * (a - b)) / (c - e))


# The formula to calculate k_closed_cone factor
def cal_k_closed_cone(bw_open):
    return (1 + (bw_open - 1) * 1.032) / bw_open
