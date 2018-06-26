"""
* Pegasus Experiment
*
* Hard to even explain the experiment at this point in time.  Really in early alpha
*
* @author John Walker
* @version 0.0.2, 03.08.18 (see below for version control)
"""

import ast, copy, csv, math, random, sys
import os.path
from operator import itemgetter

from pygame import *
from pylink import *
from psychopy import core,event,gui,visual


class PegasusExp(object):
    def __init__(self, exp_info, pic_dir, data_dir):
        self.pic_dir = pic_dir
        self.data_dir = data_dir
        
        self.win = visual.Window([1920,1080], fullscr=True, units="pix")
        self.clock = core.Clock()
        
        self.sub_name = exp_info[0]
        self.participant_type = exp_info[1]
        self.exp_type = exp_info[-1]
        self.block_list = []
        
        self.study_dur = 3
        self.stu_fix_dur = 1
        self.test_dur = 5
        self.test_fix_dur = 1
        self.distract_dur = 60
        
        self.num_stu_cond = 2
        self.num_test_cond = 6
        self.num_cond = self.num_stu_cond * self.num_test_cond
        self.num_block = 1
        self.num_per_block = 12 # number of sextet in restudy block; must be divisible by numCond
        self.num_study_per_block = self.num_per_block * 3
        self.current_block = 0
        
        self.pic_size = 100
        self.cb_list = [[[]]]
        self.get_cb_list()
        self.get_jitter()
        #self.item_disp_rec = visual.Rect(self.win,
        #                               height=900, width=1600, pos=(0, 50),
        #                               fillColor='#DAE3F3')
    
    def run_experiment(self):
        pass
    
    def get_cb_list(self):
        self.cb_file_name = self.data_dir + str(self.sub_name) + "OPcblist.txt"
        cb_file_exist = os.path.isfile(self.cb_file_name)
        
        if not cb_file_exist and self.participant_type == "New": #Create new CB list for new participant
            print("I will now gen the CB List")
            self.gen_cb_list()
                
        elif cb_file_exist and self.participant_type == "Returning":
            print("I will now load the CB List")
            self.load_cb_list()
        
        else:
            print("Error because cbFileExist is %s and participant type is %s" % (str(cb_file_exist), self.participant_type)) 
    
    def get_jitter(self):#Eventually this will get the jitters from a file
        self.study_jitter = [0] * self.num_study_per_block
        self.rs_jitter = [0] * self.num_per_block
        self.test_jitter = [0] * self.num_per_block
    
    def gen_cb_list(self):
        pic_list = self.gen_pic_list()
        cb_full_list = []
        #Create the sextets
        for block in range(self.num_block):
            sextet_temp= []
            for item in range(self.num_per_block):
                sextet_temp.append([block,[-1, -1, -1], -1, PictureSextet(pic_list[item + block * self.num_per_block][0:3], 
                                                            pic_list[item + block * self.num_per_block][3:6],
                                                            item % self.num_cond , self.pic_size)])
            cb_full_list.append(sextet_temp)
        
        #assign study and test order
        for block in range(self.num_block):
            sextant_stu_master = []
            sextant_stu_temp = []
            
            for i in range(self.num_per_block):
                for j in range(3):
                    sextant_stu_temp.append([i, j])
                sextant_stu_master.append(sextant_stu_temp)
                sextant_stu_temp = []
            
            random.shuffle(sextant_stu_master)
            print(sextant_stu_master)
            
            poss_delays = range(4,9)
            
            invalid_list = True
            max_iter = 1000
            i = 0
            
            while invalid_list and i < max_iter:
                sextant_stu = copy.deepcopy(sextant_stu_master)
                #print(len(sextant_stu_master))
                #print(len(sextant_stu_master[0]))
                s_order = [0] * (len(sextant_stu_master)*len(sextant_stu_master[0]))
                for index, item in enumerate(s_order):
                    if item == 0:
                        sextant_stu_sub = sextant_stu.pop(0)
                        s_order[index] = sextant_stu_sub.pop(0)
                        
                        jumps = poss_delays[:]
                        random.shuffle(jumps)
                        valid_jump = False
                        for jump in jumps:
                            if (index + jump) < len(s_order) and s_order[index + jump] == 0:
                                s_order[index + jump] = sextant_stu_sub.pop(0)
                                first_jump = jump
                                valid_jump = True
                                break
                        
                        if not valid_jump:
                            #print(s_order)
                            break
                            #raise Warning('cannot create valid list at item' + strings.pop())
                            
                        jumps = poss_delays[:]
                        random.shuffle(jumps)
                        valid_jump = False
                        for jump in jumps:
                            if (index + jump+ first_jump) < len(s_order) and s_order[index + jump + first_jump] == 0:
                                s_order[index + jump + first_jump] = sextant_stu_sub.pop(0)
                                valid_jump = True
                                break
                        
                        if not valid_jump:
                            #print(s_order)
                            break
                            #raise Warning('cannot create valid list at item' + strings.pop())
                    if index+ 1 == len(s_order):
                        invalid_list = False
                            
                i += 1
            
            if invalid_list:
                raise RuntimeError('Could not create valid study list')
                           
            #print(s_order)
            #print("Num iterations: ", i)
            
            for index, stu_combo in enumerate(s_order):
                cb_full_list[block][stu_combo[0]][1][stu_combo[1]] = index
            
            #print(cb_full_list)
            
            #print('num_per_block: ' + str(self.num_per_block))
            t_order = range(self.num_per_block/2)
            random.shuffle(t_order)
            print(t_order)
            sextants_left = range(self.num_per_block)
            
            for position in t_order:
                sextant_condition = cb_full_list[block][sextants_left[0]][3].ovr_cond
                
                if sextant_condition in [0, 2, 6, 8]:
                    if cb_full_list[block][sextants_left[1]][3].ovr_cond == (sextant_condition + 1):
                        cb_full_list[block][sextants_left[0]][2] = position
                        cb_full_list[block][sextants_left[1]][2] = position
                        PictureSextet.make_compatible(cb_full_list[block][sextants_left[0]][3],
                                                        cb_full_list[block][sextants_left[1]][3])
                        del(sextants_left[0:2])
                    
                    else:
                        raise RuntimeError('cb_list out of order')
                
                elif sextant_condition in [4, 5]:
                    
                    for index, item in enumerate(sextants_left):
                        if cb_full_list[block][item][3].ovr_cond == sextant_condition + 6:
                            paired_item = item
                            paired_index = index
                            break
                            
                    else:
                        raise RuntimeError('Cannot find corresponding item in cb list')
                        
                    cb_full_list[block][sextants_left[0]][2] = position
                    cb_full_list[block][paired_item][2] = position
                    PictureSextet.make_compatible(cb_full_list[block][sextants_left[0]][3],
                                                    cb_full_list[block][paired_item][3])
                    
                    del(sextants_left[paired_index])
                    del(sextants_left[0])
                
                else:
                    raise RuntimeError('cb_list out of order!')
                
            print('CB full list:')
            print(cb_full_list)
            self.cb_list = cb_full_list
        
        self.save_cb_list()
        
    
    def save_cb_list(self):
        with open(self.cb_file_name, 'wb') as cb_out_file:
            cb_out = csv.writer(cb_out_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for block in self.cb_list:
                for sextet_info in block:
                    cb_out.writerow(sextet_info[:-1] + [sextet_info[-1].trip1_names, sextet_info[-1].trip2_names, sextet_info[-1].ovr_cond,
                                                        sextet_info[-1].trip1_locs, sextet_info[-1].trip2_locs])
        print("CB List Saved")
    
    def load_cb_list(self):
        cb_temp=[]
        with open(self.cb_file_name, 'rb') as cb_in_file:
            cb_in = csv.reader(cb_in_file, delimiter=',', quotechar='|')
            block = 0
            trial_list = []
            
            for r, row in enumerate(cb_in):#Sextet info starts at 5
                if int(row[0]) != block:
                    cb_temp.append(trial_list)
                    trial_list = []
                    block += 1
                sextet_temp = PictureSextet(ast.literal_eval(row[3]), ast.literal_eval(row[4]), 
                                            int(row[5]), self.pic_size)
                
                trip1_locs_temp = ast.literal_eval(row[6])
                trip2_locs_temp = ast.literal_eval(row[7])
                sextet_temp.override_locs(trip1_locs_temp, trip2_locs_temp)
                sextet_info = [int(row[0]), ast.literal_eval(row[1]), int(row[2]), sextet_temp]
                trial_list.append(sextet_info)
            cb_temp.append(trial_list) # append final block
        
        print(cb_temp)
        self.cb_list = cb_temp
        print("CB List Loaded")
    
    def gen_pic_list(self):
        pic_list = []
        num_pics_per_sextet = 6
        pic_nums = range(1, self.num_block * self.num_per_block * num_pics_per_sextet + 1) #pictures start at "bo1.jpg"
        random.shuffle(pic_nums)
        
        for i in range(self.num_block * self.num_per_block):
            temp_pics = []
            for j in range(num_pics_per_sextet):
                pic_num = (num_pics_per_sextet * i) + j 
                temp_pics.append("bo%d.jpg" % pic_nums[pic_num])
            
            
            pic_list.append(temp_pics)
        
        self.check_pic_exist(pic_list)
        return pic_list
    
    def check_pic_exist(self, pic_list):
        for pics in pic_list:
            for pic in pics:
                if not os.path.isfile(self.pic_dir + pic):
                    print("Error: Cannot find %s" % pic)
                    sys.exit()
        print("All pictures present and accounted for")
    
    def get_study_list(self):
        study_list = [0] * self.num_per_block * 3
        sextet_list = self.cb_list[self.current_block][:]
        print(sextet_list)
        for item in sextet_list:
            for index in range(3):
                study_list[item[1][index]] = [index, item[-1]]
        
        print('Study list')
        print(study_list)
        return study_list
    
    
    def get_test_list(self):
        pass #copy getRepresList
    
    def run_study(self):
        random.shuffle(self.study_jitter)
        study_trials= self.get_study_list()
        for t, trial in enumerate(study_trials):
            self.disp_fix(self.stu_fix_dur + self.study_jitter[t])
            self.generate_stu_pic_display(trial)
            core.wait(self.study_dur)
    
    def run_distractor(self):
        pass
    
    def run_test(self, trial_list):
        pass
    
    def disp_fix(self, duration):
        #self.item_disp_rec.draw()
        fix = visual.TextStim(self.win, '+', pos=(0, 0), height=120)
        fix.draw()
        self.win.flip()
        core.wait(duration)
    
    def generate_stu_pic_display(self, pic_info):
        #self.item_disp_rec.draw()
        condition = pic_info[-1].ovr_cond // 6
        
        if condition == 0: #old/old
            if pic_info[0] == 0:
                locs = pic_info[-1].get_locs(1)
                pic_names = pic_info[-1].get_pic_names(1)
            
            elif pic_info[0] == 1:
                locs = pic_info[-1].get_locs(2)
                pic_names = pic_info[-1].get_pic_names(2)
                
            elif pic_info[0] == 2:
                locs = pic_info[-1].get_locs(1) + pic_info[-1].get_locs(2)
                pic_names = pic_info[-1].get_pic_names(1) + pic_info[-1].get_pic_names(2)
                
            else:
                raise RuntimeError('Error generating study display')
                
        elif condition == 1: #old/new
            if pic_info[0] == 0:
                locs = pic_info[-1].get_locs(1)
                pic_names = pic_info[-1].get_pic_names(1)
            
            elif pic_info[0] == 1:
                locs = pic_info[-1].get_locs(1) + pic_info[-1].get_locs(2)
                pic_names = pic_info[-1].get_pic_names(1) + pic_info[-1].get_pic_names(2)
            
            elif pic_info[0] == 2:
                locs = pic_info[-1].get_locs(2)
                pic_names = pic_info[-1].get_pic_names(2)
            
            else:
                raise RuntimeError('Error generating study display')
        
        for index, loc in enumerate(locs):
            pic_file = self.pic_dir + pic_names[index]
            picX = loc[0]
            picY = loc[1]
            temp_pic = visual.ImageStim(self.win, image=pic_file, pos=(picX, picY), size=(self.pic_size,self.pic_size))
            temp_pic.draw()
        self.win.flip()
    
    def generate_test_display(self):
        test_disp_ins = visual.TextStim(self.win, 
                text="Were the items in the same configuration as before?",
                pos=(0, 200),
                color='black',
                height=65,
                wrapWidth=1440
                )
        test_disp_new = visual.TextStim(self.win, text="New", pos=(-720, -100), color='black', height=60)
        test_disp_old = visual.TextStim(self.win, text="Old", pos=(720, -100), color='black', height=60)
        test_disp_one = visual.TextStim(self.win, text="1", pos=(-720, -200), color='black', height=60)
        test_disp_two = visual.TextStim(self.win, text="2", pos=(-240, -200), color='black', height=60)
        test_disp_three = visual.TextStim(self.win, text="3", pos=(240, -200), color='black', height=60)
        test_disp_four = visual.TextStim(self.win, text="4", pos=(720, -200), color='black', height=60)
        test_disp_ins.draw()
        test_disp_new.draw()
        test_disp_old.draw()
        test_disp_one.draw()
        test_disp_two.draw()
        test_disp_three.draw()
        test_disp_four.draw()
        self.win.flip()
        
        valid_resp = ['num_1', 'num_2', 'num_3', 'num_4']
        event.clearEvents()
        keys_pressed = event.waitKeys(maxWait=30, keyList=validResp, timeStamped=self.clock)
        print(keys_pressed)
    
    def clean_up(self):
        self.win.close()
        core.quit()


class PictureSextet(object):
    def __init__(self, trip1, trip2, condition, size):
        """ Initializes sextet
        pic1 should be tuple of picture names for first triplet
        pic2 should be tuple of picture names for second triplet
        condition should be the overall condition number
        size should be in pixels.  Currently everything is square so only one int should be passed in"""
        self.trip1_names = trip1
        self.trip2_names = trip2
        self.ovr_cond = condition
        self.pic_size = size
        
        """min_dist is set so that there is a minimum full picture square between any two pictures
        even on the diagonal"""
        self.min_dist = (self.pic_size * 2 **.5) * 2 
        
        self.gen_stu_tst_conds()
        [self.trip1_study_first, self.trip2_study_first] = self.gen_study_pres()
        
        temp_locs = self.gen_pic_locs(6, [])
        self.trip1_locs = temp_locs[:3]
        self.trip2_locs = temp_locs[3:]
    
    def __repr__(self):
        sextet_string = "["
        
        for name in self.trip1_names:
            sextet_string += name + " "
        
        sextet_string += "]_["
        
        for name in self.trip2_names:
            sextet_string += name + " "
        
        sextet_string += "]_" + str(self.ovr_cond)
        return sextet_string
    
    def get_locs(self, triplet_num):
        if triplet_num == 1:
            return self.trip1_locs
        elif triplet_num == 2:
            return self.trip2_locs
        else:
            print("Cannot give study locations for invalid picNum")
            return [[-1, -1], [-1, -1], [-1, -1]]
    
    def get_pic_names(self, triplet_num):
        if triplet_num == 1:
            return self.trip1_names
        elif triplet_num == 2:
            return self.trip2_names
        else:
            print("Cannot give picture names for invalid triple number")
            return ['NA', 'NA', 'NA']
    
    def override_locs(self, t1_locs, t2_locs):
        self.trip1_locs = t1_locs #may want to implement a check for these
        self.trip2_locs = t2_locs
    
    def gen_coordinate(self, boundaries):
        return random.randint(boundaries[0] + int(round(self.pic_size / 2)), boundaries[1] - int(round(self.pic_size / 2)))

    def gen_pic_locs(self, num_locs, locs2avoid=[]):
        num_orig_locs = len(locs2avoid)
        locs = locs2avoid[:]
        
        for i in range(num_locs):
            invalid_loc = True
            j = 0
            max_iter = 1000
            while j < max_iter and invalid_loc:
                temp_x = self.gen_coordinate([-860, 860])
                temp_y = self.gen_coordinate([-440, 440])
                invalid_loc = False
                for loc in locs:
                    if ((temp_x - loc[0]) ** 2 + (temp_y - loc[1]) ** 2) ** .5 < self.min_dist:
                        invalid_loc = True
                        break
                j += 1
                if j == max_iter:
                    raise RuntimeError('Cannot find an acceptable solution for locations')
            locs.append([temp_x, temp_y])
        
        if not self.check_dist(locs):
            print("Error generating locations")
            sys.exit()
        
        return locs[num_orig_locs:]
    
    def gen_stu_tst_conds(self):
        """Generates study and test conditions for sextet"""
        num_tst_conds = 6 # needs to be changed if exp changes along with gen_tst_cond
        
        self.stu_cond = self.ovr_cond // num_tst_conds
        
        test_cond_temp = self.ovr_cond % num_tst_conds
        
        if test_cond_temp in [0, 1, 4]:
            self.test_cond = 0 # 0 is match and 1 is mismatch
        elif test_cond_temp in [2, 3, 5]:
            self.test_cond = 1
        else:
            print("Error: problem in creating tst and stu conds")
    
    
    def gen_stu_pic_conds(self):
        return {
            0: [0,0], # old/old
            1: [0,1], # old/new
            }.get(self.stu_cond, [9, 9])
    
    def gen_study_pres(self):
        return {
            0: [True, True],
            1: [True, False],
            }.get(self.stu_cond, [False, False])
    
    def check_dist(self, locs):
        """Checks to make sure none of the locations overlap.  Returns True if no overlaps.
        Needs at least 2 locations to work"""
        for i in range(len(locs)-1):
            for j in range(i+1,len(locs)):
                if ((locs[i][0] - locs[j][0]) ** 2 + (locs[i][1] - locs[j][1]) ** 2) ** .5 < self.min_dist:
                    return False
        
        return True
    
    def make_compatible(picSextet1, picSextet2):
        locs11 = picSextet1.get_locs(1)
        locs12 = picSextet1.get_locs(2)
        locs21 = picSextet2.get_locs(1)
        locs22 = picSextet2.get_locs(2)
        
        no_overlap = picSextet1.check_dist(locs11 + locs12 + locs21 + locs22)
       
        
        if not no_overlap:
            try:
                new_locs = picSextet2.gen_pic_locs(6, locs11 + locs12)
                picSextet2.override_locs(new_locs[0:3], new_locs[3:6])
            
            except:
                new_locs = picSextet2.gen_pic_locs(12)
                picSextet1.override_locs(new_locs[0:3], new_locs[3:6])
                picSextet2.override_locs(new_locs[6:9], new_locs[9:12])





# Actual Experiment

#Retrieve Participant Details

piDlg = gui.Dlg(title="Participant Information Entry")
piDlg.addField('Participant number:')
piDlg.addField('Participant Type', choices=["New", "Returning"])
piDlg.addField('Experiment Type', choices=["Study", "Test", "Practice"])
expInfo = piDlg.show()  # show dialog and wait for OK or Cancel
if expInfo is None:  # or if ok_data is not None
    print('user cancelled')
    sys.exit()
#elif #Try to figure out why the hell I wanted an elif here

confDlg = gui.Dlg(title="Please confirm information")
confDlg.addText('Participant number: ' + expInfo[0])
confDlg.addText('Participant Type: ' + expInfo[1])
confDlg.addText('Experiment Type: ' + expInfo[-1])
confDlg.show()
if not confDlg.OK:
    print('user failed to confirm information')
    sys.exit()


#expInfo = [990, "New", "Study"]

#Run Experiment
exp = PegasusExp(expInfo,'pics/','data/')
exp.run_study()
#print(exp.gen_pic_list())
#exp.genPicList()
#core.wait(3)
#print(exp.getStudyList())
exp.clean_up()



"""
* Version Notes
*
* 0.0.1, 2.7.18
*    Early Alpha, no notes
"""
