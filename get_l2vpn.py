from l2vpn import L2VPN, VSI
import pymysql
import os
import re
from ifl import IFL

class l2vpn_general:
    def __init__(self):
        self.name = ''
        self.type = ''
        self.description = ''
        self.vpn_id = 0
        self.bd_id = ''
        self.mtu = 0


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


def get_l2vpn_from_log(list_line, hostname, Dev, total_lines, log_path,conn, cursor):
    try:
        i = 0
        L2VPN.Hostname = hostname
        if not os.path.exists(log_path + "Logs/L2VPN"):
            os.mkdir(log_path + "Logs/L2VPN")
        with open(log_path + "Logs/L2VPN/" + hostname + ".txt", "w") as f:
            f.write("=========Get L2VPN informations of routers==========\n")
        f = open(log_path + "Logs/L2VPN/" + hostname + ".txt", "a")
        temp_l2vpn_name = ""
        list_l2vpn = {}
        list_peer = {}
        if Dev == "C76xx":
            while i < total_lines:
                temp_l2vpn_name=''
                if "l2 vfi" in list_line[i]:
                    #print i,list_line[i]
                    temp_l2vpn_name = list_line[i].strip().split(" ")[2].strip()
                    temp_l2vpn_type = "vpls"
                    temp_l2vpn_mtu = 0
                    temp_l2vpn_BD_ID = ""
                    temp_l2vpn_Description = ""
                    j = i
                    while j < total_lines:
                        if list_line[j].strip()==("xconnect vfi " + temp_l2vpn_name):
                            while "!" not in list_line[j]:
                                if "mtu" in list_line[j]:
                                    temp_l2vpn_mtu = int(list_line[j].strip().split(" ")[-1])
                                    list_line[i] = '\n'
                                elif "interface Vlan" in list_line[j]:
                                    temp_l2vpn_BD_ID = int(list_line[j].strip().split(" ")[-1][4:])
                                    list_line[i] = '\n'
                                elif "description " in list_line[j]:
                                    temp_l2vpn_Description = list_line[j].strip()[len('description'):]
                                    list_line[i] = '\n'
                                j -= 1
                            break
                        j += 1
                    i += 1
                    #if 'l2 vfi' in list_line[i]:
                    #    i -= 1
                    while ("!" not in list_line[i])and('l2 vfi' not in list_line[i]):
                        if " vpn id " in list_line[i]:
                            temp_l2vpn_vpn_id = int(list_line[i].strip().split(" ")[2].strip())
                            list_line[i] = '\n'
                        elif " neighbor " in list_line[i]:
                            temp_l2vpn = L2VPN()
                            temp_l2vpn.Peer = list_line[i].strip().split(" ")[1].strip()
                            temp_l2vpn.Name = temp_l2vpn_name
                            temp_l2vpn.VPN_ID = temp_l2vpn_vpn_id
                            temp_l2vpn.Type = temp_l2vpn_type
                            temp_l2vpn.MTU = temp_l2vpn_mtu
                            temp_l2vpn.BD_ID = temp_l2vpn_BD_ID
                            temp_l2vpn.Description = temp_l2vpn_Description
                            if " encapsulation " in list_line[i]:
                                temp_l2vpn.Encap = list_line[i].strip().split(" ")[2].strip()
                                temp_l2vpn.VC_ID = temp_l2vpn_vpn_id
                                if temp_l2vpn.Encap != "encapsulation":
                                    print(list_line[i])
                                    print(temp_l2vpn.VC_ID)
                                    temp_l2vpn.VC_ID = int(list_line[i].strip().split(" ")[2])
                                    temp_l2vpn.Encap = list_line[i].strip().split(" ")[3].strip()
                                    print(temp_l2vpn.VC_ID)
                            if "no-split-horizon" in list_line[i]:
                                temp_l2vpn.No_split = True
                            list_line[i] = '\n'
                            if "backup peer" in list_line[i + 1]:
                                temp_l2vpn.BK_Peer = list_line[i + 1].strip().split(" ")[2].strip()
                                list_line[i + 1] = '\n'
                            temp_l2vpn.insert(cursor)
                        i += 1
                    i -= 1
                    if 'temp_l2vpn' not in locals():
                        temp_l2vpn = L2VPN()
                        temp_l2vpn.Peer = "NA"
                        #temp_l2vpn.Name = temp_l2vpn_name
                        #temp_l2vpn.VPN_ID = temp_l2vpn_vpn_id
                        #temp_l2vpn.VC_ID = temp_l2vpn_vpn_id
                        #temp_l2vpn.Type = temp_l2vpn_type
                        temp_l2vpn.insert(cursor)
                elif (" xconnect " in list_line[i]) and (" vfi " not in list_line[i]):

                    temp_l2vpn = L2VPN()
                    temp_l2vpn.Peer = list_line[i].strip().split(" ")[1]
                    temp_l2vpn.VC_ID = list_line[i].strip().split(" ")[2]
                    if " encapsulation " in list_line[i]:
                        temp_l2vpn.Encap = list_line[i].strip().split(" ")[3].strip()
                        if temp_l2vpn.Encap == "encapsulation":
                            temp_l2vpn.VC_ID = int(list_line[i].strip().split(" ")[2])
                            temp_l2vpn.Encap = list_line[i].strip().split(" ")[4].strip()
                    if " pw-class " in list_line[i]:
                        temp_l2vpn.PW_Class = list_line[i].strip().split(" ")[-1].strip()
                    while '!' not in list_line[i]:
                        if " backup " in list_line[i]:
                            temp_l2vpn.BK_Peer = list_line[i].strip().split(" ")[2].strip()
                        elif " mtu " in list_line[i]:
                            temp_l2vpn.MTU = list_line[i].strip().split(" ")[-1].strip()
                        i += 1
                    j = i - 1
                    while "!" not in list_line[j]:
                        if "interface Vlan" in list_line[j]:
                            temp_l2vpn.Type = "vpls"
                            temp_l2vpn.BD_ID = int(list_line[j].strip().split(" ")[-1][4:])
                        elif (" service " in list_line[j]):
                            temp_l2vpn.Type = "l2circuit"
                        elif ("interface" in list_line[j]) and ("vlan" not in list_line[j]):
                            temp_l2vpn.Type = "l2circuit"
                        elif "description" in list_line[j]:
                            temp_l2vpn.Description = list_line[j].strip()[len('description'):]
                        j -= 1
                    temp_l2vpn.insert(cursor)
                i += 1
            i = 0
            while i<total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev == "ASR9k":
            pos_1 = 0
            pos_2 = 0
            pos_3 = 0
            while i< total_lines:
                if (list_line[i] == 'l2vpn\n') and(pos_1 == 0):
                    pos_1 = i
                if (' bridge group ' in list_line[i]) and (i > pos_1) and (pos_1 > 0) and(pos_2 == 0):
                    pos_2 = i
                if (list_line[i] == '!\n') and (i > pos_2) and (pos_2 > 0) and (pos_3 == 0):
                    pos_3 = i
                if (pos_1 > 0) and (pos_2 > 0) and (pos_3 > 0):
                    break
                i += 1
            print(pos_1, pos_2, pos_3)
            i = pos_1
            while i < pos_2:
                if re.match('  p2p ', list_line[i]):
                    temp_desc = ''
                    temp_ifl_name = ''
                    temp_peer = ''
                    temp_vc_id = ''
                    while list_line[i] != '  !\n':
                        if re.match('^  p2p (.*)\n',list_line[i]):
                            temp_desc = re.match('^  p2p (.*)\n',list_line[i]).groups()[0]
                        elif re.match('^   interface ([\S]+)\n', list_line[i]):
                            temp_ifl_name = re.match('^   interface ([\S]+)\n', list_line[i]).groups()[0]
                        elif re.match('^   neighbor ipv4 (.*) pw-id ([\d]+)\n',list_line[i]):
                            temp_peer = re.match('^   neighbor ipv4 (.*) pw-id ([\d]+)\n',list_line[i]).groups()[0]
                            temp_vc_id = re.match('^   neighbor ipv4 (.*) pw-id ([\d]+)\n', list_line[i]).groups()[1]
                            list_line[i] = '\n'
                        i += 1
                    if (temp_peer != '') and (temp_vc_id != ''):
                        temp_l2vpn = L2VPN()
                        temp_l2vpn.Peer = temp_peer
                        temp_l2vpn.VC_ID = temp_vc_id
                        temp_l2vpn.Description = temp_desc
                        temp_l2vpn.Type = 'l2circuit'
                        if temp_ifl_name!='':
                            temp_l2vpn.IFL = temp_ifl_name
                        temp_l2vpn.insert(cursor)
                i += 1
            i = pos_2
            temp_desc = ''
            while i < pos_3:
                #print list_line[i]
                if re.match('^ bridge group (.*)\n',list_line[i]):
                    temp_desc = re.match('^ bridge group (.*)\n',list_line[i]).groups()[0]
                elif re.match('^  bridge-domain .*\n', list_line[i]):
                    temp_l2vpn_name = ''
                    temp_mtu = 0
                    temp_peer = ''
                    temp_no_split = True
                    temp_vc_id = ''
                    temp_mesh_group = ''
                    temp_mac_limit = 0
                    temp_admin_status = True
                    while list_line[i] != '  !\n':
                        if re.match('^  bridge-domain (.*)\n', list_line[i]):
                            temp_l2vpn_name = re.match('^  bridge-domain (.*)\n', list_line[i]).groups()[0]
                        elif re.match('^   shutdown\n',list_line[i]):
                            temp_admin_status = False
                        elif re.match('^   mac\n', list_line[i]):
                            if 'maximum' in list_line[i+2]:
                                temp_mac_limit = int(list_line[i+2].strip().split()[-1])
                                list_line[i+2] = '\n'
                                list_line[i+1] = '\n'
                                list_line[i] = '\n'
                        elif re.match('^   mtu (.*)\n',list_line[i]):
                            temp_mtu = re.match('^   mtu (.*)\n', list_line[i]).groups()[0]
                            list_line[i] = '\n'
                        elif re.match('^   neighbor (.*) pw-id ([\d]*)', list_line[i]):
                            temp_no_split = True
                            temp_peer = re.match('^   neighbor (.*) pw-id ([\d]*)', list_line[i]).groups()[0]
                            temp_vc_id = re.match('^   neighbor (.*) pw-id ([\d]*)', list_line[i]).groups()[1]
                            temp_l2vpn.mac_limit = temp_mac_limit
                            list_line[i] = '\n'
                            if 'split-horizon' in list_line[i+1]:
                                temp_no_split = False
                                list_line[i+1] = '\n'
                            if temp_peer != '' and temp_vc_id != '':
                                temp_l2vpn = L2VPN()
                                temp_l2vpn.Peer = temp_peer
                                temp_l2vpn.VC_ID = temp_vc_id
                                temp_l2vpn.Description = temp_desc
                                temp_l2vpn.Type = 'vpls'
                                temp_l2vpn.Name = temp_l2vpn_name
                                temp_l2vpn.BD_ID = temp_l2vpn_name
                                temp_l2vpn.No_split = temp_no_split
                                temp_l2vpn.mac_limit = temp_mac_limit
                                temp_l2vpn.MTU = int(temp_mtu)
                                temp_l2vpn.Admin_status = temp_admin_status
                                #temp_l2vpn.showdata()
                                temp_l2vpn.insert(cursor)
                        elif re.match('^   vfi (.*)\n',list_line[i]):
                            temp_mesh_group = re.match('^   vfi (.*)\n',list_line[i]).groups()[0]
                        elif re.match('^    neighbor (.*) pw-id ([\d]*)', list_line[i]):
                            temp_peer = re.match('^    neighbor (.*) pw-id ([\d]*)', list_line[i]).groups()[0]
                            temp_vc_id = re.match('^    neighbor (.*) pw-id ([\d]*)', list_line[i]).groups()[1]
                            temp_no_split = False
                            list_line[i] = '\n'
                            if temp_peer != '' and temp_vc_id != '':
                                temp_l2vpn = L2VPN()
                                temp_l2vpn.Peer = temp_peer
                                temp_l2vpn.VC_ID = temp_vc_id
                                temp_l2vpn.Description = temp_desc
                                temp_l2vpn.Type = 'vpls'
                                temp_l2vpn.Name = temp_l2vpn_name
                                temp_l2vpn.BD_ID = temp_l2vpn_name
                                temp_l2vpn.No_split = temp_no_split
                                temp_l2vpn.MTU = int(temp_mtu)
                                temp_l2vpn.Meshgroup = temp_mesh_group
                                temp_l2vpn.Admin_status = temp_admin_status
                                #temp_l2vpn.showdata()
                                temp_l2vpn.insert(cursor)
                        else:
                            print(list_line[i])
                        i += 1
                elif re.match('^ !\n',list_line[i]):
                    temp_desc = ''
                i += 1
            i = 0
            while i < total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev == 'HW':
            VSI.Hostname = hostname
            while i < total_lines:
                if re.match('vsi ([\S]*)(?: ([\S]*))?\n',list_line[i]):
                    #print i,list_line[i]
                    temp_vsi = VSI()
                    temp_search = re.match('vsi ([\S]*)(?: ([\S]*))?\n',list_line[i]).groups()
                    temp_vsi.name = temp_search[0]
                    if temp_search[1] is not None:
                        temp_vsi.type = temp_search[1]
                    i += 1
                    j=i
                    while list_line[i]!='#\n':
                        if re.match('^  vsi-id ([\d]*)\n',list_line[i]):
                            temp_vsi.vsi_id = int(re.match('^  vsi-id ([\d]*)\n',list_line[i]).group(1))
                            list_line[i]='\n'
                        elif re.match(' description (.*)\n',list_line[i]):
                            temp_vsi.description = re.match(' description (.*)\n',list_line[i]).groups()[0]
                            list_line[i]='\n'
                        elif re.match('^ isolate spoken\n',list_line[i]):
                            temp_vsi.isolate = True
                            list_line[i] = '\n'
                        elif re.match('^ mac-limit maximum ([\d]*)(?: rate [\d]*)\n',list_line[i]):
                            temp_vsi.mac_limit = int(re.match('^ mac-limit maximum ([\d]*)(?: rate [\d]*)\n',list_line[i]).group(1))
                            list_line[i] = '\n'
                        elif re.match(' admin-vsi\n',list_line[i]):
                            temp_vsi.admin_vsi = True
                            list_line[i] = '\n'
                        elif re.match(' track admin-vsi admin-vsi\n',list_line[i]):
                            temp_vsi.track_admin_vsi = True
                        elif re.match(' encapsulation ([\S]*)\n',list_line[i]):
                            temp_vsi.encap = re.match(' encapsulation ([\S]*)\n',list_line[i]).group(1)
                            list_line[i] = '\n'
                        elif re.match(' diffserv-mode pipe (.*)\n',list_line[i]):
                            temp_vsi.classifier = re.match(' diffserv-mode pipe (.*)\n',list_line[i]).group(1)
                            list_line[i] = '\n'
                        elif re.match(' mtu ([\d]*\n)',list_line[i]):
                            temp_vsi.MTU = re.match(' mtu ([\d]*\n)',list_line[i]).group(1)
                            list_line[i] = '\n'
                        elif re.match(' unknown-frame unicast drop',list_line[i]):
                            temp_vsi.un_unicast = True
                            list_line[i] = '\n'
                        elif re.match(' unknown-frame multicast drop',list_line[i]):
                            temp_vsi.un_multicast = True
                            list_line[i] = '\n'
                        elif re.match(' loop-detect .*\n',list_line[i]):
                            temp_vsi.loop_detect = True
                            list_line[i]='\n'
                        elif re.match('  peer ([\S]*)(?: negotiation-vc-id ([\d]*))?(?: tnl-policy ([\S]*))?(?: (upe))?(?: pw pw1)?( )?\n',
                                      list_line[i]):
                            temp_l2vpn = L2VPN()
                            temp_str = re.match('  peer ([\S]*)(?: negotiation-vc-id ([\d]*))?(?: tnl-policy ([\S]*))?'
                                                '(?: (upe))?(?: pw pw1)?( )?\n', list_line[i]).groups()
                            temp_l2vpn.Peer=temp_str[0]
                            temp_l2vpn.Name =temp_vsi.name
                            temp_l2vpn.BD_ID = temp_vsi.name
                            temp_l2vpn.Type = 'vpls'
                            if temp_str[1] is not None:
                                temp_l2vpn.VC_ID =int(temp_str[1])
                            else:
                                temp_l2vpn.VC_ID = temp_vsi.vsi_id
                            if temp_str[2] is not None:
                                temp_l2vpn.PW_Class = temp_str[2]
                            if temp_str[3] is not None:
                                temp_l2vpn.UPE = True
                            list_line[i]='\n'
                            if 'secondary\n' in list_line[i+1]:
                                temp_str = re.match('  peer ([\S]*)(?: negotiation-vc-id ([\d]*))?(?: tnl-policy '
                                                    '([\S]*))?(?: (upe))?(?: pw pw1)? secondary\n',
                                                    list_line[i+1]).groups()
                                temp_l2vpn.BK_Peer = temp_str[0]
                                if temp_str[1] is not None:
                                    temp_l2vpn.Bk_vc_id = int(temp_str[1])
                                else:
                                    temp_l2vpn.Bk_vc_id = temp_vsi.vsi_id
                                if temp_str[2] is not None:
                                    temp_l2vpn.PW_class_bk = temp_str[2]
                                if temp_str[3] is not None:
                                    temp_l2vpn.UPE_bk = True
                                list_line[i+1] = '\n'
                                i +=1
                            if temp_l2vpn.Peer+'/'+str(temp_l2vpn.VC_ID) in list_peer:
                                if list_peer[temp_l2vpn.Peer+'/'+str(temp_l2vpn.VC_ID)].UPE:
                                    temp_l2vpn.UPE = True
                                if list_peer[temp_l2vpn.Peer + '/' + str(temp_l2vpn.VC_ID)].UPE_bk:
                                    temp_l2vpn.UPE_bk = True
                            list_peer[temp_l2vpn.Peer + '/' + str(temp_l2vpn.VC_ID)] = temp_l2vpn
                        elif re.match(' shutdown\n',list_line[i]):
                            temp_vsi.Admin_status = False
                            list_line[i] = '\n'
                        i += 1
                    #temp_vsi.showdata()
                    list_l2vpn[temp_vsi.name]=temp_vsi
                    i -= 1
                i += 1
            for key in list_l2vpn:
                list_l2vpn[key].insert(cursor)
            for key in list_peer:
                #print('line 371 in get_l2vpn.py:',key, list_peer[key].showdata())
                list_peer[key].insert(cursor)
            i = 0
            while i < total_lines:
                f.write(list_line[i])
                i += 1
        else:
            print("Device is not support in this script")
        conn.commit()
    except pymysql.Error as error:
        print(error)
        for key in list_l2vpn:
            if list_l2vpn[key].vsi_id >2147483647:
                list_l2vpn[key].showdata()
    finally:
        f.close()