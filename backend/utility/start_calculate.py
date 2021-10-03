from backend.utility.nk_value import cal_nk_value, connect_to_db, select_input_from_db
from backend.utility.murho import add_murho
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
	nk_res, nk_warn = cal_nk_value(beams)

	#### calculate BW

	#### calculate Mu
	res = add_murho(beams)
	print(res)
	#### calculate K close

	#### calculate Pstem

	#### Store results into Database
	# input_table = cursor.execute(
	# 	"SELECT input_id, cone_id, beam_id "
	# 	"FROM audit_beam_inputs "
	# 	"WHERE audit_id='{}'".format(audit_id)).fetchall()
	#
	# back_result = []
	#
	# for input_id, cone_id, beam_id in input_table:
	# 	for nk_result in nk_res:
	# 		if beam_id == nk_result['id']:
	# 			if '3587' in nk_result:
	# 				back_result.append(
	# 					convert_result_from_nk(
	# 						input_id,
	# 						nk_result['3587'],
	# 						'3587'))
	# 			if '5447' in nk_result:
	# 				back_result.append(
	# 					convert_result_from_nk(
	# 						input_id,
	# 						nk_result['5447'],
	# 						'5447'))
	# 			if '5448' in nk_result:
	# 				back_result.append(
	# 					convert_result_from_nk(
	# 						input_id,
	# 						nk_result['5448'],
	# 						'5448'))
	# 			if '1508' in nk_result:
	# 				back_result.append(
	# 					convert_result_from_nk(
	# 						input_id,
	# 						nk_result['1508'],
	# 						'1508'))
	# 			if '858' in nk_result:
	# 				back_result.append(
	# 					convert_result_from_nk(
	# 						input_id,
	# 						nk_result['858'],
	# 						'858'))

	# Insert dummy data for bw, murho, kclose, pstem
	# Just for sprint 1 presentation
	# for res in back_result:
	# 	res["bw"] = 1.257
	# 	res["murho"] = 1.018
	# 	res["k_closed_cone"] = 1.0
	# 	res["pstem"] = 1.0

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
	start_calculate("ACDS-kV-5011")
