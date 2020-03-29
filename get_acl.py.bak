from acl import ACL_detail,ACL
import os
import re
import MySQLdb
class acl_process:
    def __init__(self):
        self.Str1 =''
        self.Partition =''
        self.Check = False

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
        result_str = str1[pos_next_str2:]
    else:
        result_str = str1[pos_next_str2:pos_next_space]
    return result_str

def validIP(address):
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for item in parts:
        if not 0 <= int(item) <= 255:
            return False
    return True


def acl_extended1(s1):
    list_str1 = s1.strip().split()
    result_acl_extended = ACL_detail()
    dict_str = {}

    for item in range(len(list_str1)):
        temp_partern = acl_process()
        temp_partern.Str1 = list_str1[item]
        temp_partern.Partition=''
        temp_partern.Check = False
        dict_str[item] = temp_partern

    check_complete = len(list_str1)
    i = 0
    check_source_ip = 0
    check_source_port =0
    temp_str=""
    while (check_complete >0) and (i<len(list_str1)) :
        if not dict_str[i].Check:
            temp_str = list_str1[i]
            if (list_str1[i] == 'permit') or (list_str1[i] == 'deny'):
                result_acl_extended.Action_1 = list_str1[i]
                dict_str[i].Check = True
                dict_str[i].Partition = 'action'
                i += 1
                temp_str = list_str1[i]
                if (validIP(temp_str)):
                    result_acl_extended.Prefix_Source = temp_str
                    dict_str[i].Check = True
                    dict_str[i].Partition = 'src'
                    if i < (len(list_str1)-1):
                        result_acl_extended.Prefix_Source = temp_str +' '+ list_str1[i+1]
                        i +=1
                        dict_str[i].Check = True
                        dict_str[i].Partition = 'src'
                else:
                    result_acl_extended.Protocol_1 = temp_str
                    dict_str[i ].Partition = 'proto'
                    dict_str[i].Check = True
            elif (validIP(temp_str)) or (temp_str == 'host') or (temp_str == 'any'):
                if check_source_ip == 0:
                    if temp_str == 'host':
                        result_acl_extended.Prefix_Source = 'host ' + list_str1[i + 1]
                        dict_str[i ].Partition = 'src'
                        dict_str[i].Check = True
                        dict_str[i + 1].Partition = 'src'
                        dict_str[i + 1].Check = True
                        i += 1
                    elif temp_str == 'any':
                        result_acl_extended.Prefix_Source = 'any'
                        dict_str[i].Partition = 'src'
                        dict_str[i].Check = True
                    elif validIP(temp_str):
                        result_acl_extended.Prefix_Source = temp_str + ' ' + list_str1[i + 1]
                        dict_str[i].Partition = 'src'
                        dict_str[i].Check = True
                        dict_str[i + 1].Partition = 'src'
                        dict_str[i + 1].Check = True
                        i += 1
                    check_source_ip += 1
                    if i==(len(list_str1)-1):
                        break
                    i +=1
                    temp_str = list_str1[i]
                    if (temp_str == 'eq' )or(temp_str == 'neq') or (temp_str == 'lt' )or (temp_str == 'gt') \
                            or (temp_str == 'range'):
                        result_acl_extended.S_Port = temp_str + ' ' + list_str1[i + 1]
                        dict_str[i].Partition = 'src_port'
                        dict_str[i].Check = True
                        dict_str[i + 1].Partition = 'src_port'
                        dict_str[i + 1].Check = True
                        i +=1
                        check_source_port += 1
                    else:
                        i -=1
                elif check_source_ip == 1:
                    if temp_str == 'host':
                        result_acl_extended.Prefix_Dest = 'host ' + list_str1[i + 1]
                        dict_str[i].Partition = 'dst'
                        dict_str[i].Check = True
                        dict_str[i + 1].Partition = 'dst'
                        dict_str[i + 1].Check = True
                        i += 1
                    elif temp_str == 'any':
                        result_acl_extended.Prefix_Dest = 'any'
                        dict_str[i].Partition = 'dst'
                        dict_str[i].Check = True
                    elif validIP(temp_str):
                        result_acl_extended.Prefix_Dest = temp_str + ' ' + list_str1[i + 1]
                        dict_str[i].Partition = 'dst'
                        dict_str[i].Check = True
                        dict_str[i + 1].Partition = 'dst'
                        dict_str[i + 1].Check = True
                        i += 1
                    if i==(len(list_str1)-1):
                        break
                    i += 1
                    temp_str = list_str1[i]
                    if (temp_str == 'eq' )or(temp_str == 'neq') or (temp_str == 'lt' )or (temp_str == 'gt') \
                            or (temp_str == 'range'):
                        result_acl_extended.D_Port = temp_str + ' ' + list_str1[i + 1]
                        dict_str[i].Partition = 'dst_port'
                        dict_str[i].Check = True
                        dict_str[i + 1].Partition = 'dst_port'
                        dict_str[i + 1].Check = True
                        i += 1
            elif (temp_str == 'precedence')or(temp_str == 'tos') or (temp_str == 'dscp')or (temp_str == 'log'):
                if temp_str=='log':
                    result_acl_extended.Log = True
                    dict_str[i].Partition = 'Log'
                    dict_str[i].Check = True
                elif temp_str =='precedence':
                    result_acl_extended.IP_Pre = temp_str + ' ' + list_str1[i+1]
                    dict_str[i].Partition = 'IP_Pre'
                    dict_str[i].Check = True
                    dict_str[i +1].Partition = 'IP_Pre'
                    dict_str[i + 1].Check = True
                    i +=1
                elif temp_str == 'tos':
                    result_acl_extended.ToS = temp_str + ' ' + list_str1[i + 1]
                    dict_str[i].Partition = 'ToS'
                    dict_str[i].Check = True
                    dict_str[i + 1].Partition = 'ToS'
                    dict_str[i + 1].Check = True
                    i +=1
                elif temp_str == 'dscp':
                    result_acl_extended.ToS = temp_str + ' ' + list_str1[i + 1]
                    dict_str[i].Partition = 'dscp'
                    dict_str[i].Check = True
                    dict_str[i + 1].Partition = 'dscp'
                    dict_str[i + 1].Check = True
                    i +=1
            else:
                result_acl_extended.Option_1 = temp_str
                dict_str[i].Partition ='opt'
                dict_str[i].Check = True
        i +=1
        check_complete = 0
        for item in range(len(list_str1)):
            if dict_str[item].Check == False:
                check_complete +=1
    return result_acl_extended


