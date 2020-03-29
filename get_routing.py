from ospf import OSPF
from ospf_passive import OSPF_Passive
from isis_intf import  ISIS_INTF
from isis import  ISIS
from bgp import BGP
from redistribute import Redistribute
from static_route import  Static_Route
from ifl import IFL
from vrf import VRF
from vrf_ie import VRF_IE
import pymysql
import os
import re
from route_map import Route_map


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

class static_process:
    def __init__(self):
        self.Str1 =''
        self.Partition =''
        self.Check = False

    def showdata(self):
        attrs = vars(self)
        print(','.join("%s: %s" % item for item in list(attrs.items())))


def get_static_route1(str1):
    list_pattern =['ip','route','vrf','','','','','','0','tag','0','track','0']
#                    0     1      2    3  4  5  6  7  8  9    10   11    12
    result_static_route = Static_Route()
    if re.match("ip route ", str1):
        list_str=str1.split(" ")
        len_list=len(list_str)
        print(str1)
        i=0
        while i < len_list :
            if list_str[i]=='vrf':
                list_pattern[3]=list_str[i+1]
                list_pattern[4]=list_str[i+2]
                list_pattern[5] = list_str[i + 3]
                if (i+4) < len_list:
                    if validIP(list_str[i+4]):
                        list_pattern[7]= list_str[i+4]
                    elif list_str[i+4]=='Null0':
                        list_pattern[7]='Null0'
                    else:
                        list_pattern[6] = list_str[i+4]
                        if (i+5) < len_list:
                            if validIP(list_str[i+5]):
                                list_pattern[7] = list_str[i + 5]
            if list_str[i]=='tag':
                list_pattern[10] = list_str[i + 1]
                if list_str[i-1].isdigit():
                    list_pattern[8] = list_str[i-1]
                    if validIP(list_str[i - 2]):
                        list_pattern[7] = list_str[i-2]
                        if not validIP(list_str[i-3]):
                            list_pattern[7] = list_str[i - 3]
                    elif list_str[i-2]=='Null0':
                        list_pattern[7]='Null0'
                    else:
                        list_pattern[6] = list_str[i-2]
                else:
                    if validIP(list_str[i-1]):
                        list_pattern[7] = list_str[i-1]
                        if not validIP(list_str[i-2]):
                            list_pattern[7] = list_str[i - 2]
                    elif list_str[i-1]=='Null0':
                        list_pattern[7]='Null0'
                    else:
                        list_pattern[6] = list_str[i-1]
                if ((i+2) < len_list):
                    if (list_str[i+2] == 'track'):
                        list_pattern[12] = list_str[i + 3]
            if list_str[i]=='track':
                list_pattern[12] = list_str[i + 1]
            if list_str[i]=='route' and list_str[i+1]!='vrf':
                list_pattern[4] = list_str[i+1]
                list_pattern[5] = list_str[i + 2]
                if (i+3) < len_list:
                    if validIP(list_str[i+3]):
                        list_pattern[7]= list_str[i+3]
                    elif list_str[i+3]=='Null0':
                        list_pattern[7]='Null0'
                    else:
                        list_pattern[6] = list_str[i+3]
                        if (i+4)<len_list:
                            if validIP(list_str[i+4]):
                                list_pattern[7] = list_str[i + 4]

            i +=1
        result_static_route.VRF_Name = list_pattern[3]
        result_static_route.Net = list_pattern[4]+" "+list_pattern[5]
        result_static_route.Intf_name = list_pattern[6]
        result_static_route.NH = list_pattern[7]
        result_static_route.AD = int(list_pattern[8])
        result_static_route.tag = int(list_pattern[10])
        result_static_route.Track_ID = int(list_pattern[12])
    return result_static_route


def get_static_route2(str1):
    list_pattern = ['ip', 'route', 'vrf', '', '', '', '', '', '0', 'tag', '0', 'track', '0']
    #                    0     1      2    3  4    5  6    7  8      9    10   11       12
    list_str = str1.strip().split()
    result_static_route = Static_Route()
    dict_str = {}
    for item in range(len(list_str)):
        temp_partern = static_process()
        temp_partern.Str1 = list_str[item]
        temp_partern.Partition = ''
        temp_partern.Check = False
        dict_str[item] = temp_partern

    check_complete = len(list_str)
    i = 0
    while (check_complete >0) and (i<len(list_str)) :
        if not dict_str[i].Check:
            if list_str[i]=='ip':
                dict_str[i].Partition ='ip'
                dict_str[i].Check = True
            elif list_str[i]=='route':
                dict_str[i].Partition = 'route'
                dict_str[i].Check = True
                i +=1
                if list_str[i] != 'vrf':
                    list_pattern[4] = list_str[i]
                    dict_str[i].Partition = 'net'
                    dict_str[i].Check = True
                    list_pattern[5] = list_str[i+1]
                    i += 1
                    dict_str[i].Partition = 'subnet'
                    dict_str[i].Check = True
                else:
                    i -=1
            elif list_str[i] == 'vrf':
                list_pattern[3] = list_str[i + 1]
                i +=1
                dict_str[i].Partition = 'VRF_Name'
                dict_str[i].Check = True
                i +=1
                list_pattern[4] = list_str[i]
                dict_str[i].Partition = 'net'
                dict_str[i].Check = True
                i +=1
                list_pattern[5] = list_str[i]
                dict_str[i].Partition = 'subnet'
                dict_str[i].Check = True
            elif validIP(list_str[i]):
                list_pattern[7] = list_str[i]
                dict_str[i].Partition = 'NH'
                dict_str[i].Check = True
            elif list_str[i] == 'Null0':
                list_pattern[7] = 'Null0'
                dict_str[i].Partition = 'NH'
                dict_str[i].Check = True
            elif ("Ethernet" in list_str[i]) or ("Vlan" in list_str[i]) or ("Port-channel" in list_str[i]):
                list_pattern[6] = list_str[i]
                dict_str[i].Partition = 'interface'
                dict_str[i].Check = True
            elif list_str[i] == 'tag':
                dict_str[i].Check = True
                i +=1
                list_pattern[10] = int(list_str[i])
                dict_str[i].Partition = 'tag_id'
                dict_str[i].Check = True
            elif list_str[i] == 'track':
                dict_str[i].Check = True
                i += 1
                list_pattern[12] = int(list_str[i])
                dict_str[i].Partition = 'track_id'
                dict_str[i].Check = True
            else:
                if i==(len(list_str)-1):
                    list_pattern[8]=int(list_str[i])
                    dict_str[i].Partition = 'AD'
                    dict_str[i].Check = True
                elif i<(len(list_str)-1):
                    if (list_str[i+1] == 'tag') or (list_str[i+1] == 'track'):
                        list_pattern[8] = int(list_str[i])
                        dict_str[i].Partition = 'AD'
                        dict_str[i].Check = True
        i +=1
        check_complete = 0
        for item in range(len(list_str)):
            if dict_str[item].Check == False:
                check_complete += 1
    result_static_route.VRF_Name = list_pattern[3]
    result_static_route.Net = list_pattern[4] + " " + list_pattern[5]
    result_static_route.Intf_name = list_pattern[6]
    result_static_route.NH = list_pattern[7]
    result_static_route.AD = int(list_pattern[8])
    result_static_route.tag = int(list_pattern[10])
    result_static_route.Track_ID = int(list_pattern[12])
    return result_static_route


