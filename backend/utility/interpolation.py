# Interpolation(a, b, c, d, e) -> return target
# @params: a,b is the lookup target value (e.g. nk bw mu..)
# @params: c,e is the lookup reference value (e.g. hvl, d..)
# @params: d is input_beam's input (e.g. hvl_measured, d..)
def interpolation(a, b, c, e, d):
	if a == b: return a
	return a - (((c - d) * (a - b)) / (c - e))


# The formula to calculate k_closed_cone factor
def cal_k_closed_cone(bw_open):
	return (1 + (bw_open - 1) * 1.032) / bw_open
