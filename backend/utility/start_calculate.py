import pyodbc
from backend.utility.nk_value import cal_nk_value
from backend.utility.Bw_value import cal_Bw_value
from backend.utility.murho import add_murho
from backend.utility.ccc import cal_ccc_value
import pstem

CHAMBER_SN_FARMER = ["3587", "5447", "5448"]
CHAMBER_SN_PP = ["1508", "858"]
'''
Start backend calculation
@:param audit_id: string, audit id
'''

def start_calculate(audit_id):
	#### Connect to db
	cursor = connect_to_db()

	#### Select input data from db
	beams, cones = select_input_from_db(cursor, audit_id)

	#### calculate NK
	nk_res, nk_warn = cal_nk_value(cursor, beams)

	#### calculate BW
	bw_res = cal_Bw_value(cursor, beams, cones)

	#### calculate Mu
	mu_res = add_murho(beams)

	#### calculate K close
	k_closed_res = cal_ccc_value(bw_res, cones, beams)
	# for r in k_closed_res:
	# 	print(r)
	# print(k_closed_res)
	#### calculate Pstem
    pstem_list = select_pstem_input_from_db(cursor)
    beam_cones_list = select_audit_input_from_db(cursor, audit_id)

    pstem.cal_pstem_value(beams, cones, beam_cones_list, pstem_list)

	#### Store results into Database
	input_table = cursor.execute(
		"SELECT input_id, cone_id, beam_id "
		"FROM audit_beam_inputs "
		"WHERE audit_id='{}'".format(audit_id)).fetchall()

	back_result = []

	for input_id, cone_id, beam_id in input_table:
		beam_cone_id = beam_id + "_" + cone_id
		for nk_result in nk_res:
			if beam_id == nk_result['id']:
				for chamber in CHAMBER_SN_FARMER+CHAMBER_SN_PP:
					if chamber in nk_result:
						back_result.append({
							'back_result_id': input_id + '-' + chamber,
							'input_id': input_id,
							'chamber_SN': chamber,
							'nk': nk_result[chamber],
							'bw_combined': bw_res[beam_cone_id]["Bw_Combined"],
							'bw_al': bw_res[beam_cone_id].get("Bw_Al", None),
							'bw_cu': bw_res[beam_cone_id].get("Bw_Cu", None),
							# TODO: default value for murho could be revised to NONE?
							'murho': next((x["murho"] for x in mu_res if x["beam_id"]==beam_id), 1.0),
							'k_closed_cone': k_closed_res[beam_cone_id].get("k_closed_cone", 1.0)
						})
	# DEBUG
	# for b in back_result:
	# 	print(b)

		# store ccc results
		# for res in k_closed_res:
		# 	if beam_id == res["beam_id"] and cone_id == res["cone_id"]:
		# 		back_result["k_closed_cone"] = res["k_closed_cone"]
	# 看看这么写。
	# for input_id, beam_id, cone_id in input_table:
	# 	beam_cone_id = beam_id + "_" + cone_id 
		
	# 	for chamber_SN in CHAMBER_SN_FARMER+CHAMBER_SN_PP:
	# 		res = {
	# 			"back_result_id" : input_id + '-' + chamber_SN, 
	# 			"input_id" : input_id, 
	# 			"chamber_SN" : chamber_SN, 
	# 			"nk" : , 
	# 			"Bw_Al" : bw_res[beam_cone_id]["Bw_Al"], 
	# 			"Bw_Cu" : bw_res[beam_cone_id]["Bw_Cu"], 
	# 			"Bw_Combined" : bw_res[beam_cone_id]["Bw_Combined"], 
	# 			...? 
	# 		}
	# 		back_result.append(res)

	# Insert dummy data for bw, murho, kclose, pstem
	# Just for sprint 1 presentation
	for res in back_result:
		# res["bw"] = 1.257
		# res["murho"] = 1.018
		# res["k_closed_cone"] = 1.0
		res["pstem"] = 1.0

		# cursor.execute("INSERT INTO back_result "
		# 			   "VALUES ('{}', '{}', '{}', '{}', "
		# 			   "'{}', '{}', '{}', '{}')"
		# 			   .format(res['back_result_id'],
		# 					   res['input_id'],
		# 					   res['chamber_SN'],
		# 					   res['nk'],
		# 					   res['bw'],
		# 					   res['murho'],
		# 					   res['k_closed_cone'],
		# 					   res['pstem']))
		# cursor.commit()

		# DEBUG
		# print(res)


