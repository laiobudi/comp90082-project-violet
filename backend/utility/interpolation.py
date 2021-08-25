# Interpolation/Extrapolation function

#                        c     /    a
#                             /                         a - target_val           c - d
#	    					 /                         ---------------   =   ---------------
# (target_known_val) d	    /    (target_val)               a - b                c - e
#                          /
#                         /
#                 e      /     b


####  interpolation(a, b, c, d, e) -> return target
def interpolation(a, b, c, e, d):
	return a - (((c - d) * (a - b)) / (c - e))


#### The formula to calculate k_closed_cone factor
def cal_k_closed_cone(bw_open):
	return (1 + (bw_open - 1) * 1.032) / bw_open


# def extrapolation(x_nk, y_nk, x_hvl, y_hvl, target_hvl):
# 	numerator = (x_hvl-y_hvl)*x_nk+(x_nk-y_nk)*(x_hvl-target_hvl)
# 	denominator = (x_hvl-y_hvl)
# 	return numerator/denominator


if __name__ == '__main__':
	print("Filter1 kvp=60 chamber3587 -> nk : {}"
		  .format(interpolation(49.8986656857429, 48.3988130247751, 0.788813791651093, 1.28860110150315, 1.268)))
	print("----------------------------------------------------")
	print("Filter4 kvp=120 chamber5447 -> nk : {}"
		  .format(interpolation(47.8597516857949, 47.8406595597577, 5.55599697591481, 6.37697784783916, 5.123)))
	print("----------------------------------------------------")
	print("Filter2 kvp=80 hvl=2.321 ssd=50 d=11.2837917")
	print("Diameter not found in the table, do first interpolation. 10<d<15 & 2<hvl<3 , BW(Al) : {}"
		  .format(interpolation(1.244, 1.265, 10, 15, 11.2837917)))
	print("This bw is for ssd=50 d=11.2837917 hvl=2")

	print("Diameter not found in the table, do first interpolation. 10<d<15 & 2<hvl<3 , BW(Al) : {}"
		  .format(interpolation(1.309, 1.346, 10, 15, 11.2837917)))
	print("This bw is for ssd=50 d=11.2837917 hvl=3")
	print("Now, we can calculate BW of Filter2 kvp=80 hvl=2.321 ssd=50 d=11.2837917")
	print(interpolation(1.24939192514, 1.31850005858, 2, 3, 2.321))
	print("----------------------------------------------------")
	print("Filter1 kvp=60 hvl=1.268 mu/rho : {}".format(interpolation(1.018, 1.017, 1.2, 1.5, 1.268)))
	print("----------------------------------------------------")
	print("Calculate closed cone factor for Filter7 kvp=200 bw_open=1.3620135907714")
	print("k_closed_cone factor : {}".format(cal_k_closed_cone(1.3620135907714)))
	print("----------------------------------------------------")
