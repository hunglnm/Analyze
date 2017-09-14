from policy_map import Policy_map
import MySQLdb
import os
import re


class behaviour:
    def __init__(self):
        self.name = ''
        self.service_class = ''
        self.action = ''
        self.cir = 0
        self.pir = 0
        self.cbs = 0
        self.pbs = 0
        self.green = ''
        self.yellow = ''
        self.red = ''
        self.remark_ip = ''
        self.remark_exp = ''
        self.remark_dscp = ''
        self.remark_8021p = ''

    def showdata(self):
        attrs = vars(self)
        print ','.join("%s: %s" % item for item in attrs.items())


def get_next_word(str1,str2):
    result_str = ""
    pos_str2 = str1.find(str2, 0)
    if pos_str2 <0:
        return result_str
        exit()
    pos_next_str2 = pos_str2+len(str2)
    pos_next_space=str1.find(" ",pos_next_str2)
    if pos_next_space <0:
        result_str = str1[pos_next_str2:].strip()
    else:
        result_str = str1[pos_next_str2:pos_next_space].strip()
    return result_str


def get_policy_map_from_log(list_line,hostname,Dev,total_lines,log_path, conn, cursor):
    try:
        i = 0
        Policy_map.Hostname = hostname
        if not os.path.exists(log_path + "Logs/Policy"):
            os.mkdir(log_path + "Logs/Policy")
        with open(log_path + "Logs/Policy/" + hostname + ".txt", "w") as f:
            f.write("=========Get Policy smap informations of routers==========\n")
        f = open(log_path + "Logs/Policy/" + hostname + ".txt", "a")
        if Dev == "C76xx":
            while i < total_lines:
                if list_line[i].strip().split(" ")[0] == "policy-map":
                    temp_policy_map_name = list_line[i].strip().split(" ")[-1].strip()
                    temp_line = list_line[i]
                    f.write("\n")
                    temp_pos=i
                    i += 1
                    while "policy-map" not in list_line[i]:
                        check_cond = False
                        if " class " in list_line[i]:
                            temp_policy_map = Policy_map()
                            temp_policy_map.Name = temp_policy_map_name
                            temp_policy_map.Class = get_next_word(list_line[i], ' class ')
                            check_cond = True
                        if ' police ' in list_line[i]:
                            if get_next_word(list_line[i], ' police ') == 'cir':
                                temp_policy_map.Police = 0
                            else:
                                temp_policy_map.Police = int(get_next_word(list_line[i], ' police '))
                            check_cond = True
                        if " cir " in list_line[i]:
                            temp_policy_map.CIR = int(get_next_word(list_line[i], ' cir '))
                            check_cond = True
                        if " bc " in list_line[i]:
                            temp_policy_map.BC = int(get_next_word(list_line[i], ' bc '))
                            check_cond = True
                        if " pir " in list_line[i]:
                            temp_policy_map.PIR = int(get_next_word(list_line[i], ' pir '))
                            check_cond = True
                        if " be " in list_line[i]:
                            temp_policy_map.BE = int(get_next_word(list_line[i], ' be '))
                            check_cond = True
                        if " conform-action " in list_line[i]:
                            temp_policy_map.Conform_action = get_next_word(list_line[i], ' conform-action ')
                            check_cond = True
                        if " set-prec-transmit " in list_line[i]:
                            temp_policy_map.Set_prec_transmit = get_next_word(list_line[i], ' set-prec-transmit ')
                            check_cond = True
                        if " exceed-action " in list_line[i]:
                            temp_policy_map.Exceed_action = get_next_word(list_line[i], ' exceed-action ')
                            check_cond = True
                        if "violate-action " in list_line[i]:
                            temp_policy_map.Violate_action = get_next_word(list_line[i], ' violate-action ')
                            check_cond = True
                        if " shape average " in list_line[i]:
                            temp_policy_map.Shape = int(get_next_word(list_line[i], ' shape average '))
                            check_cond = True
                        if " queue-limit " in list_line[i]:
                            temp_policy_map.Queue_limit = int(get_next_word(list_line[i], ' queue-limit '))
                            check_cond = True
                        if " priority" in list_line[i]:
                            temp_policy_map.Priority = 'priority'
                            check_cond = True
                        if " bandwidth percent " in list_line[i]:
                            temp_policy_map.BW = int(get_next_word(list_line[i], ' bandwidth percent '))
                            check_cond = True
                        if " service-policy " in list_line[i]:
                            temp_policy_map.Service_policy = get_next_word(list_line[i], ' service-policy ')
                            check_cond = True
                        if " random-detect aggregate" in list_line[i]:
                            temp_policy_map.RED_Agg = True
                            check_cond = True
                        if " random-detect precedence " in list_line[i]:
                            temp_policy_map.RED_Pre = list_line[i].strip().split(" ")[3].strip()
                            temp_policy_map.RED_Min = list_line[i].strip().split(" ")[5].strip()
                            temp_policy_map.RED_Max = list_line[i].strip().split(" ")[7].strip()
                            temp_policy_map.RED_Mark = list_line[i].strip().split(" ")[-1].strip()
                            check_cond = True
                        if "set precedence" in list_line[i]:
                            temp_policy_map.Set_prec_transmit = list_line[i].strip().split()[-1]
                            check_cond = True
                        if "set mpls experimental imposition" in list_line[i]:
                            temp_policy_map.Set_prec_transmit = list_line[i].strip().split()[-1]
                            check_cond = True
                        if "!" in list_line[i]:
                            f.write(list_line[i])
                            break
                        if check_cond == True:
                            f.write("\n")
                            if temp_policy_map.Name == 'VPN_ERS_1M':
                                print list_line[i]
                            temp_str = list_line[i+1]
                        if (" class " in temp_str) or ("!" in temp_str) or ("policy-map" in temp_str):
                            temp_policy_map.insert(cursor)
                        i +=1
                    i -=1
                else:
                    f.write(list_line[i])
                i += 1
        elif Dev == "ASR9k":
            list_policy_map = {}
            while i < total_lines:
                if list_line[i].strip().split(" ")[0] == "policy-map":
                    temp_policy_map_name = list_line[i].strip().split(" ")[-1].strip()
                    temp_line = list_line[i]
                    #print temp_policy_map_name
                    temp_pos = i
                    i += 1
                    while "end-policy-map" not in list_line[i]:
                        if " class " in list_line[i]:
                            temp_policy_map = Policy_map()
                            temp_policy_map.Name = temp_policy_map_name
                            temp_policy_map.Class = get_next_word(list_line[i], ' class ')
                            print temp_policy_map.Class
                        if ' police ' in list_line[i]:
                            if get_next_word(list_line[i], ' police ') == 'rate':
                                temp_policy_map.Police = 0
                            else:
                                temp_policy_map.Police = int(get_next_word(list_line[i], ' police '))
                                list_line[i] = '\n'
                        if " rate " in list_line[i]:
                            if get_next_word(list_line[i], ' rate ') == 'percent':
                                temp_policy_map.BW = int(get_next_word(list_line[i], ' percent '))
                            else:

                                if 'mbps' in list_line[i].strip().split()[-1]:
                                    temp_policy_map.Police = int(get_next_word(list_line[i], ' rate ')) * 1000000
                                elif 'kbps' in list_line[i].strip().split()[-1]:
                                    temp_policy_map.Police = int(get_next_word(list_line[i], ' rate ')) * 1000
                                else:
                                    temp_policy_map.Police = int(get_next_word(list_line[i], ' rate '))
                            list_line[i] = '\n'
                            #print temp_policy_map_name,temp_policy_map.Police
                        if " conform-action " in list_line[i]:
                            temp_policy_map.Conform_action = get_next_word(list_line[i], ' conform-action ')
                            list_line[i] = '\n'
                        if " exceed-action " in list_line[i]:
                            temp_policy_map.Exceed_action = get_next_word(list_line[i], ' exceed-action ')
                            list_line[i] = '\n'
                        if " queue-limit " in list_line[i]:
                            temp_policy_map.Queue_limit = int(get_next_word(list_line[i], ' queue-limit '))
                            list_line[i] = '\n'
                        if " priority" in list_line[i]:
                            temp_policy_map.Priority = 'priority'
                            list_line[i] = '\n'
                        if " bandwidth percent " in list_line[i]:
                            temp_policy_map.BW = int(get_next_word(list_line[i], ' bandwidth percent '))
                            list_line[i] = '\n'
                        if " random-detect precedence " in list_line[i]:
                            temp_policy_map.RED_Pre = list_line[i].strip().split(" ")[2].strip()
                            temp_policy_map.RED_Min = list_line[i].strip().split(" ")[3].strip()
                            temp_policy_map.RED_Max = list_line[i].strip().split(" ")[5].strip()
                            list_line[i] = '\n'
                        temp_str = list_line[i + 1]
                        if re.match(' !\n', temp_str):
                            print 'Ket qua duoc ghi:'
                            temp_policy_map.showdata()
                            temp_policy_map.insert(cursor)
                        i += 1
                    if 'end-policy-map' in list_line[i]:
                        list_line[i] = '\n'
                i += 1
            i = 0
            while i < total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev == 'HW':
            list_policy_map = {}
            list_ba = {}
            #get behavior
            while i < total_lines:
                if re.match('traffic behavior .*',list_line[i]):
                    temp_behavior = behaviour()
                    temp_behavior.name = list_line[i].strip().split()[-1]
                    i += 1
                    j=i
                    while (list_line[i]!='#\n')and('traffic behavior 'not in list_line[i]):
                        if re.match('car (cir [\d]*)( pir [\d]*)?( cbs [\d]*)?( pbs [\d]*)?( green (?:discard|pass)'
                                    '(?: service-class [a-zA-Z]+)?(?: color (?:green|yellow|red))?)?'
                                    '( yellow (?:discard|pass)(?: service-class [a-zA-Z]+)?(?: color '
                                    '(?:green|yellow|red))?)?( red (?:discard|pass)(?: service-class [a-zA-Z]+)?'
                                    '(?: color (?:green|yellow|red))?)?',list_line[i].strip()):
                            temp_list = re.match('car (cir [\d]*)( pir [\d]*)?( cbs [\d]*)?( pbs [\d]*)?'
                                                 '( green (?:discard|pass)(?: service-class [a-zA-Z]+)?'
                                                 '(?: color (?:green|yellow|red))?)?( yellow (?:discard|pass)'
                                                 '(?: service-class [a-zA-Z]+)?(?: color (?:green|yellow|red))?)?'
                                                 '( red (?:discard|pass)(?: service-class [a-zA-Z]+)?'
                                                 '(?: color (?:green|yellow|red))?)?',
                                                 list_line[i].strip()).groups()
                            list_line[i] = '\n'
                            for item in temp_list:
                                if item is not None:
                                    if 'cir' in item:
                                        temp_behavior.cir = item.split()[-1]
                                    elif 'pir' in item:
                                        temp_behavior.pir = item.split()[-1]
                                    elif 'cbs' in item:
                                        temp_behavior.cbs = item.split()[-1]
                                    elif 'pbs' in item:
                                        temp_behavior.pbs = item.split()[-1]
                                    elif re.match('green .*',item):
                                        temp_behavior.green = item
                                    elif re.match('yellow .*',item):
                                        temp_behavior.yellow = item
                                    elif re.match('red .*', item):
                                        temp_behavior.red = item
                        elif re.match('remark dscp (.*)\n',list_line[i].strip()):
                            temp_behavior.remark_dscp=re.match('remark dscp (.*)\n',list_line[i].strip()).group(1)
                        elif re.match('remark ip-precedence (.*)\n',list_line[i].strip()):
                            temp_behavior.remark_ip=re.match('remark ip-precedence(.*)\n',list_line[i].strip()).group(1)
                        elif re.match('remark 8021p (.*)\n',list_line[i].strip()):
                            temp_behavior.remark_8021p = re.match('remark 8021p (.*)\n',list_line[i].strip()).group(1)
                        elif re.match('remark mpls-exp (.*)\n',list_line[i].strip()):
                            temp_behavior.remark_exp=re.match('remark mpls-exp (.*)\n',list_line[i].strip()).group(1)
                        i += 1
                    i -=1
                    if temp_behavior.action=='':
                        temp_behavior.action = 'permit'
                    list_ba[temp_behavior.name] = temp_behavior
                elif re.match('traffic policy .*\n',list_line[i]):
                    #print 'Co match policy'
                    temp_policy_map = Policy_map()
                    temp_policy_map.Name = list_line[i].strip().split()[-1]
                    i += 1
                    while (list_line[i]!='#\n')and('traffic policy' not in list_line[i]):
                        if re.match(' classifier (.*) behavior (.*)\n',list_line[i]):
                            temp_policy_map.Class = re.match(' classifier (.*) behavior (.*)\n',list_line[i]).group(1)
                            temp_str = re.match(' classifier (.*) behavior (.*)\n',list_line[i]).group(2)
                            if temp_str in list_ba:
                                temp_policy_map.Set_prec_transmit = list_ba[temp_str].remark_ip
                                temp_policy_map.Exceed_action = list_ba[temp_str].red
                                temp_policy_map.CIR = list_ba[temp_str].cir
                                temp_policy_map.PIR = list_ba[temp_str].pir
                                temp_policy_map.BC = list_ba[temp_str].cbs
                                temp_policy_map.Set_EXP = list_ba[temp_str].remark_exp
                                temp_policy_map.BE = list_ba[temp_str].remark_dscp
                                temp_policy_map.p1 = list_ba[temp_str].remark_8021p
                            list_line[i] = '\n'
                        i += 1
                    list_policy_map[temp_policy_map.Name] = temp_policy_map
                    i -= 1
                i += 1
            #for key in list_ba:
            #    list_ba[key].showdata()
            for key in list_policy_map:
                list_policy_map[key].insert(cursor)
            i = 0
            while i < total_lines:
                f.write(list_line[i])
                i += 1
        else:
            print "Device is not support in this script"
        conn.commit()
    except MySQLdb.Error as error:
        print(error)
    finally:
        f.close()