def check_vrf_ie(temp_search,temp_dict_policy_map,temp_dict_vrf_ie,temp_seq_1,temp_vrf_name):

    temp_vrf_ie = VRF_IE()
    temp_vrf_ie.Name = temp_vrf_name + '_' + str(temp_seq_1)
    temp_vrf_ie.VRF_Name = temp_vrf_name
    temp_vrf_ie.IE = 'exp'
    temp_vrf_ie.Seq = temp_seq_1
    if temp_search[0] is not None:
        temp_vrf_ie.protocol = temp_search[0]
    if temp_search[1] is not None:
        temp_vrf_ie.route_filter = temp_search[1]
    if temp_search[2] is not None:
        for key in temp_dict_policy_map:
            if re.match(temp_search[2] + '/', key):
                temp_vrf_ie.ACL = temp_dict_policy_map[key].ACL
                temp_vrf_ie.Action = temp_dict_policy_map[key].Action_1
        check_exist = False
        for key in temp_dict_vrf_ie:
            if (temp_vrf_name == temp_dict_vrf_ie[key].VRF_Name) and \
                    (temp_vrf_ie.ACL == temp_dict_vrf_ie[key].ACL) and \
                    (temp_vrf_ie.route_filter == temp_dict_vrf_ie[key].route_filter) and \
                    (temp_vrf_ie.Action == temp_dict_vrf_ie[key].Action):
                if temp_dict_vrf_ie[key].protocol!='':
                    temp_dict_vrf_ie[key].protocol = temp_dict_vrf_ie[key].protocol + ' ' + \
                                            temp_vrf_ie.protocol
                if temp_dict_vrf_ie[key].route_filter!='':
                    temp_dict_vrf_ie[key].route_filter = temp_dict_vrf_ie[key].protocol + ' ' + \
                                            temp_vrf_ie.route_filter
                check_exist = True
        if not check_exist:
            temp_dict_vrf_ie[temp_vrf_ie.Name] = temp_vrf_ie
    else:
        check_exist = False
        for key in temp_dict_vrf_ie:
            if (temp_vrf_name == temp_dict_vrf_ie[key].VRF_Name) and \
                    (temp_vrf_ie.ACL == temp_dict_vrf_ie[key].ACL) and \
                    (temp_vrf_ie.route_filter == temp_dict_vrf_ie[key].route_filter):
                if temp_dict_vrf_ie[key].protocol!='':
                    temp_dict_vrf_ie[key].protocol = temp_dict_vrf_ie[key].protocol + ' ' + \
                                            temp_vrf_ie.protocol
                if temp_dict_vrf_ie[key].route_filter!='':
                    temp_dict_vrf_ie[key].route_filter = temp_dict_vrf_ie[key].protocol + ' ' + \
                                            temp_vrf_ie.route_filter
                check_exist = True
        if not check_exist:
            temp_dict_vrf_ie[temp_vrf_ie.Name] = temp_vrf_ie