"""
###########################
#### Helper functions #####
###########################
"""

'''
connect to the database
@:return cursor object
'''
def connect_to_db():
	try:
		connection = pyodbc.connect(
			"Driver={ODBC Driver 17 for SQL Server};"
			"Server=13.70.131.250,1433;"
			"Database=violet_dev;"
			"Uid=SA;"
			"PWD=ProjViolet_1;"
			"Trusted_Connection=no;"
		)
		# Create cursor object
		return connection.cursor()

	except pyodbc.Error as ex:
		raise Exception(ex.args[1])


'''
select the data from db based on the audit_id
@:param cursor: Object, a cursor object
@:param audit_id: string, the audit_id that you want to search
@:return beams: list, the data of beams
'''
def select_input_from_db(cursor, audit_id):
	beams, cones = [], []
	input_beams_table = cursor.execute('SELECT beam_id, '
								+ 'nom_energy, '
								+ 'hvl_measured_mm_al, '
								+ 'hvl_measured_mm_cu '
								+ "FROM beam_data "
								+ "WHERE beam_id "
								+ "LIKE '{}%'".format(audit_id)
									   ).fetchall()
	for key, value in enumerate(input_beams_table):
		beam = {"beam_id": (value)[0],
				"kvp": (value)[1],
				"hvl_measured_al": (value)[2],
				"hvl_measured_cu": (value)[3]}
		beams.append(beam)

	input_cones_table = cursor.execute('SELECT cone_id, ssd, open_closed, '
									   + "CASE WHEN shape = 'circular' "
										 "THEN field_diameter "
									   + "	WHEN shape = 'square' "
										 "THEN 2*SQRT(field_area/PI()) "
									   + "	WHEN shape = 'rectangular' "
										 "THEN 2*SQRT(field_dimension_1*"
										 "field_dimension_2/PI()) "
									   + "END AS diameter "
									   + "FROM cone "
									   + "WHERE cone_id "
									   + "LIKE '{}%'".format(audit_id)
									   ).fetchall()
	for key, value in enumerate(input_cones_table):
		cone = {"cone_id": (value)[0],
				"SSD": (value)[1],
				"open": (value)[2],
				"diameter": (value)[3]}
		cones.append(cone)
	# DEBUG
	# print(beams)
	return beams, cones

def select_pstem_input_from_db(cursor):
    pstem_list = []
    input_pstem_table = cursor.execute('select diameter, '
                                       + 'hvl_measured_mm_al, '
                                       + 'pstem_value '
                                       + "from pstem_measured "
                                       + "where pstem_option = 'measured' "
                                       ).fetchall()
    for key, value in enumerate(input_pstem_table):
            pstem = {"diameter": (value)[0],
                "hvl_measured_mm_al": (value)[1],
                "pstem_value": (value)[2]}
            pstem_list.append(pstem)

    # DEBUG
    # print(pstem_list[24]['pstem_value'])
    return pstem_list

def select_audit_input_from_db(cursor, audit_id):
    audit_list = []
    input_audit_table = cursor.execute('SELECT beam_id, '
                                       + 'cone_id, '
                                       + "WHERE audit_id "
                                       + "LIKE '{}%'".format(audit_id)
                                       ).fetchall()
    for key, value in enumerate(input_audit_table):
        audit = {"beam_id": (value)[0],
                "cone_id": (value)[1]}
        audit_list.append(audit)

    return audit_list


# convert to result format
def convert_result_from_nk(input_id, nk, chamber_SN):
	return {
		'back_result_id': input_id + '-' + chamber_SN,
		'input_id': input_id,
		'chamber_SN': chamber_SN,
		'nk': nk
	}


# DEBUG
if __name__ == "__main__":
	start_calculate("ACDS-kV-5014")
