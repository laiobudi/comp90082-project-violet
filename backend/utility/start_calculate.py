import pyodbc
from backend.utility.nk_value import cal_nk_value
from backend.utility.Bw_value import cal_Bw_value
from backend.utility.murho import cal_murho_value
from backend.utility.ccc import cal_ccc_value
from backend.utility.pstem import cal_pstem_value

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
	mu_res = cal_murho_value(beams)

	#### calculate K close
	k_closed_res = cal_ccc_value(bw_res, cones, beams)

	#### calculate Pstem
	beam_cone_list = select_beam_cone_from_db(cursor, audit_id)
	pstem_res = cal_pstem_value(cursor, beams, cones, beam_cone_list)

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
							'k_closed_cone': k_closed_res[beam_cone_id].get("k_closed_cone", 1.0),
							'pstem': next((x["pstem"] for x in pstem_res if x["beam_cone_id"]==beam_cone_id and x["chamber"]==chamber), 1.0),
							'warning': next((x['message'] for x in nk_warn if x["beam_id"]==beam_id), None)
						})

	for res in back_result:

		cursor.execute("INSERT INTO back_result "
					   "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
					   (res["back_result_id"],
						res["input_id"],
						res["chamber_SN"],
						res["nk"],
						res["bw_combined"],
						res["bw_al"],
						res["bw_cu"],
						res["murho"],
						res["k_closed_cone"],
						res["pstem"],
						res["warning"]))
		cursor.commit()

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

# Get the paired beam and cone from db
def select_beam_cone_from_db(cursor, audit_id):
    audit_list = []
    input_audit_table = cursor.execute('SELECT beam_id, '
                                       + 'cone_id FROM audit_beam_inputs '
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