def get_routing_from_log(list_line,hostname,Dev,total_lines,log_path,conn,cursor):
    try:
        i = 0
        OSPF.Hostname = hostname
        OSPF_Passive.Hostname = hostname
        IFL.Hostname = hostname
        ISIS_INTF.Hostname = hostname
        ISIS.Hostname = hostname
        BGP.Hostname = hostname
        Redistribute.Hostname = hostname
        Static_Route.Hostname = hostname
        VRF.Hostname = hostname
        VRF_IE.Hostname = hostname
        Route_map.Hostname = hostname
        if not os.path.exists(log_path + "Logs/Routing"):
            os.mkdir(log_path + "Logs/Routing")
        with open(log_path + "Logs/Routing/" + hostname + ".txt", "w") as f:
            f.write("=========Get Routing informations of routers==========\n")
        OSPF.Hostname = hostname
        if Dev == "C76xx":
            while i < total_lines:
                if "router" == list_line[i].strip().split(" ")[0].strip():
                    if "ospf" in list_line[i]:
                        temp_ospf = OSPF()
                        temp_ospf.Name = list_line[i].strip().split(" ")[2].strip()
                        if "vrf" in list_line[i]:
                            temp_ospf.VRF_Name = list_line[i].strip().split(" ")[-1].strip()
                            temp_VRF = VRF()
                            temp_VRF.Name = temp_ospf.VRF_Name
                            temp_VRF.OSPF = True
                            temp_VRF.insert_ospf(cursor)
                        i += 1
                        while "!" not in list_line[i]:
                            if "reference-bandwidth" in list_line[i]:
                                temp_ospf.Ref_BW = int(list_line[i].strip().split(" ")[-1])
                                list_line[i] = "\n"
                            elif "redistribute" in list_line[i]:
                                temp_ospf.Redistribute = list_line[i].strip()[len('redistribute '):]
                                list_line[i] = "\n"
                            elif "default-information originate" in list_line[i]:
                                temp_ospf.DF = list_line[i].strip().split(" ")[-1]
                                if temp_ospf.DF == "":
                                    temp_ospf.DF="Y"
                                list_line[i] = "\n"
                            elif "authentication message-digest" in list_line[i]:
                                temp_ospf.Authen ="MD5"
                                list_line[i] = "\n"
                            elif list_line[i].strip()=="shutdown" :
                                temp_ospf.Admin_Status="shutdown"
                            elif "network" in list_line[i]:
                                temp_ospf_passive = OSPF_Passive()
                                pos_area=list_line[i].strip().find("area",0)
                                temp_ospf_passive.IFL = list_line[i].strip()[len('network '):pos_area]
                                temp_ospf_passive.Area = list_line[i].strip().split(" ")[-1].strip()
                                temp_ospf_passive.VRF_Name =temp_ospf.VRF_Name
                                list_line[i]="\n"
                                temp_ospf_passive.insert(cursor)
                            elif "passive" in list_line[i]:
                                temp_ospf_passive = OSPF_Passive()
                                temp_ospf_passive.IFL = list_line[i].strip().split(" ")[-1].strip()
                                temp_ospf_passive.Passive = True
                                temp_ospf_passive.VRF_Name = temp_ospf.VRF_Name
                                list_line[i]="\n"
                                temp_ospf_passive.insert(cursor)

                            i += 1
                        temp_ospf.insert(cursor)
                    elif "isis" in list_line[i]:
                        temp_isis = ISIS()
                        while "!" not in list_line[i]:
                            if "router isis" in list_line[i]:
                                temp_isis.Name = list_line[i].strip().split(" ")[-1].strip()
                            elif "net" in list_line[i]:
                                temp_isis.Net = list_line[i].strip().split(" ")[-1].strip()
                                list_line[i] = "\n"
                            elif "is-type" in list_line[i]:
                                temp_isis.Level = list_line[i].strip().split(" ")[-1].strip()
                                list_line[i] = "\n"
                            elif "authentication mode" in list_line[i]:
                                temp_isis.Authen_mode = list_line[i].strip().split(" ")[-1]
                                list_line[i] = "\n"
                            elif "key-chain" in list_line[i]:
                                temp_isis.Authen_key = list_line[i].strip().split(" ")[-1].strip()
                                list_line[i] = "\n"
                            elif "metric-style" in list_line[i]:
                                temp_isis.Metric_style = list_line[i].strip().split(" ")[-1].strip()
                                list_line[i] = "\n"
                            elif "max-lsp-lifetime" in list_line[i]:
                                temp_isis.max_lsp_lifetime = int(list_line[i].strip().split(" ")[-1].strip())
                                list_line[i] = "\n"
                            elif "lsp-refresh-interval" in list_line[i]:
                                temp_isis.lsp_refresh_interval = int(list_line[i].strip().split(" ")[-1].strip())
                                list_line[i] = "\n"
                            elif "set-overload-bit" in list_line[i]:
                                temp_isis.Overloadbit = list_line[i].strip()[17:]
                                list_line[i] = "\n"
                            elif "redistribute " in list_line[i]:
                                temp_isis.Redistribute = list_line[i].strip()[len('redistribute '):]
                                list_line[i] = "\n"
                            elif "distance " in list_line[i]:
                                temp_isis.Distance = list_line[i].strip()[len('distance '):]
                                list_line[i] = "\n"
                            elif list_line[i].strip().split(" ")[0] =="metric":
                                temp_isis.Metric = list_line[i].strip().split(" ")[-1]
                                list_line[i]="\n"
                            elif "default-information originate" in list_line[i]:
                                temp_isis.DF = list_line[i].strip().split(" ")[-1]
                                list_line[i] = "\n"
                            elif "passive-interface" in list_line[i]:
                                temp_isis_ifl = ISIS_INTF()
                                temp_isis_ifl.ISIS = temp_isis.Name
                                if "Loopback" in list_line[i].strip().split(" ")[-1]:
                                    temp_isis_ifl.IFL = "lo0."+list_line[i].strip().split(" ")[-1].strip()[len('Loopback'):]
                                elif "Vlan" in list_line[i].strip().split(" ")[-1] :
                                    temp_isis_ifl.IFL = "vlan." + list_line[i].strip().split(" ")[-1].strip()[
                                                                 len('Vlan'):]
                                else:
                                    temp_isis_ifl.IFL = list_line[i].strip().split(" ")[-1].strip() +".0"
                                temp_isis_ifl.ISIS = temp_isis.Name
                                temp_isis_ifl.VRF_Name=temp_isis.VRF_Name
                                temp_isis_ifl.Passive = True
                                temp_isis_ifl.insert_passive(cursor)
                                list_line[i] = "\n"

                            i +=1
                        temp_isis.insert(cursor)
                    elif "bgp" in list_line[i]:
                        temp_nlri= []
                        temp_AS = ""
                        temp_bgp_RID = ""
                        temp_VRF_name = ""
                        temp_peer_group=""
                        list_group = []
                        list_peer = {}
                        while "!" not in list_line[i]:
                            if "router bgp " in list_line[i]:
                                temp_AS = list_line[i].strip().split(" ")[-1].strip()
                            elif "router-id" in list_line[i]:
                                temp_bgp_RID = list_line[i].strip().split(" ")[-1].strip()
                                list_line[i] = "\n"
                            elif "bgp log-neighbor-changes" in list_line[i]:
                                BGP.BGP_log_change = True
                            if " neighbor " in list_line[i]:
                                temp_peer = list_line[i].strip().split(" ")[1].strip()
                                if temp_peer not in list(list_peer.keys()):
                                    temp_bgp = BGP()
                                    temp_bgp.Peer = temp_peer
                                    temp_bgp.Local_AS = temp_AS
                                    temp_bgp.RID = temp_bgp_RID
                                    list_peer[temp_bgp.Peer] = temp_bgp
                                if "remote-as" in list_line[i]:
                                        temp_peer = list_line[i].strip().split(" ")[1].strip()
                                        list_peer[temp_peer].Remote_AS = list_line[i].strip().split(" ")[-1].strip()
                                        list_line[i] = "\n"
                                elif "peer-group" in list_line[i]:
                                        s1 = list_line[i].strip()
                                        if len(s1)!=(s1.find("peer-group", 0) + len("peer-group")):
                                            temp_peer_group = list_line[i].strip().split(" ")[-1]
                                            temp_peer = list_line[i].strip().split(" ")[1]
                                            list_peer[temp_peer].Peer_group = temp_peer_group
                                            list_peer[temp_peer].Remote_AS = list_peer[temp_peer_group].Remote_AS
                                            list_peer[temp_peer].Update_Source = list_peer[temp_peer_group].Update_Source
                                        else:
                                            list_group.append(temp_peer)
                                        list_line[i] = "\n"
                                elif "update-source" in list_line[i]:
                                    list_peer[temp_peer].Update_Source = list_line[i].strip().split(" ")[-1].strip()
                                elif "fall-over bfd" in list_line[i]:
                                    j=0
                                    while j<total_lines:
                                        if list_line[j].strip()== 'interface ' + list_peer[temp_bgp.Peer].Update_Source :
                                            while "!" not in list_line[j]:
                                                if ' bfd interval ' in list_line[j]:
                                                    list_peer[temp_peer].BFD_interval = int(list_line[j].strip().split()[2])
                                                    list_peer[temp_peer].BFD_multiplier = int(list_line[j].strip().split()[-1])
                                                    break
                                                j +=1
                                        j +=1
                                list_line[i]="\n"
                            i += 1
                        while "vrf" not in list_line[i]:
                            if " address-family " in list_line[i] and "vrf" not in list_line:
                                s1=list_line[i].strip().split(" ")[-1]
                                temp_nlri.append(s1)
                            elif "neighbor" in list_line[i]:
                                temp_peer = list_line[i].strip().split(" ")[1].strip()
                                if temp_peer in list(list_peer.keys()):
                                    if list_peer[temp_peer].NLRI!="":
                                        list_peer[temp_peer].NLRI = list_peer[temp_peer].NLRI + " " + temp_nlri[0]
                                    else :
                                        list_peer[temp_peer].NLRI = temp_nlri[0]
                                list_line[i]="\n"
                            elif "exit-address" in list_line[i]:
                                del temp_nlri[0]
                            elif list_line[i]=="!\n":
                                break
                            i += 1
                        temp_VRF_name = ""
                        temp_nlri_vrf =""
                        while list_line[i]!="!\n":
                            if " address-family ipv4 vrf " in list_line[i]:
                                temp_VRF_name = list_line[i].strip().split(" ")[-1]
                                temp_nlri_vrf = "ipv4"
                            elif " router-id " in list_line[i]:
                                temp_bgp_RID = list_line[i].strip().split(" ")[-1].strip()
                                list_line[i] = "\n"
                            elif " redistribute " in list_line[i]:
                                temp_redistribute = Redistribute()
                                temp_redistribute.VRF_Name = temp_VRF_name
                                temp_redistribute.Type = list_line[i].strip()[len('redistribute '):]
                                temp_redistribute.insert(cursor)
                                list_line[i] = "\n"
                            elif " network " in list_line[i]:
                                temp_redistribute = Redistribute()
                                temp_redistribute.VRF_Name = temp_VRF_name
                                temp_redistribute.Type = list_line[i].strip()[len("network "):]
                                temp_redistribute.insert(cursor)
                                list_line[i] = "\n"
                            elif "neighbor" in list_line[i]:
                                temp_peer = list_line[i].strip().split(" ")[1].strip()
                                if temp_peer not in list(list_peer.keys()):
                                    temp_bgp = BGP()
                                    temp_bgp.Peer = temp_peer
                                    temp_bgp.Local_AS = temp_AS
                                    temp_bgp.RID = temp_bgp_RID
                                    temp_bgp.VRF_Name = temp_VRF_name
                                    temp_bgp.NLRI = temp_nlri_vrf
                                    temp_VRF = VRF()
                                    temp_VRF.Name = temp_bgp.VRF_Name
                                    temp_VRF.BGP = True
                                    temp_VRF.insert_bgp(cursor)
                                    list_peer[temp_bgp.Peer] = temp_bgp
                                if "remote-as" in list_line[i]:
                                    temp_peer = list_line[i].strip().split(" ")[1].strip()
                                    list_peer[temp_peer].Remote_AS = list_line[i].strip().split(" ")[-1].strip()
                                    list_line[i] = "\n"
                                elif "peer-group" in list_line[i]:
                                    s1 = list_line[i].strip()
                                    if len(s1) != (s1.find("peer-group", 0) + len("peer-group")):
                                        temp_peer_group = list_line[i].strip().split(" ")[-1].strip()
                                        temp_peer = list_line[i].strip().split(" ")[1]
                                        list_peer[temp_peer].Peer_group = temp_peer_group
                                elif "update-source" in list_line[i]:
                                    list_peer[temp_peer].Update_Source = list_line[i].strip().split(" ")[-1].strip()
                                elif "fall-over bfd" in list_line[i]:
                                    j=0
                                    while j<total_lines:
                                        if list_line[j].strip()== 'interface ' + list_peer[temp_bgp.Peer].Update_Source :
                                            while "!" not in list_line[j]:
                                                if ' bfd interval ' in list_line[j]:
                                                    list_peer[temp_peer].BFD_interval = int(list_line[j].strip().split()[2])
                                                    list_peer[temp_peer].BFD_multiplier = int(list_line[j].strip().split()[-1])
                                                    break
                                                j +=1
                                        j +=1
                                list_line[i] = "\n"
                            elif "exit-" in list_line[i]:
                                pass
                            i += 1
                        for item in list_peer:
                            if list_peer[item].Peer not in list_group:
                                list_peer[item].insert(cursor)
                elif re.match("ip route ",list_line[i].strip()):
                    while "!" not in list_line[i]:
                        temp_static = Static_Route()
                        temp_static = get_static_route2(list_line[i].strip())
                        if temp_static.VRF_Name!='':
                            temp_VRF = VRF()
                            temp_VRF.Name  = temp_static.VRF_Name
                            temp_VRF.Static_routing = True
                            temp_VRF.insert_static(cursor)
                        temp_static.insert(cursor)
                        list_line[i]="\n"
                        i +=1
                elif list_line[i]=="end\n":
                    break
                i += 1

            i = 0
            f = open(log_path + "Logs/Routing/" + hostname + ".txt", "a")
            while i<total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev == "ASR9k":
            dict_static = {}
            dict_router_isis = {}
            dict_bgp = {}
            while i < total_lines:
                if re.match('^router static\n', list_line[i]):
                    while list_line[i] != '!\n':
                        if re.match(' address-family ipv4 unicast\n',list_line[i]):
                            while list_line[i] != ' !\n':
                                if re.match('^  ((?:[\d]{0,3}[\.]){3}[\d]{0,3}[\/][\d]{1,2})[ ]?([\S]+)*[ ]?'
                                            '((?:[\d]{0,3}[\.]){3}[\d]{0,3})*\n', list_line[i]):
                                    tmp_list = re.match('^  ((?:[\d]{0,3}[\.]){3}[\d]{0,3}[\/][\d]{1,2})[ ]?'
                                                        '([\S]+)*[ ]?((?:[\d]{0,3}[\.]){3}[\d]{0,3})*\n',
                                                        list_line[i]).groups()
                                    temp_static = Static_Route()
                                    temp_static.Net = tmp_list[0]
                                    if tmp_list[1] is not None:
                                        temp_static.Intf_name = tmp_list[1]
                                        if re.match('([\d]{0,3}[\.]){3}[\d]{0,3}', tmp_list[1]):
                                            temp_static.NH = tmp_list[1]
                                    if tmp_list[2] is not None:
                                        if temp_static.NH == '':
                                            temp_static.NH = tmp_list[2]
                                    temp_static.insert(cursor)
                                    list_line[i] = '\n'
                                else:
                                    print(list_line[i])
                                i += 1
                        elif re.match('^ vrf (.*)\n',list_line[i]):
                            tmp_vrf_name = re.match('^ vrf (.*)\n',list_line[i]).groups()[0]
                            if re.match('  address-family ipv4 unicast\n', list_line[i+1]):
                                i += 1
                                while list_line[i] != '  !\n':
                                    if re.match(
                                            '^   ((?:[\d]{0,3}[\.]){3}[\d]{0,3}[\/][\d]{1,2})[ ]?([\S]+)*[ ]?(.*)\n',
                                            list_line[i]):
                                        tmp_list = re.match(
                                            '^   ((?:[\d]{0,3}[\.]){3}[\d]{0,3}[\/][\d]{1,2})[ ]?([\S]+)*[ ]?(.*)\n',
                                            list_line[i]).groups()
                                        temp_static = Static_Route()
                                        temp_static.Net = tmp_list[0]
                                        if tmp_list[1] is not None:
                                            if re.match('([\d]{0,3}[\.]){3}[\d]{0,3}', tmp_list[1]):
                                                temp_static.NH = tmp_list[1]
                                            else:
                                                if 'BVI' in tmp_list[1]:
                                                    temp_static.Intf_name = 'BVI.' + tmp_list[1][len('BVI'):]
                                                else:
                                                    temp_static.Intf_name = tmp_list[1]
                                        if tmp_list[2] is not None:
                                            if temp_static.NH == '':
                                                temp_static.NH = tmp_list[2]
                                        temp_static.VRF_Name = tmp_vrf_name
                                        temp_VRF = VRF()
                                        temp_VRF.Name = temp_static.VRF_Name
                                        temp_VRF.Static_routing = True
                                        temp_VRF.insert_static(cursor)
                                        temp_static.insert(cursor)
                                        list_line[i] = '\n'
                                    else:
                                        print(list_line[i])
                                    i += 1
                        i += 1
                elif re.match('^router isis (.*)\n',list_line[i]):
                    temp_isis = ISIS()
                    while list_line[i] != '!\n':
                        if "router isis" in list_line[i]:
                            temp_isis.Name = list_line[i].strip().split(" ")[-1].strip()
                        elif "net" in list_line[i]:
                            temp_isis.Net = list_line[i].strip().split(" ")[-1].strip()
                            list_line[i] = "\n"
                        elif "is-type" in list_line[i]:
                            temp_isis.Level = list_line[i].strip().split(" ")[-1].strip()
                            list_line[i] = "\n"
                        elif "key-chain" in list_line[i]:
                            temp_isis.Authen_key = list_line[i].strip().split(" ")[-1].strip()
                            list_line[i] = "\n"
                        elif "metric-style" in list_line[i]:
                            temp_isis.Metric_style = list_line[i].strip().split(" ")[1].strip()
                            list_line[i] = "\n"
                        elif "max-lsp-lifetime" in list_line[i]:
                            temp_isis.max_lsp_lifetime = int(list_line[i].strip().split(" ")[-1].strip())
                            list_line[i] = "\n"
                        elif "lsp-refresh-interval" in list_line[i]:
                            temp_isis.lsp_refresh_interval = int(list_line[i].strip().split(" ")[-1].strip())
                            list_line[i] = "\n"
                        elif "set-overload-bit" in list_line[i]:
                            temp_isis.Overloadbit = list_line[i].strip()[17:]
                            list_line[i] = "\n"
                        elif "redistribute " in list_line[i]:
                            temp_isis.Redistribute = list_line[i].strip()[len('redistribute '):]
                            list_line[i] = "\n"
                        elif "distance " in list_line[i]:
                            temp_isis.Distance = list_line[i].strip()[len('distance '):]
                            list_line[i] = "\n"
                        elif " interface " in list_line[i]:
                            temp_isis_ifl = ISIS_INTF()
                            temp_isis_ifl.ISIS = temp_isis.Name
                            if "Loopback" in list_line[i].strip().split(" ")[-1]:
                                temp_isis_ifl.IFL = "lo0." + list_line[i].strip().split(" ")[-1].strip()[
                                                             len('Loopback'):]
                            elif "BVI" in list_line[i].strip().split(" ")[-1]:
                                temp_isis_ifl.IFL = "BVI." + list_line[i].strip().split(" ")[-1].strip()[
                                                              len('BVI'):]
                            else:
                                if '.' not in list_line[i]:
                                    temp_isis_ifl.IFL = list_line[i].strip().split(" ")[-1].strip() + ".0"
                                else:
                                    temp_isis_ifl.IFL = list_line[i].strip().split(" ")[-1].strip()
                            temp_isis_ifl.ISIS = temp_isis.Name
                            list_line[i] = "\n"
                            while list_line[i] != ' !\n':
                                if 'passive' in list_line[i]:
                                    temp_isis_ifl.Passive = True
                                    list_line[i] = "\n"
                                i += 1
                            temp_isis_ifl.insert(cursor)
                        i += 1
                    temp_isis.insert(cursor)
                elif re.match('^router bgp (.*)\n', list_line[i]):
                    print('Processing BGP')
                    temp_nlri = []
                    temp_AS = list_line[i].strip().split()[2]
                    temp_bgp_RID = ""
                    temp_VRF_name = ""
                    temp_peer_group = ""
                    list_group = {}
                    list_peer = {}
                    while list_line[i]!='!\n':
                        if re.match(' bgp router-id (.*)\n',list_line[i]):
                            re.match(' bgp router-id (.*)\n', list_line[i]).groups()
                            temp_bgp_RID = re.match(' bgp router-id (.*)\n', list_line[i]).groups()[0]
                        elif re.match(' mpls activate\n',list_line[i]):
                            while list_line[i]!=' !\n':
                                if 'interface ' in list_line[i]:
                                    tmp_ifl_name = list_line[i].strip().split()[-1]
                                    if 'Loopback' in list_line[i]:
                                        tmp_ifl_name = 'Loopback' + '.' + tmp_ifl_name[len('Loopback'):]
                                    elif 'BVI' in list_line[i]:
                                        tmp_ifl_name = 'BVI' + '.' + tmp_ifl_name[len('BVI'):]
                                    else:
                                        tmp_ifl_name = tmp_ifl_name + '.0'
                                    temp_ifl = IFL()
                                    temp_ifl.IFD = tmp_ifl_name.split('.')[0]
                                    temp_ifl.Unit = tmp_ifl_name.split('.')[1]
                                    temp_ifl.MPLS = True
                                    list_line[i]='\n'
                                    temp_ifl.showdata()
                                    temp_ifl.update_bgp_mpls(cursor)
                                i += 1
                        elif re.match(' neighbor-group .*',list_line[i]):
                            temp_bgp_group = BGP()
                            temp_bgp_group.Peer = list_line[i].strip().split()[1]
                            temp_bgp_group.Peer_group = list_line[i].strip().split()[1]
                            temp_bgp_group.Local_AS = temp_AS
                            temp_bgp_group.RID = temp_bgp_RID
                            while list_line[i] != ' !\n':
                                if 'remote-as' in list_line[i]:
                                    temp_bgp_group.Remote_AS = list_line[i].strip().split()[1]
                                    list_line[i] = '\n'
                                elif 'update-source' in list_line[i]:
                                    tmp_ifl_name = list_line[i].strip().split()[-1]
                                    if 'Loopback' in list_line[i]:
                                        tmp_ifl_name = 'Loopback' + '.' + tmp_ifl_name[len('Loopback'):]
                                    elif 'BVI' in list_line[i]:
                                        tmp_ifl_name = 'BVI' + '.' + tmp_ifl_name[len('BVI'):]
                                    else:
                                        tmp_ifl_name = tmp_ifl_name + '.0'
                                    temp_bgp_group.Update_Source = tmp_ifl_name
                                    list_line[i] = '\n'
                                elif 'address-family vpnv4 unicast' in list_line[i]:
                                    temp_bgp_group.NLRI = 'vpnv4'
                                    list_line[i] = '\n'
                                elif 'route-reflector-client' in list_line[i]:
                                    temp_bgp_group.Cluster = True
                                    print(i)
                                    list_line[i] = '\n'
                                i += 1
                            temp_bgp_group.showdata()
                            list_group[temp_bgp_group.Peer] = temp_bgp_group
                        elif re.match(' neighbor [\S]+\n', list_line[i]):
                            if re.match('^  use neighbor-group (.*)\n', list_line[i+1]):
                                temp_group_name = re.match('^  use neighbor-group (.*)\n', list_line[i+1]).groups()[0]
                                #print 'Group name:',temp_group_name
                                #print list_line[i]
                                #print list_line[i+1]
                                ##list_group[temp_group_name].showdata()
                                temp_bgp = list_group[temp_group_name]
                                temp_bgp.Peer = list_line[i].strip().split()[-1]
                                list_line[i] = '\n'
                                list_line[i+1] = '\n'
                                i=i+1
                                #temp_bgp.showdata()
                                temp_bgp.insert(cursor)
                            else:
                                temp_bgp = BGP()
                                temp_bgp.Peer = list_line[i].strip().split()[-1]
                                temp_bgp.Local_AS = temp_AS
                                while list_line[i] !=' !\n':
                                    if 'remote-as' in list_line[i]:
                                        temp_bgp.Remote_AS = list_line[i].strip().split()[-1]
                                        list_line[i] = '\n'
                                    elif 'update-source' in list_line[i]:
                                        tmp_ifl_name = list_line[i].strip().split()[-1]
                                        if 'Loopback' in list_line[i]:
                                            tmp_ifl_name = 'Loopback' + '.' + tmp_ifl_name[len('Loopback'):]
                                        elif 'BVI' in list_line[i]:
                                            tmp_ifl_name = 'BVI' + '.' + tmp_ifl_name[len('BVI'):]
                                        else:
                                            tmp_ifl_name = tmp_ifl_name + '.0'
                                        temp_bgp.Update_Source = tmp_ifl_name
                                        list_line[i] = '\n'
                                    elif 'address-family vpnv4 unicast' in list_line[i]:
                                        temp_bgp.NLRI = 'vpnv4'
                                        list_line[i] = '\n'
                                    elif re.match('^   route-policy (.*) in\n',list_line[i]):
                                        temp_bgp.Export_policy = \
                                            re.match('^   route-policy (.*) in\n',list_line[i]).groups()[0]
                                        list_line[i] = '\n'
                                    elif re.match('^   route-policy (.*) out\n',list_line[i]):
                                        temp_bgp.Import_policy = \
                                                re.match('^   route-policy (.*) out\n', list_line[i]).groups()[0]
                                        list_line[i] = '\n'
                                    i += 1
                                temp_bgp.insert(cursor)
                                #temp_bgp.showdata()
                        elif re.match(' vrf .*',list_line[i]):
                            temp_VRF_name = list_line[i].strip().split()[-1]
                            temp_bgp = BGP()
                            print('Check VRF BGP')
                            while list_line[i]!=' !\n':
                                if " redistribute " in list_line[i]:
                                    temp_redistribute = Redistribute()
                                    temp_redistribute.VRF_Name = temp_VRF_name
                                    temp_redistribute.Type = list_line[i].strip()[len('redistribute '):]
                                    temp_redistribute.insert(cursor)
                                    list_line[i] = "\n"
                                elif re.match('^  neighbor .*\n', list_line[i]):
                                    temp_bgp = BGP()
                                    temp_bgp.Peer = list_line[i].strip().split()[1]
                                    temp_bgp.Local_AS = temp_AS
                                    temp_bgp.VRF_Name = temp_VRF_name
                                    temp_VRF = VRF()
                                    temp_VRF.Name = temp_VRF_name
                                    temp_VRF.BGP = True
                                    temp_VRF.insert_bgp(cursor)
                                    while list_line[i] !='  !\n':
                                        if 'remote-as' in list_line[i]:
                                            temp_bgp.Remote_AS = list_line[i].strip().split()[-1]
                                            list_line[i] = '\n'
                                        elif 'update-source' in list_line[i]:
                                            tmp_ifl_name = list_line[i].strip().split()[-1]
                                            if 'Loopback' in list_line[i]:
                                                tmp_ifl_name = 'Loopback' + '.' + tmp_ifl_name[len('Loopback'):]
                                            elif 'BVI' in list_line[i]:
                                                tmp_ifl_name = 'BVI' + '.' + tmp_ifl_name[len('BVI'):]
                                            else:
                                                tmp_ifl_name = tmp_ifl_name + '.0'
                                            temp_bgp.Update_Source = tmp_ifl_name
                                            list_line[i] = '\n'
                                        elif 'address-family ipv4 unicast' in list_line[i]:
                                            temp_bgp.NLRI = 'ipv4'
                                            list_line[i] = '\n'
                                        elif re.match('^    route-policy (.*) out\n',list_line[i]):
                                            temp_bgp.Export_policy = \
                                                re.match('^    route-policy (.*) out\n',list_line[i]).groups()[0]
                                            list_line[i] = '\n'
                                        elif re.match('^    route-policy (.*) in\n',list_line[i]):
                                            temp_bgp.Import_policy = \
                                                                    re.match('    route-policy (.*) in\n',
                                                                             list_line[i]).groups()[0]
                                            list_line[i] = '\n'
                                        elif 'bfd multiplier' in list_line[i]:
                                            temp_bgp.BFD_multiplier = int(list_line[i].strip().split()[-1])
                                            list_line[i] = '\n'
                                        elif 'bfd minimum-interval' in list_line[i]:
                                            temp_bgp.BFD_interval = int(list_line[i].strip().split()[-1])
                                            list_line[i] = '\n'
                                        i += 1
                                    temp_bgp.insert(cursor)
                                i += 1
                        i += 1
                i += 1
            f = open(log_path + "Logs/Routing/" + hostname + ".txt", "a")
            i = 0
            while i<total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev == 'HW':
            list_static = []
            router_isis = []
            dict_bgp = {}
            dict_vrf = {}
            dict_vrf_ie = {}
            dict_bgp_group = {}
            dict_policy_map = {}
            temp_vrf_name=''
            #print 'Test vrf'
            #for key in dict_vrf_ie:
            #    dict_vrf_ie[key].showdata()
            while i < total_lines:
                #print 'Kiem tra :',i,list_line[i]
                if re.match('[\s]?ip route-static(?: vpn-instance ([\S]*))? ((?:[\d]{1,3}[\.]){3}[\d]{1,3} '
                            '(?:[\d]{1,3}[\.]){3}[\d]{1,3})(?: ((?:Vlan|Giga|Eth)[\S]*))?(?: ((?:[\d]{1,3}[\.]){3}[\d]{1,3}))?'
                            '(?: preference ([\d]*))?(?: track bfd-session ([\S]*))?'
                            '(?: description (.*))?\n', list_line[i]):
                    temp_search = re.match('[\s]?ip route-static(?: vpn-instance ([\S]*))? ((?:[\d]{1,3}[\.]){3}[\d]{1,3} '
                            '(?:[\d]{1,3}[\.]){3}[\d]{1,3})(?: ((?:Vlan|Giga|Eth)[\S]*))?(?: ((?:[\d]{1,3}[\.]){3}[\d]{1,3}))?'
                            '(?: preference ([\d]*))?(?: track bfd-session ([\S]*))?'
                            '(?: description (.*))?\n', list_line[i]).groups()
                    temp_static = Static_Route()
                    temp_static.Net = temp_search[1]
                    if temp_search[0] is not None:
                        temp_static.VRF_Name = temp_search[0]
                    if temp_search[2] is not None:
                        temp_static.Intf_name = temp_search[2]
                    if temp_search[3] is not None:
                        temp_static.NH = temp_search[3]
                    if temp_search[4] is not None:
                        temp_static.AD = temp_search[4]
                    if temp_search[5] is not None:
                        temp_static.BFD = temp_search[5]
                    if temp_search[6] is not None:
                        temp_static.description = temp_search[6]
                    list_static.append(temp_static)
                    list_line[i] = '\n'
                elif re.match('^isis ([\S]*)\n', list_line[i]):
                    temp_isis = ISIS()
                    temp_isis.Name = re.match('^isis (.*)\n', list_line[i]).groups()[0]
                    i += 1
                    while list_line[i]!='#\n':
                        if re.match(' is-level ([\S]*)\n',list_line[i]):
                            temp_isis.Level = re.match(' is-level ([\S]*)\n',list_line[i]).groups()[0]
                            list_line[i]='\n'
                        elif re.match(' cost-style wide\n',list_line[i]):
                            temp_isis.Metric_style = 'wide'
                            list_line[i] = '\n'
                        elif re.match(' cost-style wide\n',list_line[i]):
                            temp_isis.Metric_style = 'wide'
                            list_line[i] = '\n'
                        elif re.match(' bandwidth-reference ([\d]*)\n',list_line[i]):
                            temp_isis.BW = int(re.match(' bandwidth-reference ([\d]*)\n',
                                                                  list_line[i]).groups()[0])
                            list_line[i] = '\n'
                        elif re.match(' network-entity ([\S]+)\n',list_line[i]):
                            temp_isis.Net = re.match(' network-entity ([\S]+)\n',list_line[i]).groups()[0]
                            list_line[i] = '\n'
                        elif re.match(' timer lsp-max-age ([\d]*)\n',list_line[i]):
                            temp_isis.max_lsp_lifetime = re.match(' timer lsp-max-age ([\d]*)\n',list_line[i]).groups()[0]
                            list_line[i] = '\n'
                        elif re.match(' timer lsp-refresh ([\d]*)\n',list_line[i]):
                            temp_isis.lsp_refresh_interval = int(re.match(' timer lsp-refresh ([\d]*)\n',
                                                                          list_line[i]).groups()[0])
                            list_line[i] = '\n'
                        elif re.match(' import-route (static|direct)( level-1)?\n',list_line[i]):
                            temp_search=re.match(' import-route (static|direct)( level-1)?\n',list_line[i]).groups()
                            if temp_search[0] is not None:
                                if temp_isis.Redistribute=='':
                                    temp_isis.Redistribute = temp_search[0]
                                else:
                                    temp_isis.Redistribute = temp_isis.Redistribute + '|'+ temp_search[0]
                            if temp_search[1] is not None:
                                temp_isis.Redistribute = temp_isis.Redistribute + ' ' + temp_search[1]
                            list_line[i] = '\n'
                        i += 1
                    i -= 1
                    router_isis.append(temp_isis)
                elif re.match('^bgp ([\d]*)\n', list_line[i]):
                    print('Into BGP')
                    temp_local_as = re.match('^bgp ([\d]*)\n', list_line[i]).groups()[0]
                    temp_gr = False
                    temp_nlri = ''
                    temp_vrf_name = ''
                    temp_bgp_RID = ''
                    temp_cluster = ''
                    dict_policy_map = Route_map.get_route_policy(list_line,total_lines)
                    i += 1
                    while list_line[i]!='#\n':
                        #print 'Kiem tra tai sao :', i, list_line[i]
                        if re.match(' graceful-restart\n',list_line[i]):
                            temp_gr = True
                            list_line[i]='\n'
                        elif re.match(' peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) as-number ([\d]*)\n',list_line[i]):
                            temp_search = re.match(' peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) as-number ([\d]*)\n',
                                                   list_line[i]).groups()
                            temp_bgp = BGP()
                            temp_bgp.Local_AS = temp_local_as
                            temp_bgp.GR = temp_gr
                            temp_bgp.Peer = temp_search[0]
                            temp_bgp.Remote_AS = temp_search[1]
                            temp_bgp.RID = temp_bgp_RID
                            temp_bgp.GR = temp_gr
                            dict_bgp[temp_bgp.Peer+'/'+temp_bgp.Local_AS] = temp_bgp
                            list_line[i]='\n'
                        elif re.match(' router-id ((?:[\d]{1,3}[\.]){3}[\d]{1,3})\n',list_line[i]):
                            temp_bgp_RID = re.match(' router-id ((?:[\d]{1,3}[\.]){3}[\d]{1,3})\n',
                                                    list_line[i]).groups()[0]
                            list_line[i]='\n'
                        elif re.match(' peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) description (.*)\n',list_line[i]):
                            temp_search= re.match(' peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) description (.*)\n',
                                                  list_line[i]).groups()
                            dict_bgp[temp_search[0] + '/' + temp_local_as].description = temp_search[1]
                            list_line[i] = '\n'
                        elif re.match(' peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) connect-interface (.*)\n',list_line[i]):
                            temp_search= re.match(' peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) connect-interface (.*)\n',
                                                  list_line[i]).groups()
                            dict_bgp[temp_search[0] + '/' + temp_local_as].Update_Source = temp_search[1]
                            list_line[i] = '\n'
                        elif re.match(' group ([\S]*) internal\n',list_line[i]):
                            temp_bgp_group = BGP()
                            temp_bgp_group.Peer = re.match(' group ([\S]*) internal\n', list_line[i]).groups()[0]
                            temp_bgp_group.Local_AS = temp_local_as
                            temp_bgp_group.RID = temp_bgp_RID
                            temp_bgp_group.GR = temp_gr
                            dict_bgp_group[temp_bgp_group.Peer+'/'+temp_local_as] = temp_bgp_group
                            list_line[i]='\n'
                        elif re.match(' peer ([\S]*) connect-interface ([\S]*)\n',list_line[i]):
                            temp_search = re.match(' peer ([\S]*) connect-interface ([\S]*)\n',list_line[i]).groups()
                            dict_bgp_group[temp_search[0] + '/' + temp_local_as].Peer = temp_search[0]
                            dict_bgp_group[temp_search[0] + '/' + temp_local_as].Update_Source = temp_search[1]
                            list_line[i]='\n'
                        elif re.match(' peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) group ([\S]*)\n',list_line[i]):
                            temp_search = re.match(' peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) group ([\S]*)\n',
                                                   list_line[i]).groups()
                            dict_bgp[temp_search[0] + '/' + temp_local_as].Peer_group = temp_search[1]
                            if (temp_search[1] + '/' + temp_local_as) in dict_bgp_group:
                                dict_bgp[temp_search[0] + '/' + temp_local_as].Update_Source = \
                                    dict_bgp_group[temp_search[1] + '/' + temp_local_as].Update_Source
                        elif re.match(' ipv4-family unicast\n',list_line[i]):
                            temp_nlri = 'ipv4'
                        elif re.match(' ipv4-family vpnv4\n',list_line[i]):
                            temp_nlri = 'vpnv4'
                        elif re.match('  undo peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) enable',list_line[i]):
                            list_line[i] = '\n'
                        elif re.match('  peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) enable',list_line[i]):
                            temp_search= re.match('  peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) enable',list_line[i]).groups()
                            if temp_search[0] + '/' + temp_local_as in dict_bgp:
                                if dict_bgp[temp_search[0] + '/' + temp_local_as].NLRI =='':
                                    dict_bgp[temp_search[0] + '/' + temp_local_as].NLRI = temp_nlri
                                else:
                                    dict_bgp[temp_search[0] + '/' + temp_local_as].NLRI = \
                                        dict_bgp[temp_search[0] + '/' + temp_local_as].NLRI +'|'+temp_nlri
                            else:
                                temp_bgp = BGP()
                                temp_bgp.Peer = temp_search[0]
                                temp_bgp.Local_AS = temp_local_as
                                temp_bgp.RID = temp_bgp_RID
                                temp_bgp.GR = temp_gr
                                if temp_vrf_name!='':
                                    temp_bgp.VRF_Name = temp_vrf_name
                                    temp_bgp.NLRI = 'ipv4'
                                dict_bgp[temp_bgp.Peer+'/'+temp_bgp.Local_AS]=temp_bgp
                            list_line[i] = '\n'
                        elif re.match('  reflector cluster-id ([\d]*)\n',list_line[i]):
                            temp_cluster = re.match('  reflector cluster-id ([\d]*)\n',list_line[i]).groups()[0]
                            #print 'Gia tri cluster id:',temp_cluster
                            list_line[i] = '\n'
                        elif re.match('  peer ([\S]*) enable\n',list_line[i]):
                            temp_search= re.match('  peer ([\S]*) enable\n',list_line[i]).groups()
                            if temp_search[0]+'/'+temp_local_as in dict_bgp_group:
                                dict_bgp_group[temp_search[0]+'/'+temp_local_as].NLRI = temp_nlri
                            else:
                                print('Group chua duoc khoi tao!!!')
                            list_line[i]='\n'
                        elif re.match('  peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) group ([\S]*)\n',list_line[i]):
                            temp_search = re.match('  peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) group ([\S]*)\n',
                                                   list_line[i]).groups()
                            if temp_search[0]+'/'+temp_local_as in dict_bgp:
                                dict_bgp[temp_search[0]+'/'+temp_local_as].Peer_group = temp_search[1]
                            else:
                                print('Peer chua duoc khoi tao')
                            list_line[i] = '\n'
                        elif re.match('  peer ([\S]*) reflect-client\n',list_line[i]):
                            #print 'Reflect-client',list_line[i],temp_cluster
                            temp_search = re.match('  peer ([\S]*) reflect-client\n',list_line[i]).groups()

                            if temp_search[0]+'/'+temp_local_as in dict_bgp_group:
                                #print 'Da vao day:',temp_search[0]+'/'+temp_local_as
                                dict_bgp_group[temp_search[0]+'/'+temp_local_as].Cluster = True
                                dict_bgp_group[temp_search[0] + '/' + temp_local_as].cluster_id = temp_cluster
                        elif re.match(' ipv4-family vpn-instance ([\S]*)\n',list_line[i]):
                            temp_search = re.match(' ipv4-family vpn-instance ([\S]*)\n',list_line[i]).groups()
                            #print 'BGP VPN:',temp_search
                            temp_vrf_name = temp_search[0]
                            temp_vrf = VRF()
                            temp_vrf.Name = temp_vrf_name
                            dict_vrf[temp_vrf_name] = temp_vrf
                            list_line[i]='\n'
                            i += 1
                            temp_seq = 0
                            temp_key = temp_vrf.Name + '_' + 'default_exp' + str(temp_seq)
                            while (list_line[i]!=' #\n')and(list_line[i]!='#\n'):

                                #print 'Kiem tra:',list_line[i]
                                if re.match('  (?:import-route (direct|static))?'
                                            '(?:network ((?:[\d]{1,3}[\.]){3}[\d]{1,3}(?: (?:[\d]{1,3}[\.]){3}[\d]{1,3})?))?'
                                            '(?: route-policy ([\S]*))?\n',list_line[i]):
                                    temp_search = re.match('  (?:import-route (direct|static))?'
                                                           '(?:network ((?:[\d]{1,3}[\.]){3}[\d]{1,3}(?: '
                                                           '(?:[\d]{1,3}[\.]){3}[\d]{1,3})?))?'
                                                           '(?: route-policy ([\S]*))?\n',list_line[i]).groups()
                                    #print 'Gia tri seq bat dau:',temp_seq,list_line[i]
                                    check_vrf_ie(temp_search,dict_policy_map,dict_vrf_ie,temp_seq,temp_vrf_name)
                                    temp_seq +=1
                                    #print 'Ket qua out:'
                                    #for key in dict_vrf_ie:
                                    #    dict_vrf_ie[key].showdata()
                                    list_line[i]='\n'
                                elif re.match('  default-route imported',list_line[i]):
                                    temp_search = (None,'0.0.0.0',None)
                                    check_vrf_ie(temp_search, dict_policy_map, dict_vrf_ie, temp_seq, temp_vrf_name)
                                    temp_seq += 1
                                    list_line[i] = '\n'
                                elif re.match('  auto-frr\n',list_line[i]):
                                    dict_vrf[temp_vrf_name].frr = True
                                    list_line[i]='\n'
                                elif re.match('  peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) as-number ([\d]*)\n',list_line[i]):
                                    temp_search=re.match('  peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) as-number ([\d]*)\n',
                                                         list_line[i]).groups()
                                    temp_bgp = BGP()
                                    temp_bgp.Peer = temp_search[0]
                                    temp_bgp.Remote_AS = temp_search[1]
                                    temp_bgp.Local_AS = temp_local_as
                                    temp_bgp.NLRI = 'ipv4'
                                    temp_bgp.VRF_Name = temp_vrf_name
                                    if temp_vrf_name in dict_vrf:
                                        dict_vrf[temp_vrf_name].BGP=True
                                    else:
                                        temp_vrf = VRF()
                                        temp_vrf.Name = temp_vrf_name
                                        temp_vrf.BGP = True
                                        dict_vrf[temp_vrf_name] = temp_vrf
                                    temp_bgp.BFD_multiplier = 3
                                    dict_bgp[temp_bgp.Peer+'/'+temp_bgp.Local_AS] = temp_bgp
                                    temp_search=('bgp',None,None)
                                    check_vrf_ie(temp_search, dict_policy_map, dict_vrf_ie, temp_seq, temp_vrf_name)
                                    temp_seq +=1
                                    list_line[i] = '\n'
                                elif re.match('  peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) bfd min-tx-interval ([\d]*)'
                                              ' min-rx-interval ([\d]*)\n',list_line[i]):
                                    temp_search = re.match('  peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) bfd min-tx-interval ([\d]*)'
                                              ' min-rx-interval ([\d]*)\n',list_line[i]).groups()
                                    dict_bgp[temp_search[0]+'/'+temp_local_as].BFD_interval = int(temp_search[1])
                                elif re.match('  peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) route-policy ([\S]*) import\n',
                                              list_line[i]):
                                    temp_search= re.match('  peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) route-policy ([\S]*)'
                                                          ' import\n', list_line[i]).groups()
                                    dict_bgp[temp_search[0] + '/' + temp_local_as].Import_policy = temp_search[1]
                                    list_line[i] = '\n'
                                elif re.match('  peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) route-policy ([\S]*) export\n',
                                              list_line[i]):
                                    temp_search= re.match('  peer ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) route-policy ([\S]*)'
                                                          ' export\n', list_line[i]).groups()
                                    dict_bgp[temp_search[0] + '/' + temp_local_as].Export_policy = temp_search[1]
                                    list_line[i] = '\n'
                                i += 1
                                #print 'Kiem tra %s'%i
                            i -= 1
                        i += 1
                    i -= 1
                i += 1
            print('Data policy map:')
            for key in dict_policy_map:
                dict_policy_map[key].insert(cursor)
            print('Data static route:')
            for item in list_static:
                #item.showdata()
                if item.VRF_Name!='':
                    if item.VRF_Name in dict_vrf:
                        dict_vrf[item.VRF_Name].Static_routing = True
                    else:
                        temp_vrf = VRF()
                        temp_vrf.Name = item.VRF_Name
                        temp_vrf.Static_routing = True
                        dict_vrf[item.VRF_Name] = temp_vrf
                item.insert(cursor)
            print('Update VRF Information')
            for item in dict_vrf:
                if dict_vrf[item].Static_routing == True:
                    dict_vrf[item].insert_new(cursor)
                else:
                    dict_vrf[item].insert_new1(cursor)
            print('Data isis:')
            for item in router_isis:
                item.insert(cursor)
            print('Data RR bgp')
            for item in dict_bgp_group:
                dict_bgp_group[item].insert(cursor)
            print('Data BGP')
            for item in dict_bgp:
                #dict_bgp[item].showdata()
                dict_bgp[item].insert(cursor)
            print('Data IE VRF:')
            for item in dict_vrf_ie:
               dict_vrf_ie[item].insert(cursor)
            i = 0
            f = open(log_path + "Logs/Routing/" + hostname + ".txt", "a")
            while i < total_lines:
                f.write(list_line[i])
                i += 1
        else:
            print("Device is not support in this script")
        conn.commit()
    except pymysql.Error as error:
        print(error)

    finally:
        f.close()