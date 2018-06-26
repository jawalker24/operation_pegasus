from Pegasus import PegasusExp

expInfo = [988, "New", "Study"]
#expInfo = [988, "Returning", "Study"]


exp = PegasusExp(expInfo,'pics/','data/')
"""
print('Test initialization:\n')
print('Pic Dir: ' + exp.pic_dir)
print('Data Dir: ' + exp.data_dir)
print('Sub Name: ' + str(exp.sub_name))
print('Participant Type: ' + exp.participant_type)
print('Experitment Type: ' + exp.exp_type)
print('Num Cond: ' + str(exp.num_cond))
"""
print('\nFunction checks:\n')
#print('gen_pic_list():')
#print(exp.gen_pic_list())
#print('gen_cb_list():')
#exp.get_cb_list()
#exp.get_study_list()
exp.run_study()