def get_acl_from_log(list_line,hostname,Dev,total_lines,log_path, conn, cursor):
    try:
        i = 0
        ACL.Hostname = hostname
        ACL_detail.Hostname = hostname
        list_acl = {}
        list_acl_detail = {}
        if not os.path.exists(log_path + "Logs/ACL"):
            os.mkdir(log_path + "Logs/ACL")
        with open(log_path + "Logs/ACL/" + hostname + ".txt", "w") as f:
            f.write("=========Get ACL informations of routers==========\n")
        if Dev == "C76xx":
            while i < total_lines:
                if re.match("ip access-list ", list_line[i].strip()):
                    temp_acl_name = list_line[i].strip().split(" ")[-1].strip()
                    temp_acl_type = list_line[i].strip().split(" ")[-2].strip()
                    temp_acl = ACL()
                    temp_acl.Name = temp_acl_name
                    temp_acl.Type = temp_acl_type
                    list_line[i]='\n'
                    if " remark " in list_line[i+1]:
                        temp_acl.Description = list_line[i+1].strip()[len("remark "):]
                        list_line[i+1] = '\n'
                        i=i+2
                    else:
                        i += 1
                    list_acl[temp_acl.Name]=temp_acl
                    temp_index=0
                    while ("ip access-list" not in list_line[i])and("!" not in list_line[i]):
                        if temp_acl_type == "standard":
                            if ("permit" or "deny" ) in list_line[i]:
                                temp_acl_detail =ACL_detail()
                                temp_acl_detail.Name = temp_acl_name
                                temp_acl_detail.Index_1 = temp_index
                                temp_index +=1
                                temp_acl_detail.Action =list_line[i].strip().split()[0]
                                if "log" in list_line[i]:
                                    temp_acl_detail.Prefix_Source = list_line[i].strip()[(len(temp_acl_detail.Action)+1): \
                                        (len(list_line[i].strip())-len(" log")-1)]
                                    temp_acl_detail.Log = True
                                else:
                                    temp_acl_detail.Prefix_Source = list_line[i].strip()[(len(temp_acl_detail.Action)+1):]
                                list_acl_detail[temp_acl_name+str(temp_acl_detail.Index_1)]=temp_acl_detail
                                list_line[i]="\n"
                        else:
                            temp_acl_detail = acl_extended1(list_line[i].strip())
                            temp_acl_detail.Index_1 = temp_index
                            temp_acl_detail.Name = temp_acl_name
                            #temp_acl_detail.showdata()
                            temp_index += 1
                            list_acl_detail[temp_acl_name + str(temp_acl_detail.Index_1)] = temp_acl_detail
                            list_line[i] = "\n"
                        i += 1
                    i -=1
                elif "access-list" == list_line[i].strip().split(" ")[0]:  # ACL
                    list_acl_index={}
                    temp_index = 0
                    while "!" not in list_line[i]:
                        temp_acl_name = list_line[i].strip().split(" ")[1]
                        temp_str = list_line[i].strip().split()[0] + ' ' + list_line[i].strip().split()[1] + ' '
                        temp_str = list_line[i].strip()[len(temp_str):]
                        if temp_acl_name in list_acl_index.keys():
                            temp_index=list_acl_index[temp_acl_name]+1
                            temp_acl_detail=acl_extended1(temp_str)
                            temp_acl_detail.Name = temp_acl_name
                            temp_acl_detail.Index_1 = temp_index
                            list_acl_index[temp_acl_name] = temp_index
                            list_acl_detail[temp_acl_name + str(temp_acl_detail.Index_1)] = temp_acl_detail
                            list_line[i] = "\n"
                        else:
                            temp_acl = ACL()
                            temp_acl.Type = 'extended'
                            temp_acl.Name = temp_acl_name
                            list_acl[temp_acl_name]=temp_acl
                            list_acl_index[temp_acl_name] = 0
                            temp_acl_detail=acl_extended1(temp_str)
                            temp_acl_detail.Name = temp_acl_name
                            temp_acl_detail.Index_1 = temp_index
                            list_acl_detail[temp_acl_name + str(temp_acl_detail.Index_1)] = temp_acl_detail
                            temp_acl_detail.showdata()
                            list_line[i] = "\n"
                        i +=1
                i += 1
            for item in list_acl:
                list_acl[item].insert(cursor)
            for item in list_acl_detail:
                list_acl_detail[item].insert(cursor)
            i = 0
            f = open(log_path + "Logs/ACL/" + hostname + ".txt", "a")
            while i<total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev == "ASR9k":
            while i<total_lines:
                if re.match('^ipv4 access-list (.*)\n',list_line[i]):
                    temp_acl_name = re.match('^ipv4 access-list (.*)\n',list_line[i]).groups()[0]
                    temp_acl = ACL()
                    temp_acl.Name = temp_acl_name
                    temp_acl.insert(cursor)
                    #print temp_acl_name
                    src_pattern = '(host\s\d+\.\d+\.\d+\.\d+|any|\d+\.\d+\.\d+\.\d+\s\d+\.\d+\.\d+\.\d+)'
                    #src_port_pattern = '(eq|gt|lt|neq|range)'
                    #src_port_range_pattern = '([(\S+\s\S+)]+)'
                    dst_pattern = '(host\s\d+\.\d+\.\d+\.\d+|any|\d+\.\d+\.\d+\.\d+\s\d+\.\d+\.\d+\.\d+)'
                    #option_pattern = '.*'
                    acl_pattern = '^ (\d+) (permit|deny) ipv4 ' + src_pattern + ' ' + dst_pattern +'\n'
                    while list_line[i] != '!\n':
                        temp_result = re.match(acl_pattern, list_line[i])
                        if temp_result:
                            temp_acl_detail = ACL_detail()
                            temp_acl_detail.Name = temp_acl_name
                            temp_acl_detail.Index_1 = temp_result.groups()[0]
                            temp_acl_detail.Action_1 = temp_result.groups()[1]
                            temp_acl_detail.Prefix_Source = temp_result.groups()[2]
                            temp_acl_detail.Prefix_Dest = temp_result.groups()[3]
                            list_line[i] = '\n'
                            temp_acl_detail.insert(cursor)
                        i += 1
                i += 1
            i = 0
            f = open(log_path + "Logs/ACL/" + hostname + ".txt", "a")
            while i<total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev=='HW':
            dict_acl = {}
            dict_acl_detail = {}
            while i < total_lines:
                if re.match('^acl(?: name ([\S]*))? number (.*)\n', list_line[i]):
                    temp_search = re.match('^acl(?: name ([\S]*))? number (.*)\n', list_line[i]).groups()
                    if temp_search[0] is not None:
                        temp_acl_name = temp_search[0].strip()
                    else:
                        temp_acl_name = temp_search[1].strip()
                    temp_acl = ACL()
                    temp_acl.Name = temp_acl_name
                    if re.match('^ description (.*)\n',list_line[i+1]):
                        temp_acl.Description = re.match('^ description (.*)\n',list_line[i+1]).groups()[0]
                        list_line[i+1]='\n'
                        i += 1
                    dict_acl[temp_acl.Name]=temp_acl
                    i += 1
                    while list_line[i] != '#\n':
                        if re.match(' rule ([\d]+) (deny|permit)\n', list_line[i]):
                            temp_search = re.match(' rule ([\d]+) (deny|permit)\n', list_line[i]).groups()
                            temp_acl_detail = ACL_detail()
                            temp_acl_detail.Name = temp_acl_name
                            temp_acl_detail.Index_1 = temp_search[0]
                            temp_acl_detail.Action_1 = temp_search[1]
                            #print 'DK0:'
                            #temp_acl_detail.showdata()
                            dict_acl_detail[temp_acl_detail.Name + '/' + temp_acl_detail.Index_1] = temp_acl_detail
                            list_line[i] = '\n'
                        elif re.match(' rule ([\d]+) (deny|permit)(?: (tcp|udp|ip))(?: vpn-instance ([\S]+))?'
                                      '(?: fragment-type ([\S]+))?'
                                      '(?: source(?: ip-address)? ((?:(?:[\d]{1,3}[\.]){3}[\d]{1,3})'
                                      ' (?:0|(?:[\d]{1,3}[\.]){3}[\d]{1,3})'
                                      '|any))?(?: source-port ((?:eq|gt|lt|neq|range) [\S]+))?'
                                      '(?: destination ((?:(?:[\d]{1,3}[\.]){3}[\d]{1,3})'
                                      ' (?:0|(?:[\d]{1,3}[\.]){3}[\d]{1,3})|any))?'
                                      '(?: destination-port ((?:eq|gt|lt|neq|range) [\S]+))?[\s]*\n',
                                      list_line[i]):
                            temp_search = re.match(' rule ([\d]+) (deny|permit)(?: (tcp|udp|ip))(?: vpn-instance ([\S]+))?'
                                                   '(?: fragment-type ([\S]+))?'
                                                   '(?: source(?: ip-address)? ((?:(?:[\d]{1,3}[\.]){3}[\d]{1,3})'
                                                   ' (?:0|(?:[\d]{1,3}[\.]){3}[\d]{1,3})'
                                                   '|any))?(?: source-port ((?:eq|gt|lt|neq|range) [\S]+))?'
                                                   '(?: destination ((?:(?:[\d]{1,3}[\.]){3}[\d]{1,3})'
                                                   ' (?:0|(?:[\d]{1,3}[\.]){3}[\d]{1,3})|any))?'
                                                   '(?: destination-port ((?:eq|gt|lt|neq|range) [\S]+))?[\s]*\n',
                                                   list_line[i]).groups()
                            temp_acl_detail = ACL_detail()
                            temp_acl_detail.Name = temp_acl_name
                            temp_acl_detail.Index_1 = temp_search[0]
                            temp_acl_detail.Action_1 = temp_search[1]
                            temp_acl_detail.Protocol_1 = temp_search[2]
                            if temp_search[3] is not None:
                                temp_acl_detail.VRF_Name = temp_search[3]
                            if temp_search[4] is not None:
                                print 'Chua tao attribute fragment'
                            if temp_search[5] is not None:
                                temp_acl_detail.Prefix_Source = temp_search[5]
                            if temp_search[6] is not None:
                                temp_acl_detail.S_Port = temp_search[6]
                            if temp_search[7] is not None:
                                temp_acl_detail.Prefix_Dest = temp_search[7]
                            if temp_search[8] is not None:
                                temp_acl_detail.D_Port = temp_search[8]
                            #print 'DK3:'
                            #temp_acl_detail.showdata()
                            dict_acl_detail[temp_acl_detail.Name + '/' + temp_acl_detail.Index_1] = temp_acl_detail
                            list_line[i] = '\n'
                        elif re.match(' rule ([\d]+) (deny|permit)(?: (icmp))(?: vpn-instance ([\S]+))?'
                                      '(?: fragment-type ([\S]+))?'
                                      '(?: source(?: ip-address)? ((?:(?:[\d]{1,3}[\.]){3}[\d]{1,3})'
                                      ' (?:0|(?:[\d]{1,3}[\.]){3}[\d]{1,3})|any))?'
                                      '(?: destination ((?:(?:[\d]{1,3}[\.]){3}[\d]{1,3})'
                                      ' (?:0|(?:[\d]{1,3}[\.]){3}[\d]{1,3})|any))?(?: icmp-type ([\S]+))?[\s]*\n',
                                      list_line[i]):
                            temp_search = re.match(' rule ([\d]+) (deny|permit)(?: (icmp))(?: vpn-instance ([\S]+))?'
                                                   '(?: fragment-type ([\S]+))?'
                                                   '(?: source(?: ip-address)? ((?:(?:[\d]{1,3}[\.]){3}[\d]{1,3})'
                                                   ' (?:0|(?:[\d]{1,3}[\.]){3}[\d]{1,3})|any))?'
                                                   '(?: destination ((?:(?:[\d]{1,3}[\.]){3}[\d]{1,3})'
                                                   ' (?:0|(?:[\d]{1,3}[\.]){3}[\d]{1,3})|any))?(?: icmp-type ([\S]+))?[\s]*\n',
                                                   list_line[i]).groups()
                            temp_acl_detail = ACL_detail()
                            temp_acl_detail.Name = temp_acl_name
                            temp_acl_detail.Index_1 = temp_search[0]
                            temp_acl_detail.Action_1 = temp_search[1]
                            temp_acl_detail.Protocol_1 = temp_search[2]
                            if temp_search[3] is not None:
                                temp_acl_detail.VRF_Name = temp_search[3]
                            if temp_search[4] is not None:
                                print 'Chua tao attribute fragment'
                            if temp_search[5] is not None:
                                temp_acl_detail.Prefix_Source = temp_search[5]
                            if temp_search[6] is not None:
                                temp_acl_detail.Prefix_Dest = temp_search[6]
                            if temp_search[7] is not None:
                                temp_acl_detail.Option_1 = temp_search[7]
                            dict_acl_detail[temp_acl_detail.Name + '/' + temp_acl_detail.Index_1] = temp_acl_detail
                            list_line[i] = '\n'
                        elif re.match(' rule ([\d]+) (deny|permit)(?: source-mac ((?:[A-Fa-f0-9]{4,4}\-){2,2}[A-Fa-f0-9]{4,4} '
                                      '(?:[A-Fa-f0-9]{4,4}\-){2,2}[A-Fa-f0-9]{4,4}))?(?: dest-mac ((?:[A-Fa-f0-9]{4,4}\-){2,2}[A-Fa-f0-9]{4,4} '
                                      '(?:[A-Fa-f0-9]{4,4}\-){2,2}[A-Fa-f0-9]{4,4}))?[\s]*\n',list_line[i]):
                            temp_search = re.match(' rule ([\d]+) (deny|permit)(?: source-mac ((?:[A-Fa-f0-9]{4,4}'
                                                   '\-){2,2}[A-Fa-f0-9]{4,4} (?:[A-Fa-f0-9]{4,4}\-){2,2}'
                                                   '[A-Fa-f0-9]{4,4}))?(?: dest-mac ((?:[A-Fa-f0-9]{4,4}\-){2,2}'
                                                   '[A-Fa-f0-9]{4,4} (?:[A-Fa-f0-9]{4,4}\-){2,2}[A-Fa-f0-9]{4,4}))?[\s]*\n',
                                                   list_line[i]).groups()
                            temp_acl_detail = ACL_detail()
                            temp_acl_detail.Name = temp_acl_name
                            temp_acl_detail.Index_1 = temp_search[0]
                            temp_acl_detail.Action_1 = temp_search[1]
                            if temp_search[2] is not None:
                                temp_acl_detail.Prefix_Source = temp_search[2]
                            if temp_search[3] is not None:
                                temp_acl_detail.Prefix_Dest = temp_search[3]
                            #print 'DK2:'
                            #temp_acl_detail.showdata()
                            dict_acl_detail[temp_acl_detail.Name + '/' + temp_acl_detail.Index_1] = temp_acl_detail
                            list_line[i] = '\n'
                        elif re.match(' rule ([\d]+) (deny|permit)(?: vpn-instance ([\S]+))?(?: fragment-type ([\S]+))?'
                                    ' source ((?:(?:(?:[\d]{1,3}[\.]){3}[\d]{1,3}) (?:0|(?:[\d]{1,3}[\.]){3}[\d]{1,3})'
                                    ')|any)[\s]*\n',list_line[i]):
                            temp_search = re.match(' rule ([\d]+) (deny|permit)(?: vpn-instance ([\S]+))?(?: fragment-type ([\S]+))?'
                                    '(?: source ((?:(?:[\d]{1,3}[\.]){3}[\d]{1,3}) (?:0|(?:[\d]{1,3}[\.]){3}[\d]{1,3})'
                                    ')|any)[\s]*\n',list_line[i]).groups()

                            temp_acl_detail = ACL_detail()
                            temp_acl_detail.Name = temp_acl_name
                            temp_acl_detail.Index_1 = temp_search[0]
                            temp_acl_detail.Action_1 = temp_search[1]
                            if temp_search[4] is not None:
                                temp_acl_detail.Prefix_Source = temp_search[4]
                            else:
                                temp_acl_detail.Prefix_Source = 'any'
                            if temp_search[2] is not None:
                                temp_acl_detail.VRF_Name = temp_search[2]
                            if temp_search[3] is not None:
                                print 'Chua tao attribute Fragment'
                            #print 'DK1:'
                            #temp_acl_detail.showdata()
                            dict_acl_detail[temp_acl_detail.Name+'/'+temp_acl_detail.Index_1] = temp_acl_detail
                            list_line[i] = '\n'
                        i += 1
                    i -= 1
                elif re.match('[\s]?ip ip-prefix ([\S]+) index ([\d]+) permit ((?:(?:[\d]{1,3}[\.]){3}[\d]{1,3})) [\d]+'
                              '(?: greater-equal ([\d]+) less-equal ([\d]+))?\n',list_line[i]):
                    temp_search = re.match('[\s]?ip ip-prefix ([\S]+) index ([\d]+) permit ((?:(?:[\d]{1,3}[\.]){3}[\d]{1,3}) [\d]+)'
                              '(?: greater-equal ([\d]+) less-equal ([\d]+))?\n',list_line[i]).groups()
                    #print temp_search
                    temp_acl_name = temp_search[0]
                    temp_acl = ACL()
                    temp_acl.Name = temp_acl_name
                    if temp_acl.Name not in dict_acl:
                        dict_acl[temp_acl.Name]=temp_acl
                    temp_acl_detail = ACL_detail()
                    temp_acl_detail.Name = temp_search[0]
                    temp_acl_detail.Index_1 = temp_search[1]
                    if temp_search[3] is not None:
                        temp_acl_detail.Prefix_Source = temp_search[2] + ' ' + temp_search[3] + '-' + temp_search[4]
                    else:
                        temp_acl_detail.Prefix_Source = temp_search[2]
                    dict_acl_detail[temp_acl_detail.Name + '/' + temp_acl_detail.Index_1] = temp_acl_detail
                    #temp_acl_detail.showdata()
                    list_line[i]='\n'
                i += 1
            i=0
            while i< total_lines:
                if re.match('user-interface vty .*\n',list_line[i]):
                    #print list_line[i]
                    i += 1
                    #print 'Dong ke tiep:',list_line[i]
                    while re.match(' ',list_line[i]) is not None:
                        if re.match(' acl ([\S]+) inbound\n',list_line[i]):
                            #print 'Kiem acl MGMT',list_line[i]
                            temp_search = re.match(' acl ([\S]+) inbound\n',list_line[i]).groups()
                            #print 'Ket qua search:',temp_search[0]
                            if temp_search[0] in dict_acl:
                                #print 'Match acl trong dict_acl'
                                dict_acl[temp_search[0]].Purpose='MGMT'
                            list_line[i]='\n'
                        i += 1
                    i -=1
                i += 1
            for key in dict_acl:
                #dict_acl[key].showdata()
                dict_acl[key].insert(cursor)
            for key in dict_acl_detail:
                #dict_acl_detail[key].showdata()
                dict_acl_detail[key].insert(cursor)
            i = 0
            f = open(log_path + "Logs/ACL/" + hostname + ".txt", "a")
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