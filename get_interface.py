from ifd import IFD
from ifl import  IFL
from lsp import  LSP
from isis_intf import ISIS_INTF
from l2vpn import L2VPN,VSI
from vrf import VRF
from static_route import Static_Route
from netaddr import *
from policy_map import Policy_map
import pymysql
import os
import re
from policy_map import Policy_map
from bfd import BFD

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

def separate_vlan(str1):
    str_list = []
    list_str1=str1.split(',')
    for num in range(len(list_str1)):
        if list_str1[num].isdigit():
            str_list.append(list_str1[num])
        else:
            if '-' in list_str1[num]:
                str1_min = list_str1[num].split('-')[0]
                str1_max = list_str1[num].split('-')[1]
                i_min=int(str1_min)
                i_max=int(str1_max)+1
                while i_min < i_max:
                    str_list.append(str(i_min))
                    i_min +=1
    return str_list


def get_interface_from_log(list_line,hostname,Dev,total_lines,log_path, conn, cursor):
    try:
        i = 0
        IFD.Hostname = hostname
        IFL.Hostname = hostname
        LSP.Hostname = hostname
        ISIS_INTF.Hostname = hostname
        L2VPN.Hostname = hostname
        VRF.Hostname = hostname
        Policy_map.Hostname = hostname
        BFD.Hostname = hostname
        Static_Route.Hostname = hostname
        if not os.path.exists(log_path + "Logs/Interface"):
            os.mkdir(log_path + "Logs/Interface")
        with open(log_path + "Logs/Interface/" + hostname + ".txt", "w") as f:
            f.write("=========Get Interface informations of routers==========\n")
        f = open(log_path + "Logs/Interface/" + hostname + ".txt", "a")
        dict_ifd ={} #contains IFD and Junos unit
        list_ae_child =[] #contains IFD which is member of AE
        list_ifd = {}
        if Dev == "C76xx":
            pos_first_ifd = 0
            pos_end_if = 0
            ###########IFD###########
            temp_ifd = IFD()
            temp_ifd.Name = "Loopback"
            temp_ifd.MX_IFD = "lo0"
            temp_ifd.insert(cursor)
            temp_ifd = IFD()
            temp_ifd.Name = "Vlan"
            temp_ifd.MX_IFD = "irb"
            temp_ifd.insert(cursor)
            i=0
            while i < total_lines:
                if "interface" == list_line[i].strip().split(" ")[0].strip():
                    if pos_first_ifd ==0 :
                        pos_first_ifd = i
                    if ("." not in list_line[i]) and ("Vlan" not in list_line[i]) and ("Tunnel" not in list_line[i])\
                            and("Loopback" not in list_line[i]):
                        temp_ifd = IFD()
                        temp_ifd.Name = list_line[i].strip().split(" ")[1].strip()
                        dict_ifd[temp_ifd.Name] = 5000
                        if "Port-channel" in temp_ifd.Name:
                            temp_ifd.Type = "ae"
                        i += 1
                        while ("!" not in list_line[i]) and ("service instance" not in list_line[i]):
                            check_cond = False
                            if "description " in list_line[i]:
                                temp_ifd.Description = list_line[i].strip()[12:]
                            elif "dampening" in list_line[i]:
                                temp_ifd.Dampening = True
                                check_cond = True
                            elif ("mtu " in list_line[i]) and("clns" not in list_line[i]):
                                temp_ifd.MTU = int(list_line[i].strip().split(" ")[1].strip())
                            elif "channel-protocol" in list_line[i]:
                                temp_ifd.AE_type = list_line[i].strip().split(" ")[1].strip()
                                check_cond = True
                            elif "channel-group" in list_line[i]:
                                temp_ifd.AE_mode = list_line[i].strip().split(" ")[-1].strip()
                                temp_ifd.Parent_link = list_line[i].strip().split(" ")[1].strip()
                                list_ae_child.append(temp_ifd.Name)
                                list_ifd['Port-channel'+temp_ifd.Parent_link].AE_mode = temp_ifd.AE_mode
                                list_ifd['Port-channel' + temp_ifd.Parent_link].AE_type = temp_ifd.AE_type
                                check_cond = True
                            elif "service-policy output" in list_line[i]:
                                temp_ifd.Service_pol_out = list_line[i].strip().split(" ")[-1].strip()
                                check_cond = True
                            elif "media-type" in list_line[i]:
                                temp_ifd.Media_type = list_line[i].strip().split(" ")[-1].strip()
                                check_cond = True
                            elif ("shutdown" in list_line[i]) and ("no" not in list_line[i]):
                                temp_ifd.Admin_status = False
                            elif "speed" in list_line[i]:
                                temp_ifd.Speed = list_line[i].strip().split(" ")[-1].strip()
                                check_cond = True
                            elif "switchport" in list_line[i]:
                                temp_ifd.Vlan_tag = True
                                temp_ifd.Flex_service = True
                            elif "transport-mode wan" in list_line[i]:
                                temp_ifd.Wanphy = True
                                check_cond = True
                            if check_cond== True :
                                list_line[i] = "\n"
                            i += 1

                        if "service instance" in list_line[i]:
                                temp_ifd.Flex_vlan_tag = True
                                temp_ifd.Flex_service = True
                        list_ifd[temp_ifd.Name] = temp_ifd
                        #temp_ifd.insert(cursor)
                else:
                    if list_line[i].strip().split(" ")[0] == "router" and pos_end_if == 0:
                        pos_end_if = i
                i += 1
            for item in list_ifd:
                list_ifd[item].insert(cursor)
            #IFL+LSP+non-switchport
            i = pos_first_ifd
            dict_ifl = {}
            while i<pos_end_if:
                if ("interface" == list_line[i].strip().split(" ")[0].strip())and ("Tunnel" not in list_line[i]):
                    temp_ifd_name = ""
                    temp_ifl = IFL()
                    check_service = False
                    if "Loopback" in list_line[i]:
                        temp_ifl.IFD = "Loopback"
                        temp_ifl.Unit = int(list_line[i].strip().split(" ")[1][len("Loopback"):])
                        temp_ifl.Unit1 = temp_ifl.Unit
                        #temp_ifl.showdata()
                        if temp_ifl.Unit == 0 :
                            temp_ifl.Service='CORE'
                    elif "Vlan" in list_line[i]:
                        temp_ifl.IFD = "Vlan"
                        temp_ifl.Unit = int(list_line[i].strip().split(" ")[1][len("Vlan"):])
                        temp_ifl.Unit1 = temp_ifl.Unit
                    elif "." in list_line[i]:
                        temp_ifl_name = list_line[i].strip().split(" ")[1]
                        temp_ifl.IFD = temp_ifl_name.split(".")[0]
                        temp_ifl.Unit = int(temp_ifl_name.split(".")[1])
                        if temp_ifl.Unit>4094:
                            temp_ifl.Unit1 = dict_ifd[temp_ifl.IFD]
                            dict_ifd[temp_ifl.IFD] += 1
                        else:
                            temp_ifl.Unit1 = temp_ifl.Unit
                    else :
                        temp_ifd_name = list_line[i].strip().split(" ")[1]
                        temp_ifl.IFD = temp_ifd_name
                    i +=1
                    if temp_ifd_name not in list_ae_child :
                        j=i
                        while "!" not in list_line[j]:
                            if "service instance" in list_line[j]:
                                check_service=True
                                temp_ifl = IFL()
                                temp_ifl.IFD = temp_ifd_name
                                temp_ifl.Unit = int(list_line[j].strip().split(" ")[2].strip())
                                if int(temp_ifl.Unit) > 4094:
                                    temp_ifl.Unit1 = dict_ifd[temp_ifd_name]
                                    dict_ifd[temp_ifd_name] += 1
                                else:
                                    temp_ifl.Unit1 = temp_ifl.Unit
                                j += 1
                                while "!" not in list_line[j]:
                                    if "description " in list_line[j]:
                                        temp_ifl.Description = list_line[j].strip()[12:]
                                        list_line[j] = "\n"
                                    elif ("encapsulation " in list_line[j])and("xconnect" not in list_line[j]):
                                        if ("default" not in list_line[j])and("untagged" not in list_line[j]):
                                            temp_ifl.SVLAN = list_line[j].strip().split(" ")[2].strip()
                                            if "second-dot1q" in list_line[j]:
                                                temp_ifl.CVLAN = list_line[j].strip().split(" ")[-1].strip()
                                        elif "untagged" in list_line[j]:
                                            temp_ifl.SVLAN ="untagged"
                                        elif "default" in list_line[j]:
                                            temp_ifl.SVLAN = "default"
                                        list_line[j] = "\n"
                                    elif "rewrite ingress tag " in list_line[j]:
                                        temp_ifl.Vlan_mapping = list_line[j].strip().split(" ")[3].strip()
                                        temp_ifl.Vlan_translate = list_line[j].strip().split(" ")[4].strip()
                                        if ("dot1q" in list_line[j]) and ("-dot1q" not in list_line[j]):
                                            temp_ifl.Vlan_map_svlan = get_next_word(list_line[j]," dot1q ")
                                        elif ("dot1q" in list_line[j]) and("second-dot1q" in list_line[j]):
                                            temp_ifl.Vlan_map_svlan = get_next_word(list_line[j]," dot1q ")
                                            temp_ifl.Vlan_map_cvlan = get_next_word(list_line[j]," second-dot1q ")
                                        list_line[j] = "\n"
                                    elif "bridge-domain" in list_line[j]:
                                        temp_ifl.BD_ID = list_line[j].strip().split(" ")[1].strip()
                                        temp_ifl.Service = "vpls"
                                        if "split-horizon" in list_line[j]:
                                            temp_ifl.Split_horizon = True
                                        list_line[j] = "\n"
                                    elif "service-policy input" in list_line[j]:
                                        temp_ifl.Service_pol_in = list_line[j].strip().split(" ")[-1].strip()
                                        list_line[j] = "\n"
                                    elif "service-policy output" in list_line[j]:
                                        temp_ifl.Service_pol_out = list_line[j].strip().split(" ")[-1].strip()
                                        list_line[j] = "\n"
                                    elif "xconnect" in list_line[j]:
                                        #if hostname == 'R7606-ALA-UPE-01' and temp_ifd_name == 'GigabitEthernet3/12':
                                        #    print list_line[j]
                                        temp_ifl.Service = "l2circuit"
                                        temp_l2vpn = L2VPN()
                                        temp_l2vpn.VC_ID = list_line[j].strip().split(" ")[2].strip()
                                        temp_l2vpn.Peer = list_line[j].strip().split(" ")[1].strip()
                                        temp_l2vpn.IFL = temp_ifl.IFD + "." + str(temp_ifl.Unit)
                                        temp_l2vpn.insert_ifl(cursor)
                                        list_line[j] = "\n"
                                        if "backup" in list_line[j + 1]:
                                            list_line[j + 1] = "\n"
                                    j +=1
                                tmp_key = temp_ifl.IFD + '.' + str(temp_ifl.Unit)
                                if tmp_key in list(dict_ifl.keys()):
                                    temp_ifl.Unit += 100000
                                    temp_ifl.Unit1 = dict_ifd[temp_ifd_name]
                                    dict_ifd[temp_ifd_name] += 1
                                else:
                                    dict_ifl[tmp_key] = temp_ifl
                                temp_ifl.insert(cursor)
                            j += 1
                        if check_service == False:
                            j = i
                            check_stitching = 0
                            temp_vrf_name = ""
                            if temp_ifl.IFD == 'Vlan' :
                                temp_ifl.BD_ID = str(temp_ifl.Unit)
                            while "!" not in list_line[j]:
                                if ("no " not in list_line[j]) and ("ip address " in list_line[j]):
                                    temp_ifl.IP = list_line[j].strip()[11:]
                                    if temp_ifl.IFD == 'Loopback' and temp_ifl.Unit!=0:
                                        temp_ifl.Service == 'L3'
                                    check_stitching +=1
                                    list_line[j] = "\n"
                                elif ("encapsulation " in list_line[j]) and ("slip" not in list_line[j]) \
                                    and ("mpls" not in list_line[j]):
                                    if "default" not in list_line[j]:
                                        temp_ifl.SVLAN = list_line[j].strip().split(" ")[2].strip()
                                        if "second-dot1q" in list_line[j]:
                                            temp_ifl.CVLAN = list_line[j].strip().split(" ")[-1].strip()
                                    list_line[j] = "\n"
                                elif "no ip address" in list_line[j]:
                                    list_line[j] ="\n"
                                elif "ip unnumbered Loopback" in list_line[j]:
                                    temp_ifl.IP = "unnumbered lo0"
                                    list_line[j] = "\n"
                                    temp_ifl.Service = "CORE"
                                elif "ip vrf forwarding" in list_line[j]:
                                    temp_ifl.VRF_Name = list_line[j].strip().split(" ")[-1]
                                    temp_vrf_name = temp_ifl.VRF_Name
                                    temp_ifl.Service="L3VPN"
                                    list_line[j] = "\n"
                                elif "description" in list_line[j]:
                                    temp_ifl.Description = list_line[j].strip()[12:]
                                elif "service-policy output" in list_line[j]:
                                    temp_ifl.Service_pol_out = list_line[j].strip().split(" ")[-1].strip()
                                    list_line[j] = "\n"
                                elif "service-policy input" in list_line[j]:
                                    temp_ifl.Service_pol_in = list_line[j].strip().split(" ")[-1].strip()
                                    list_line[j] = "\n"
                                elif "ip router isis" in list_line[j]:
                                    temp_ifl.Routing_type = "isis"
                                    temp_isis_ifl = ISIS_INTF()
                                    temp_isis_ifl.ISIS = list_line[j].strip().split(" ")[-1].strip()
                                    temp_isis_ifl.IFL = temp_ifl.IFD + "." + str(temp_ifl.Unit)
                                    temp_isis_ifl.insert(cursor)
                                    list_line[j] ="\n"
                                elif "ip pim sparse" in list_line[j]:
                                    temp_ifl.PIM = True
                                    temp_ifl.Service = 'CORE'
                                    list_line[j] = "\n"
                                elif "ip helper-address" in list_line[j]:
                                    if temp_ifl.IP_helper !='':
                                        temp_ifl.IP_helper = temp_ifl.IP_helper + " " + list_line[j].strip().split(" ")[-1].strip()
                                    else:
                                        temp_ifl.IP_helper = list_line[j].strip().split(" ")[-1].strip()
                                    if temp_vrf_name!='':
                                        temp_vrf = VRF()
                                        temp_vrf.Name = temp_vrf_name
                                        temp_vrf.DHCP_Relay = True
                                        temp_vrf.insert_dhcp_relay(cursor)
                                    list_line[j]="\n"
                                elif "mpls ip" in list_line[j]:
                                    temp_ifl.MPLS = True
                                    temp_ifl.Service = "CORE"
                                    list_line[j] = "\n"
                                elif "isis circuit-type" in list_line[j]:
                                    temp_ifl.ISIS_circuit_type = list_line[j].strip().split(" ")[-1].strip()
                                    list_line[j] = "\n"
                                elif "isis network" in list_line[j]:
                                    temp_ifl.Routing_intf_type = list_line[j].strip().split(" ")[-1].strip()
                                    list_line[j] = "\n"
                                elif "isis metric" in list_line[j]:
                                    temp_ifl.Intf_metric = list_line[j].strip().split(" ")[-1].strip()
                                    list_line[j] = "\n"
                                elif "ip rsvp " in list_line[j]:
                                    temp_ifl.RSVP = True
                                    list_line[j] = "\n"
                                elif "clns mtu" in list_line[j]:
                                    temp_ifl.CLNS_MTU = int(list_line[j].strip().split(" ")[-1].strip())
                                    list_line[j] = "\n"
                                elif ("mtu" in list_line[j]) and("clns" not in list_line[j])and("mtu-ignore" not in list_line[j]):
                                    temp_ifl.MTU = int(list_line[j].strip().split(" ")[-1].strip())
                                    list_line[j] = "\n"
                                elif ("xconnect") in list_line[j]:
                                    check_stitching += 1
                                    if check_stitching == 2:
                                        temp_ifl.Stitching = True
                                    if "vfi" in list_line[j]:
                                        temp_ifl.BD_ID = str(temp_ifl.Unit)
                                        temp_ifl.Service = 'vpls'
                                    elif ("vfi" not in list_line[j])and(temp_ifl.IFD=="Vlan"):
                                        temp_ifl.BD_ID = str(temp_ifl.Unit)
                                        temp_ifl.Service = 'vpls'
                                    else:
                                        temp_ifl.Service='l2circuit'
                                        temp_l2vpn = L2VPN()
                                        temp_l2vpn.VC_ID = list_line[j].strip().split(" ")[2].strip()
                                        temp_l2vpn.Peer = list_line[j].strip().split(" ")[1].strip()
                                        temp_l2vpn.IFL = temp_ifl.IFD + "." + str(temp_ifl.Unit)
                                        temp_l2vpn.insert_ifl(cursor)
                                    list_line[j] = "\n"
                                    if "backup" in list_line[j+1]:
                                        list_line[j+1] ="\n"
                                elif "shutdown" == list_line[j].strip():
                                    temp_ifl.Admin_status = False
                                    list_line[j]="\n"
                                elif "switchport"==list_line[j].strip():
                                    break
                                elif "service instance" in list_line[j]:
                                    break
                                j += 1
                            if temp_ifl.IFD!="" and temp_ifl.Service!="":
                                tmp_key = temp_ifl.IFD + '.' + str(temp_ifl.Unit)
                                if tmp_key in list(dict_ifl.keys()):
                                    temp_ifl.Unit += 100000
                                    temp_ifl.Unit1 = dict_ifd[temp_ifl.IFD]
                                    dict_ifd[temp_ifl.IFD] += 1
                                else:
                                    dict_ifl[tmp_key] = temp_ifl
                                temp_ifl.insert(cursor)
                elif "Tunnel" in list_line[i]:
                    temp_lsp = LSP()
                    temp_lsp.Name = list_line[i].strip().split(" ")[-1].strip()
                    check_backup_path=False
                    i += 1
                    while "!" not in list_line[i]:
                        check_cond = False
                        if "description" in list_line[i]:
                            temp_lsp.Description = list_line[i].strip()[12:]
                            check_cond = True
                        elif "destination" in list_line[i]:
                            temp_lsp.Dest = list_line[i].strip().split(" ")[-1].strip()
                            check_cond = True
                        elif "path-option" in list_line[i]:
                            if check_backup_path == False :
                                temp_lsp.Path = list_line[i].strip().split(" ")[-1].strip()
                                check_backup_path = True
                            else:
                                temp_lsp.Backup_path = list_line[i].strip().split(" ")[-1].strip()
                            check_cond = True
                        elif list_line[i].strip()=="tunnel mode mpls traffic-eng":
                            temp_lsp.TE= True
                            check_cond= True
                        elif list_line[i].strip() =="tunnel mpls traffic-eng fast-reroute":
                            temp_lsp.FRR = True
                            check_cond = True
                        elif "ip unnumber" in list_line[i]:
                            temp_lsp.Src = list_line[i].strip().split(" ")[-1].strip()
                            check_cond = True
                        elif "source" in list_line[i]:
                            temp_lsp.Src = list_line[i].strip().split(" ")[-1].strip()
                            check_cond = True
                        elif "ip vrf forwarding" in list_line[i]:
                            temp_lsp.VRF_Name = list_line[i].strip().split(" ")[-1].strip()
                            check_cond = True
                        elif list_line[i].strip()=="shutdown":
                            temp_lsp.Admin_status = False
                            check_cond = True
                        if check_cond == True:
                            list_line[i] = "\n"
                        i += 1
                    temp_lsp.insert(cursor)
                else:
                    pass
                i += 1
            #IFL switchport
            i = pos_first_ifd
            while i<pos_end_if:
                if ("interface" == list_line[i].strip().split(" ")[0].strip()) and ("Tunnel" not in list_line[i])\
                        and ("Vlan" not in list_line[i]) and ("." not in list_line[i]) \
                        and ("Loopback" not in list_line[i]):
                    temp_ifd_name = list_line[i].strip().split(" ")[1]
                    if temp_ifd_name not in list_ae_child:
                        i +=1
                        temp_ifl_Description=""
                        temp_ifl_switchport =""
                        temp_ifl_switch_mode = ""
                        check_vlan = False
                        while "!" not in list_line[i]:
                            #print i, list_line[i]
                            if "description" in list_line[i]:
                                temp_ifl_Description = list_line[i].strip()[12:]
                                list_line[i] = "\n"
                            elif "switchport" == list_line[i].strip():
                                temp_ifl_switchport = True
                                list_line[i] = "\n"
                            elif "mtu" in list_line[i]:
                                temp_ifl_mtu = int(list_line[i].strip().split(" ")[-1])
                                list_line[i] = "\n"
                            elif ("switchport" in list_line[i]) and ("mode" in list_line[i]):
                                temp_ifl_switch_mode = list_line[i].strip().split(" ")[2]
                                list_line[i] = "\n"
                            elif ("switchport" in list_line[i]) and ("vlan" in list_line[i]):
                                check_vlan = True
                                vlan_range = list_line[i].strip().split(' ')[-1]
                                vlan_list = separate_vlan(vlan_range)
                                for num in range(len(vlan_list)):
                                    temp_ifl=IFL()
                                    temp_ifl.IFD = temp_ifd_name
                                    temp_ifl.Unit = int(vlan_list[num])
                                    temp_ifl.Unit1 = temp_ifl.Unit
                                    temp_ifl.Description = temp_ifl_Description
                                    temp_ifl.Switchport = temp_ifl_switchport
                                    temp_ifl.Switch_mode = temp_ifl_switch_mode
                                    temp_ifl.SVLAN = int(vlan_list[num])
                                    temp_ifl.Service = "vpls"
                                    temp_ifl.BD_ID = int(vlan_list[num])
                                    temp_ifl.Vlan_mapping = "pop"
                                    temp_ifl.Vlan_translate = "1"
                                    tmp_key = temp_ifl.IFD + '.' + str(temp_ifl.Unit)
                                    dict_ifl[tmp_key] = temp_ifl
                                    temp_ifl.insert(cursor)
                                list_line[i] = "\n"
                            elif "service instance" in list_line[i]:
                                break
                            i +=1
                        if (temp_ifl_switch_mode !="")and(check_vlan==False):
                            temp_ifl = IFL()
                            temp_ifl.IFD = temp_ifd_name
                            temp_ifl.Unit = 0
                            temp_ifl.Unit1 = temp_ifl.Unit
                            temp_ifl.Description = temp_ifl_Description
                            temp_ifl.Switchport = temp_ifl_switchport
                            temp_ifl.Switch_mode = temp_ifl_switch_mode
                            temp_ifl.SVLAN = 1
                            temp_ifl.Service='NA'
                            tmp_key = temp_ifl.IFD + '.' + str(temp_ifl.Unit)
                            if tmp_key in list(dict_ifl.keys()):
                                temp_ifl.Unit += 100000
                                temp_ifl.Unit1 = dict_ifd[temp_ifd_name]
                                dict_ifd[temp_ifd_name] += 1
                            else:
                                dict_ifl[tmp_key] = temp_ifl
                            temp_ifl.insert(cursor)
                i += 1
            i = 0
            while i<total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev == "ASR9k":
            dict_ifd = {}
            dict_ifl = {}
            ###########IFD###########
            temp_ifd = IFD()
            temp_ifd.Name = "Loopback"
            temp_ifd.MX_IFD = "lo0"
            list_ifd[temp_ifd.Name] = temp_ifd
            temp_ifd = IFD()
            temp_ifd.Name = "BVI"
            temp_ifd.MX_IFD = "irb"
            list_ifd[temp_ifd.Name] = temp_ifd
            i = 0
            while i < total_lines:
                if re.match('interface ((Bundle|TenGi|Gi)[\w\/\-\d]*[^\.][\/\d]*)\n', list_line[i]):
                    tmp_result = re.match('interface ((?:Bundle|TenGi|Gi)[\S]+)\n', list_line[i])
                    #print tmp_result.groups()
                    temp_ifd = IFD()
                    while list_line[i] != '!\n':
                        if re.match('^interface .*',list_line[i]):
                            temp_ifd.Name = tmp_result.groups()[0]
                            dict_ifd[temp_ifd.Name] = 5000
                            if 'Bundle-' in temp_ifd.Name:
                                temp_ifd.Type = 'ae'
                        elif re.match('^ description (.*)\n',list_line[i]):
                            temp_ifd.Description = re.match('^ description (.*)\n',list_line[i]).groups()[0]
                        elif re.match('^ mtu ([\d]+)\n',list_line[i]):
                            temp_ifd.MTU = re.match('^ mtu ([\d]+)\n',list_line[i]).groups()[0]
                        elif re.match('^ bundle id ([\d]+) mode (.*)\n',list_line[i]):
                            tmp_str = re.match('^ bundle id ([\d]+) mode (.*)\n',list_line[i])
                            #print 'Gia tri bundle-id :', tmp_str.groups()
                            temp_ifd.Parent_link = tmp_str.groups()[0]
                            temp_ifd.AE_mode = tmp_str.groups()[1]
                            list_ae_child.append(temp_ifd.Name)
                            if temp_ifd.AE_mode =='active':
                                temp_ifd.AE_type = 'lacp'
                            list_ifd['Bundle-Ether' + temp_ifd.Parent_link].AE_mode = temp_ifd.AE_mode
                            list_ifd['Bundle-Ether' + temp_ifd.Parent_link].AE_type = temp_ifd.AE_type
                        elif re.match('^ dampening\n',list_line[i]):
                            temp_ifd.Dampening = True
                        elif re.match('^ service-policy output (.*)\n',list_line[i]):
                            temp_ifd.Service_pol_out = re.match('^ service-policy output (.*)\n',list_line[i]).groups()[0]
                        elif re.match('^ shutdown\n', list_line[i]):
                            temp_ifd.Admin_status = False
                        i += 1
                    if temp_ifd.Name in list_line[i+1]:
                        temp_ifd.Flex_service = True
                        temp_ifd.Flex_vlan_tag = True
                    list_ifd[temp_ifd.Name] = temp_ifd
                i += 1
            i = 0
            while i < total_lines:
                if re.match('interface ((?:Bundle|TenGi|Gi|BVI|Loopback)[\w\/\-\d]*[\.]*[\d]*)(?: (.*))*\n', list_line[i]):
                    tmp_result = re.match('interface (((?:Bundle|TenGi|Gi|BVI|Loopback)[\w\/\-\d]*)[\.]*([\d]*))'
                                          '(?: (.*))*\n', list_line[i])
                    tmp_str = tmp_result.groups()[1]
                    if 'Loopback' in tmp_str:
                        tmp_str = 'Loopback'
                    elif 'BVI' in tmp_str:
                        tmp_str = 'BVI'
                    if list_ifd[tmp_str].Parent_link == '':
                        temp_ifl = IFL()
                        temp_ifl_name = ''
                        while list_line[i] != '!\n':
                            if 'interface ' in list_line[i]:
                                if 'Loopback' in list_line[i]:
                                    temp_ifl.IFD = 'Loopback'
                                    temp_ifl.Unit = int(list_line[i].strip().split()[-1][len('Loopback'):])
                                    temp_ifl.Unit1 = temp_ifl.Unit
                                elif 'BVI' in list_line[i]:
                                    temp_ifl.IFD = 'BVI'
                                    temp_ifl.Unit = int(list_line[i].strip().split()[-1][len('BVI'):])
                                    temp_ifl.Unit1 = temp_ifl.Unit
                                elif '.' not in list_line[i]:
                                    temp_ifl.IFD = tmp_result.groups()[1]
                                    temp_ifl.Unit, temp_ifl.Unit1 = 0, 0
                                    temp_ifl_name = temp_ifl.IFD + '.' + str(temp_ifl.Unit)
                                elif '.' in list_line[i]:
                                    temp_ifl.IFD = tmp_result.groups()[1]
                                    temp_ifl.Unit = int(tmp_result.groups()[2])
                                    if temp_ifl.Unit > 4095:
                                        temp_ifl.Unit1 = dict_ifd[temp_ifl.IFD]
                                        dict_ifd[temp_ifl.IFD] += 1
                                    else:
                                        temp_ifl.Unit1 = temp_ifl.Unit
                                temp_ifl_name = temp_ifl.IFD + '.' + str(temp_ifl.Unit)
                                dict_ifl[temp_ifl_name] = temp_ifl
                            elif re.match('^ description (.*)\n',list_line[i]):
                                dict_ifl[temp_ifl_name].Description = re.match('^ description (.*)\n',
                                                                               list_line[i]).groups()[0]
                                list_line[i] = "\n"
                            elif re.match('^ vrf .*\n',list_line[i]):
                                dict_ifl[temp_ifl_name].VRF_Name = list_line[i].strip().split()[-1]
                                dict_ifl[temp_ifl_name].Service = 'L3VPN'
                                list_line[i] = "\n"
                            elif re.match('^ ipv4 address (.*)\n',list_line[i]):
                                if dict_ifl[temp_ifl_name].IP =='':
                                    dict_ifl[temp_ifl_name].IP = re.match('^ ipv4 address (.*)\n',
                                                                      list_line[i]).groups()[0]
                                else:
                                    dict_ifl[temp_ifl_name].IP = dict_ifl[temp_ifl_name].IP + '/' + \
                                                                 re.match('^ ipv4 address (.*)\n',
                                                                          list_line[i]).groups()[0]

                                if dict_ifl[temp_ifl_name].VRF_Name == '':
                                    dict_ifl[temp_ifl_name].Service = 'L3'
                                list_line[i] = "\n"
                            elif re.match('^ encapsulation dot1q (.*)\n',list_line[i]):
                                #print list_line[i]
                                #print re.match('^ encapsulation dot1q (.*)',list_line[i]).groups()[0]
                                dict_ifl[temp_ifl_name].SVLAN = re.match('^ encapsulation dot1q (.*)\n', list_line[i]).groups()[0]
                                list_line[i] = "\n"
                            elif re.match('^ rewrite ingress tag .*',list_line[i]):
                                dict_ifl[temp_ifl_name].Vlan_mapping = list_line[i].strip().split(" ")[3].strip()
                                dict_ifl[temp_ifl_name].Vlan_translate = list_line[i].strip().split(" ")[4].strip()
                                if ("dot1q" in list_line[i]) and ("-dot1q" not in list_line[i]):
                                    dict_ifl[temp_ifl_name].Vlan_map_svlan = get_next_word(list_line[i], " dot1q ")
                                elif ("dot1q" in list_line[i]) and ("second-dot1q" in list_line[i]):
                                    dict_ifl[temp_ifl_name].Vlan_map_svlan = get_next_word(list_line[i], " dot1q ")
                                    dict_ifl[temp_ifl_name].Vlan_map_cvlan = get_next_word(list_line[i], " second-dot1q ")
                                list_line[i] = "\n"
                            elif re.match('^ service-policy output (.*)\n', list_line[i]):
                                dict_ifl[temp_ifl_name].Service_pol_out = \
                                     re.match('^ service-policy output (.*)\n', list_line[i]).groups()[0]
                                #dict_ifl[temp_ifl_name].showdata()
                                list_line[i] = "\n"

                            elif re.match('^ service-policy input (.*)\n', list_line[i]):
                                dict_ifl[temp_ifl_name].Service_pol_in = \
                                    re.match('^ service-policy input (.*)\n', list_line[i]).groups()[0]
                                list_line[i] = "\n"
                            elif re.match('^ mtu (.*)\n', list_line[i]):
                                dict_ifl[temp_ifl_name].MTU = int(re.match('^ mtu (.*)\n',list_line[i]).groups()[0])
                                list_line[i] = "\n"
                            elif re.match(' ipv4 access-group (.*) ingress\n', list_line[i]):
                                dict_ifl[temp_ifl_name].FF_in = re.match(' ipv4 access-group (.*) ingress\n', list_line[i]).groups()[0]
                                list_line[i] = "\n"
                            elif re.match(' shutdown\n',list_line[i]):
                                dict_ifl[temp_ifl_name].Admin_status = False
                                list_line[i] = "\n"
                            i += 1
                i += 1

            i = 0
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
            i = pos_1
            while i < pos_2:
                if re.match('^   interface ([\S]+)\n', list_line[i]):
                    temp_ifl_name = re.match('^   interface ([\S]+)\n', list_line[i]).groups()[0]
                    if temp_ifl_name in dict_ifl:
                        dict_ifl[temp_ifl_name].Service = 'l2circuit'
                        list_line[i] = '\n'
                i += 1
            i = pos_2
            tmp_bd = ''
            while i < pos_3:
                if re.match('^  bridge-domain .*\n', list_line[i]):
                    tmp_bd = re.match('^  bridge-domain (.*)\n', list_line[i]).groups()[0]
                    while list_line[i] != '  !\n':
                        if ' interface ' in list_line[i]:
                            temp_ifl_name = list_line[i].strip().split()[-1]
                            if 'BVI' in temp_ifl_name:
                                temp_ifl_name = 'BVI' + '.' + temp_ifl_name[len('BVI'):]
                            if temp_ifl_name in dict_ifl:
                                if dict_ifl[temp_ifl_name].IP!='':
                                    dict_ifl[temp_ifl_name].Stitching = True
                                    dict_ifl[temp_ifl_name].Service = 'l3/vpls'
                                else:
                                    dict_ifl[temp_ifl_name].Service = 'vpls'
                                dict_ifl[temp_ifl_name].BD_ID = tmp_bd
                                if 'split-horizon' in list_line[i+1]:
                                    dict_ifl[temp_ifl_name].Split_horizon = True
                                list_line[i] = '\n'
                            else:
                                print(hostname, temp_ifl_name)
                        i += 1
                i += 1
            print('Bat dau check ISIS')
            i = 0
            while i < total_lines:
                if re.match('^router isis .*\n', list_line[i]):
                    tmp_ifl_name = ''
                    while list_line[i] != '!\n':
                        if 'interface ' in list_line[i]:
                            if re.match('^ interface .*\n', list_line[i]) and ('.' in list_line[i]):
                                tmp_ifl_name = list_line[i].strip().split()[-1]
                            elif re.match('^ interface .*\n', list_line[i]) and ('.' not in list_line[i]):
                                tmp_ifl_name = list_line[i].strip().split()[-1]
                                if 'Loopback' in list_line[i]:
                                    tmp_ifl_name = 'Loopback' + '.' + tmp_ifl_name[len('Loopback'):]
                                elif 'BVI' in list_line[i]:
                                    tmp_ifl_name = 'BVI' + '.' + tmp_ifl_name[len('BVI'):]
                                else:
                                    tmp_ifl_name = tmp_ifl_name + '.0'
                            if (tmp_ifl_name!='')and(tmp_ifl_name in dict_ifl):
                                dict_ifl[tmp_ifl_name].Service = 'CORE'
                                dict_ifl[tmp_ifl_name].Routing_type = 'isis'
                                while list_line[i] != ' !\n':
                                    if 'circuit-type ' in list_line[i]:
                                        dict_ifl[tmp_ifl_name].ISIS_circuit_type = list_line[i].strip().split()[-1]
                                        list_line[i] = '\n'
                                    elif 'point-to-point' in list_line[i]:
                                        dict_ifl[tmp_ifl_name].Routing_intf_type = 'point-to-point'
                                        list_line[i] = '\n'
                                    elif ' metric ' in list_line[i]:
                                        dict_ifl[tmp_ifl_name].Intf_metric = list_line[i].strip().split()[1]
                                        list_line[i] = '\n'
                                    i += 1
                        i += 1
                    break
                i +=1
            i = 0
            print('Bat dau check RSVP')
            while i < total_lines:
                if re.match('rsvp', list_line[i]):
                    while list_line[i] != '!\n':
                        if re.match('^ interface ', list_line[i]) and ('.' in list_line[i]):
                            tmp_ifl_name = list_line[i].strip().split()[-1]
                        elif re.match('^ interface ', list_line[i]) and ('.' not in list_line[i]):
                            tmp_ifl_name = list_line[i].strip().split()[-1]
                            if 'Loopback' in list_line[i]:
                                tmp_ifl_name = 'Loopback' + '.' + tmp_ifl_name[len('Loopback'):]
                            elif 'BVI' in list_line[i]:
                                tmp_ifl_name = 'BVI' + '.' + tmp_ifl_name[len('BVI'):]
                            else:
                                tmp_ifl_name = tmp_ifl_name + '.0'
                            if tmp_ifl_name in dict_ifl:
                                if 'bandwidth' in list_line[i+1]:
                                    dict_ifl[tmp_ifl_name].RSVP = True
                                    list_line[i] = '\n'
                                    list_line[i+1] = '\n'
                        i += 1
                    break
                i += 1
            tmp_ifl_name = ''
            print('Bat dau check MPLS')
            i = 0
            while i < total_lines:
                if re.match('^mpls traffic-eng\n', list_line[i]):
                    while list_line[i] != '!\n':
                        if re.match('^ interface .*\n', list_line[i]) and ('.' in list_line[i]):
                            tmp_ifl_name = list_line[i].strip().split()[-1]
                        elif re.match('^ interface .*\n', list_line[i]) and ('.' not in list_line[i]):
                            tmp_ifl_name = list_line[i].strip().split()[-1]
                            if 'Loopback' in list_line[i]:
                                tmp_ifl_name = 'Loopback' + '.' + tmp_ifl_name[len('Loopback'):]
                            elif 'BVI' in list_line[i]:
                                tmp_ifl_name = 'BVI' + '.' + tmp_ifl_name[len('BVI'):]
                            else:
                                tmp_ifl_name = tmp_ifl_name + '.0'
                            if tmp_ifl_name in dict_ifl:
                                dict_ifl[tmp_ifl_name].MPLS = True
                                list_line[i] = '\n'
                                if re.match('^  backup-path (.*)\n', list_line[i+1]):
                                    dict_ifl[tmp_ifl_name].Backup_path = \
                                        re.match('^  backup-path (.*)\n', list_line[i+1]).groups()[0]
                                    list_line[i+1] = '\n'
                        i += 1
                    break
                i += 1
            print('Bat dau check LDP')
            i= 0
            while i < total_lines:
                if re.match('^mpls ldp\n', list_line[i]):
                    while list_line[i] != '!\n':
                        if re.match('^ interface .*\n', list_line[i]) and ('tunnel' not in list_line[i]):
                            tmp_ifl_name = list_line[i].strip().split()[-1]
                            if '.' not in tmp_ifl_name:
                                tmp_ifl_name = tmp_ifl_name + '.0'
                            if tmp_ifl_name in dict_ifl:
                                dict_ifl[tmp_ifl_name].MPLS = True
                                list_line[i] = '\n'
                        i += 1
                    break
                i += 1
            print('Bat dau check pim')
            i=0
            while i < total_lines:
                if re.match('^router pim\n', list_line[i]):
                    while list_line[i] != '!\n':
                        if re.match('^  interface ', list_line[i]) and ('.' in list_line[i]):
                            tmp_ifl_name = list_line[i].strip().split()[-1]
                        elif re.match('^  interface ', list_line[i]) and ('.' not in list_line[i]):
                            tmp_ifl_name = list_line[i].strip().split()[-1]
                            if 'Loopback' in list_line[i]:
                                tmp_ifl_name = 'Loopback' + '.' + tmp_ifl_name[len('Loopback'):]
                            elif 'BVI' in list_line[i]:
                                tmp_ifl_name = 'BVI' + '.' + tmp_ifl_name[len('BVI'):]
                            else:
                                tmp_ifl_name = tmp_ifl_name + '.0'
                            if tmp_ifl_name in dict_ifl:
                                if 'enable' in list_line[i+1]:
                                    dict_ifl[tmp_ifl_name].PIM = True
                                    list_line[i] = '\n'
                                    list_line[i+1] = '\n'
                        i += 1
                    break
                i += 1
            dict_lsp = {}
            i = 0
            print('Bat dau check LSP')
            while i < total_lines:
                if re.match('interface tunnel-.*\n', list_line[i]):
                    temp_lsp = LSP()
                    temp_lsp.Name = list_line[i].strip().split()[-1].strip()
                    check_backup_path = False
                    i += 1
                    while list_line[i] !='!\n':
                        check_cond = False
                        if "description" in list_line[i]:
                            temp_lsp.Description = list_line[i].strip()[12:]
                            check_cond = True
                        elif "destination" in list_line[i]:
                            temp_lsp.Dest = list_line[i].strip().split(" ")[-1].strip()
                            check_cond = True
                        elif "path-option" in list_line[i]:
                            if check_backup_path == False:
                                temp_lsp.Path = list_line[i].strip().split(" ")[-1].strip()
                                check_backup_path = True
                            else:
                                temp_lsp.Backup_path = list_line[i].strip().split(" ")[-1].strip()
                            check_cond = True
                        elif list_line[i].strip() == "tunnel mode mpls traffic-eng":
                            temp_lsp.TE = True
                            check_cond = True
                        elif 'fast-reroute' in list_line[i].strip():
                            temp_lsp.FRR = True
                            check_cond = True
                        elif "ipv4 unnumber" in list_line[i]:
                            temp_lsp.Src = list_line[i].strip().split(" ")[-1].strip()
                            check_cond = True
                        elif "source" in list_line[i]:
                            temp_lsp.Src = list_line[i].strip().split(" ")[-1].strip()
                            check_cond = True
                        elif "ip vrf forwarding" in list_line[i]:
                            temp_lsp.VRF_Name = list_line[i].strip().split(" ")[-1].strip()
                            check_cond = True
                        elif list_line[i].strip() == "shutdown":
                            temp_lsp.Admin_status = False
                            check_cond = True
                        elif 'metric absolute' in list_line[i]:
                            temp_lsp.Metric = int(list_line[i].strip().split(" ")[-1].strip())
                            check_cond = True
                        if check_cond == True:
                            list_line[i] = "\n"
                        i += 1
                    dict_lsp[temp_lsp.Name] = temp_lsp
                i += 1
            for key in list_ifd:
                list_ifd[key].insert(cursor)
            for key in dict_ifl:
                #if dict_ifl[key].Hostname == 'ASR9912-GDI-P-01':
                #    dict_ifl[key].showdata()
                if dict_ifl[key].Service != '':
                    dict_ifl[key].insert(cursor)
            for key in dict_lsp:
                dict_lsp[key].insert(cursor)
            i = 0
            while i < total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev == 'HW':
            sql = "select Name,Encap,Isolate,Classifier from vsi where Hostname='%s'" % hostname
            cursor.execute(sql)
            list_vsi = cursor.fetchall()
            dict_vsi = {}
            dict_static_route = {}
            for item in list_vsi:
                temp_vsi = VSI()
                temp_vsi.name = item[0]
                temp_vsi.encap = item[1]
                temp_vsi.isolate = item[2]
                temp_vsi.classifier = item[3]
                dict_vsi[temp_vsi.name] = temp_vsi
            sql = "select Name,Classifier from vrf where Hostname='%s'" % hostname
            cursor.execute(sql)
            list_vrf = cursor.fetchall()
            dict_vrf = {}
            for item in list_vrf:
                temp_vrf = VRF()
                temp_vrf.name = item[0]
                temp_vrf.classifier = item[1]
                dict_vrf[temp_vrf.name] = temp_vrf
            sql = "select Name from policy_map " \
                  "where Hostname = '%s' and ( ACL='' or ACL='any') and CIR > 0 group by Name" % hostname
            cursor.execute(sql)
            list_rows = cursor.fetchall()
            list_policer = list([x[0].decode() for x in list_rows])
            dict_ifl = {} #chua ifl information
            dict_policy_map = {} #chua policy map tren interface truc tiep
            dict_l2vpn = {} #chua l2
            dict_lsp = {} #chua lsp
            dict_bfd = {} #chua bfd info

             ###########IFD###########
            temp_ifd = IFD()
            temp_ifd.Name = "LoopBack"
            temp_ifd.MX_IFD = "lo0"
            list_ifd[temp_ifd.Name] = temp_ifd
            temp_ifd = IFD()
            temp_ifd.Name = "Vlanif"
            temp_ifd.MX_IFD = "irb"
            list_ifd[temp_ifd.Name] = temp_ifd
            while i < total_lines:
                if re.match('interface ((?:Eth-Trunk|GigabitEthernet|100GE)[\d]{1,}[^\.]?(?:\/[\d]{1,}){0,2})\n', list_line[i]):
                    tmp_result = re.match('interface ((?:Eth-Trunk|GigabitEthernet|100GE)[\d]{1,}[^\.]?(?:\/[\d]{1,}){0,2})\n', list_line[i]).groups()
                    #print tmp_result.groups()
                    temp_ifd = IFD()
                    while list_line[i] != '#\n':
                        if re.match('^interface .*\n',list_line[i]):
                            temp_ifd.Name = tmp_result[0]
                            list_ifd[temp_ifd.Name] = temp_ifd
                            dict_ifd[temp_ifd.Name] = 5000
                            if 'Eth-Trunk' in temp_ifd.Name:
                                temp_ifd.Type = 'ae'
                        elif re.match(' set transfer-mode wan\n', list_line[i]):
                            temp_ifd.Wanphy = True
                            list_line[i] = "\n"
                        elif re.match('^ description (.*)\n', list_line[i]):
                            temp_ifd.Description = re.match('^ description (.*)\n',list_line[i]).groups()[0]
                        elif re.match('^ mtu ([\d]+)\n',list_line[i]):
                            temp_ifd.MTU = re.match('^ mtu ([\d]+)\n',list_line[i]).groups()[0]
                        elif re.match(' negotiation auto\n',list_line[i]):
                            temp_ifd.Speed = 'auto'
                            list_line[i] = "\n"
                        elif re.match('^ eth-trunk ([\d]+)\n',list_line[i]):
                            tmp_str = re.match('^ eth-trunk ([\d]+)\n',list_line[i])
                            #print 'Gia tri bundle-id :', tmp_str.groups()
                            temp_ifd.Parent_link = tmp_str.groups()[0]
                            list_ae_child.append(temp_ifd.Name)
                            temp_ifd.AE_mode = list_ifd['Eth-Trunk' + temp_ifd.Parent_link].AE_mode
                            temp_ifd.AE_type = list_ifd['Eth-Trunk' + temp_ifd.Parent_link].AE_type
                            list_line[i] = "\n"
                        elif re.match(' distribute-weight ([\d]*)\n',list_line[i]):
                            temp_ifd.weight = int(re.match(' distribute-weight ([\d]*)\n',list_line[i]).groups()[0])
                            list_line[i] = "\n"
                        elif re.match(' port default vlan (.*)\n',list_line[i]):
                            temp_ifd.native_vlan = re.match(' port default vlan (.*)\n',list_line[i]).groups()[0]
                        elif 'mode lacp-static' in list_line[i]:

                            temp_ifd.AE_type = 'lacp'
                            temp_ifd.AE_mode = 'active'
                            #print 'Matching lacp', temp_ifd.showdata()
                            #list_line[i] = "\n"
                        elif re.match('^ shutdown\n', list_line[i]):
                            temp_ifd.Admin_status = False
                        i += 1
                    list_ifd[temp_ifd.Name] = temp_ifd
                    #temp_ifd.showdata()
                    i -= 1
                i += 1
            i = 0
            while i < total_lines:
                if re.match('interface ((?:Eth-Trunk|GigabitEthernet|100GE|LoopBack|Vlanif)[\d]{1,}(?:\/[\d]{1,}){0,2})[\.]?([\d]*)\n',
                            list_line[i]):
                    print(list_line[i])
                    if list_line[i+1]!='#\n':
                        tmp_result = re.match('interface ((?:Eth-Trunk|GigabitEthernet|100GE|LoopBack|Vlanif)[\d]{1,}(?:\/[\d]{1,}){0,2})[\.]?([\d]*)\n',
                                list_line[i])
                        tmp_str = tmp_result.groups()[0]

                        if 'LoopBack' in tmp_str:
                            tmp_str = 'LoopBack'
                        elif 'Vlanif' in tmp_str:
                            tmp_str = 'Vlanif'
                        if list_ifd[tmp_str].Parent_link == '':
                            temp_ifl = IFL()
                            temp_ifl_name = ''
                            temp_ifd_name = ''
                            temp_vlan_list = []
                            while list_line[i]!= '#\n':
                                if re.match('interface .*\n',list_line[i]):
                                    if 'LoopBack' in list_line[i]:
                                        temp_ifl.IFD = 'LoopBack'
                                        temp_ifl.Unit = int(list_line[i].strip().split()[-1][len('LoopBack'):])
                                        temp_ifl.Unit1 = temp_ifl.Unit
                                    elif 'Vlanif' in list_line[i]:
                                        temp_ifl.IFD = 'Vlanif'
                                        temp_ifl.Unit = int(list_line[i].strip().split()[-1][len('Vlanif'):])
                                        temp_ifl.Unit1 = temp_ifl.Unit
                                        temp_ifl.BD_ID = 'VLAN-'+str(temp_ifl.Unit)
                                    elif '.' not in list_line[i]:
                                        temp_ifl.IFD = tmp_result.groups()[0]
                                        temp_ifd_name = tmp_result.groups()[0]
                                        temp_ifl.Unit, temp_ifl.Unit1 = 0, 0
                                    elif '.' in list_line[i]:
                                        temp_ifl.IFD = tmp_result.groups()[0]
                                        temp_ifd_name = tmp_result.groups()[0]
                                        temp_ifl.Unit = int(tmp_result.groups()[1])
                                        if temp_ifl.Unit > 4095:
                                            #print 'Unit1', dict_ifd[temp_ifl.IFD]
                                            #print 'Check type dict_ifd', dict_ifd[temp_ifl.IFD]
                                            temp_ifl.Unit1 = dict_ifd[temp_ifl.IFD]
                                            dict_ifd[temp_ifl.IFD] += 1
                                        else:
                                            if temp_ifl.IFD + '.' + str(temp_ifl.Unit) in dict_ifl:
                                                temp_ifl.Unit = dict_ifd[temp_ifl.IFD]
                                                dict_ifd[temp_ifl.IFD] += 1
                                            temp_ifl.Unit1 = temp_ifl.Unit
                                    temp_ifl_name = temp_ifl.IFD + '.' + str(temp_ifl.Unit)
                                    dict_ifl[temp_ifl_name] = temp_ifl
                                elif re.match('^ description (.*)\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].Description = re.match('^ description (.*)\n',
                                                                                   list_line[i]).groups()[0]
                                    list_line[i] = "\n"
                                elif re.match('^ ip address (.*)\n',list_line[i]):
                                    if dict_ifl[temp_ifl_name].IP=='':
                                        dict_ifl[temp_ifl_name].IP = re.match('^ ip address (.*)\n',
                                                                          list_line[i]).groups()[0]
                                    else:
                                        dict_ifl[temp_ifl_name].IP = dict_ifl[temp_ifl_name].IP +'/'+ re.match('^ ip address (.*)\n',
                                                                          list_line[i]).groups()[0]
                                    if dict_ifl[temp_ifl_name].VRF_Name == '':
                                        dict_ifl[temp_ifl_name].Service = 'L3'
                                    list_line[i] = "\n"
                                elif re.match('^ vlan-type dot1q ([\d]+)( vlan-group ([\d]+))?\n',list_line[i]):
                                    temp_search=re.match('^ vlan-type dot1q ([\d]+)(?: vlan-group ([\d]+))?\n', list_line[i]).groups()
                                    dict_ifl[temp_ifl_name].SVLAN = temp_search[0]
                                    dict_ifl[temp_ifl_name].Vlan_mapping = 'pop'
                                    dict_ifl[temp_ifl_name].Vlan_translate = '1'
                                    if temp_search[1] is not None:
                                        if (temp_ifl_name + '/' + temp_search[1] + '_in') in dict_policy_map:
                                            dict_ifl[temp_ifl_name].Service_pol_in = \
                                                dict_policy_map[temp_ifl_name + '/' + temp_search[1] + '_in'].Name
                                        if (temp_ifl_name + '/' + temp_search[1] + '_out') in dict_policy_map:
                                            #print 'Gia tri policy:',dict_policy_map[temp_ifd_name + '/' + temp_search[2] + '_out'].Name
                                            dict_ifl[temp_ifl_name].Service_pol_out = \
                                                dict_policy_map[temp_ifl_name + '/' + temp_search[2] + '_out'].Name
                                    list_line[i] = "\n"
                                elif re.match('^ dot1q termination vid ([\d]+)( vlan-group ([\d]+))?\n',list_line[i]):
                                    temp_search = re.match('^ dot1q termination vid ([\d]+)(?: vlan-group ([\d]+))?\n',
                                                                             list_line[i]).groups()
                                    dict_ifl[temp_ifl_name].SVLAN = temp_search[0]
                                    dict_ifl[temp_ifl_name].Vlan_mapping = 'pop'
                                    dict_ifl[temp_ifl_name].Vlan_translate = '1'
                                    if temp_search[1] is not None:
                                        #if temp_ifl_name=='GigabitEthernet4/1/2.2708':
                                        #    print 'Key:',temp_ifl_name + '/' + temp_search[1] +'_in'
                                        if (temp_ifl_name + '/' + temp_search[1] +'_in') in dict_policy_map:
                                            #print 'Matching...'
                                            dict_ifl[temp_ifl_name].Service_pol_in =\
                                            dict_policy_map[temp_ifl_name + '/' + temp_search[1] +'_in'].Name
                                        if (temp_ifl_name + '/' + temp_search[1] +'_out') in dict_policy_map:
                                            dict_ifl[temp_ifl_name].Service_pol_out =\
                                            dict_policy_map[temp_ifl_name + '/' + temp_search[1] +'_out'].Name
                                    list_line[i] = "\n"
                                elif re.match(' port trunk allow-pass vlan (.*)\n',list_line[i]):
                                    temp_status = True
                                    temp_desc=''
                                    temp_ifl_switch_mode= 'trunk'
                                    ##xoa ngay 1/4/2020 do 2 dong trunk allow vlan , khi qua dong 2 xoa sub dong 1, tu line 1048 dej 1053
                                    #if temp_ifl_name in dict_ifl:
                                    #    temp_status =dict_ifl[temp_ifl_name].Admin_status
                                    #    temp_desc = dict_ifl[temp_ifl_name].Description
                                    #    del dict_ifl[temp_ifl_name] #xoa interface tam
                                    ##xoa ngay 1/4/2020 do 2 dong trunk allow vlan , khi qua dong 2 xoa sub dong 1
                                    temp_search=re.match(' port trunk allow-pass vlan (.*)\n',list_line[i]).groups()
                                    temp_vlan_list =[]
                                    if ' to ' in temp_search[0]:
                                        temp_list = temp_search[0].split()
                                        for idx in range(len(temp_list)):
                                            if temp_list[idx]=='to':
                                                vlan_min = temp_list[idx-1]
                                                vlan_max = temp_list[idx + 1]
                                                vlan_num = int(vlan_max)-int(vlan_min)
                                                for idx_sub in range(1,vlan_num):
                                                    temp_vlan_list.append(str(int(vlan_min)+ idx_sub))
                                            else:
                                                temp_vlan_list.append(temp_list[idx])
                                    elif ' ' in temp_search[0]:
                                        temp_vlan_list = temp_search[0].split()
                                    else:
                                        temp_vlan_list.append(temp_search[0])
                                    #print('line 1067 trong get_interface:',temp_vlan_list,temp_ifl_name)
                                    for item in temp_vlan_list:
                                        temp_ifl = IFL()
                                        temp_ifl.IFD = temp_ifd_name
                                        temp_ifl.Unit = int(item)
                                        temp_ifl.Unit1 = int(item)
                                        temp_ifl.SVLAN = item
                                        temp_ifl.Description = temp_desc
                                        temp_ifl.Service = 'vpls'
                                        temp_ifl.BD_ID = 'VLAN-' + item
                                        temp_ifl.Admin_status = temp_status
                                        temp_ifl.Switchport = True
                                        temp_ifl.Switch_mode = 'trunk'
                                        dict_ifl[temp_ifl.IFD + '.' + str(item)] = temp_ifl
                                        ##Unit = vlan the hien trong temp_ifl_name//31/3/2020
                                        temp_ifl_name=temp_ifl.IFD + '.' + str(item)
                                        ##
                                        #if temp_ifl_name == 'Eth-Trunk6.3021':
                                        #    print('Line 1083 trong get_interface.py:item',temp_ifl.IFD, item)
                                        #    print('line 1085 trong get_interface:', temp_vlan_list, temp_ifl_name,
                                        #          )
                                        #    dict_ifl[temp_ifl.IFD + '.' + item].showdata()
                                    list_line[i]='\n'
                                elif re.match(' port default vlan ([\d])*\n',list_line[i]):
                                    #print 'default:',list_line[i]
                                    temp_status = True
                                    if temp_ifl_name in dict_ifl:
                                        temp_status = dict_ifl[temp_ifl_name].Admin_status
                                        del dict_ifl[temp_ifl_name] #xoa interface tam
                                    temp_search = re.match(' port default vlan ([\d]*)\n',list_line[i]).groups()
                                    temp_ifl = IFL()
                                    temp_ifl.IFD = temp_ifd_name
                                    #port access thi cho unit 0 30/3/2020
                                    temp_ifl.Unit = 0
                                    temp_ifl.Unit1 = 0
                                    #old code: port unit theo vlan
                                    #temp_ifl.Unit = int(temp_search[0])
                                    #temp_ifl.Unit1 = int(temp_search[0])
                                    temp_ifl.Admin_status = temp_status
                                    temp_ifl.Switchport = True
                                    #temp_ifl.Switch_mode = 'access'
                                    temp_ifl.SVLAN = temp_search[0]
                                    temp_ifl.Service='vpls'
                                    temp_ifl.BD_ID = 'VLAN-'+temp_search[0]
                                    dict_ifl[temp_ifl.IFD + '.0'] = temp_ifl
                                    #if temp_ifl.IFD == 'Eth-Trunk6':
                                    #    print('Dong 1113 trong get_interface.py:','Key:',temp_ifl.IFD + '.' + str(temp_ifl.Unit))

                                    #    dict_ifl[temp_ifl.IFD + '.' + str(temp_ifl.Unit)].showdata()
                                elif re.match(' traffic-policy ([\S]*) (inbound|outbound)(?: link-layer)?(?: )?\n',list_line[i]):
                                    if temp_ifd_name=='Eth-Trunk15':
                                        print('line 1122 in get_interface.py:',list_line[i])
                                    temp_search = re.match(' traffic-policy ([\S]*) (inbound|outbound)(?: link-layer)?(?: )?\n',list_line[i]).groups()
                                    if (len(temp_vlan_list)>0)and((temp_ifd_name+'.0')==temp_ifl_name):
                                        for idx in temp_vlan_list:
                                            if temp_search[1] == 'inbound':
                                                if temp_search[0] in list_policer:
                                                    dict_ifl[temp_ifd_name+'.'+idx].Service_pol_in = temp_search[0]
                                                else:
                                                    dict_ifl[temp_ifd_name+'.'+idx].FF_in = temp_search[0]
                                            elif temp_search[1] == 'outbound':
                                                if temp_search[0] in list_policer:
                                                    dict_ifl[temp_ifd_name+'.'+idx].Service_pol_out = temp_search[0]
                                                else:
                                                    dict_ifl[temp_ifd_name+'.'+idx].FF_out = temp_search[0]
                                    else:
                                        if temp_search[1] == 'inbound':
                                            if temp_search[0] in list_policer:
                                                dict_ifl[temp_ifl_name].Service_pol_in = temp_search[0]
                                            else:
                                                dict_ifl[temp_ifl_name].FF_in = temp_search[0]
                                        elif temp_search[1] == 'outbound':
                                            if temp_search[0] in list_policer:
                                                dict_ifl[temp_ifl_name].Service_pol_out = temp_search[0]
                                            else:
                                                dict_ifl[temp_ifl_name].FF_out = temp_search[0]
                                    list_line[i]='\n'
                                elif re.match(' traffic-policy ([\S]*) (inbound|outbound) vlan (.*)\n',list_line[i]):
                                    temp_search =re.match(' traffic-policy ([\S]*) (inbound|outbound) vlan (.*)\n',
                                                          list_line[i]).groups()
                                    #print(list_line[i])
                                    temp_vlan_list = []
                                    if ' to ' in temp_search[2]:
                                        temp_list = temp_search[2].split()
                                        for idx in range(len(temp_list)):
                                            if temp_list[idx] == 'to':
                                                vlan_min = temp_list[idx - 1]
                                                vlan_max = temp_list[idx + 1]
                                                vlan_num = int(vlan_max) - int(vlan_min)
                                                for idx_sub in range(1, vlan_num):
                                                    temp_vlan_list.append(str(int(vlan_min) + idx_sub))
                                            else:
                                                temp_vlan_list.append(temp_list[idx])
                                    elif ' ' in temp_search[2]:
                                        temp_vlan_list = temp_search[2].split()
                                    else:
                                        temp_vlan_list.append(temp_search[2])
                                    for item in temp_vlan_list:
                                        if temp_search[1] == 'inbound':
                                            if temp_search[0] in list_policer:
                                                dict_ifl[temp_ifd_name + '.' + item].Service_pol_in = temp_search[0]
                                            else:
                                                #print(temp_ifd_name, item)
                                                #print(dict_ifl[temp_ifd_name+'.'+ item])
                                                if temp_ifd_name+'.'+ item in dict_ifl.keys():
                                                    dict_ifl[temp_ifd_name+'.'+ item].FF_in = temp_search[0]
                                                else:
                                                    print("Khong co "+ item+" trong "+ temp_ifd_name, list_line[i])
                                        elif temp_search[1] == 'outbound':
                                            if temp_search[0] in list_policer:
                                                dict_ifl[temp_ifd_name + '.' + item].Service_pol_out = temp_search[0]
                                            else:
                                                if temp_ifd_name+'.'+ item in dict_ifl.keys():
                                                    dict_ifl[temp_ifd_name + '.' + item].FF_out = temp_search[0]
                                                else:
                                                    print("Khong co "+ item+" trong "+ temp_ifd_name, list_line[i])
                                    list_line[i] = '\n'
                                elif re.match(' port isolate-state enable vlan (.*)\n',list_line[i]):
                                    temp_search = re.match(' port isolate-state enable vlan (.*)\n',list_line[i]).groups()
                                    temp_vlan_list = []
                                    if ' to ' in temp_search[0]:
                                        temp_list = temp_search[0].split()
                                        for idx in range(len(temp_list)):
                                            if temp_list[idx] == 'to':
                                                vlan_min = temp_list[idx - 1]
                                                vlan_max = temp_list[idx + 1]
                                                vlan_num = int(vlan_max) - int(vlan_min)
                                                for idx_sub in range(1, vlan_num):
                                                    temp_vlan_list.append(str(int(vlan_min) + idx_sub))
                                            else:
                                                temp_vlan_list.append(temp_list[idx])
                                    elif ' ' in temp_search[0]:
                                        temp_vlan_list = temp_search[0].split()
                                    else:
                                        temp_vlan_list.append(temp_search[0])
                                    #print('line 1196 trong get_interface.py',temp_vlan_list,temp_ifl_name)
                                    for item in temp_vlan_list:
                                        #if temp_ifl.IFD=='Eth-Trunk6':
                                        #    print('line 1203 trong get_interface.py:',item)
                                        #    dict_ifl[temp_ifl.IFD + '.' + item].showdata()
                                        dict_ifl[temp_ifl.IFD + '.' + str(item)].Split_horizon = True
                                    list_line[i] = '\n'
                                elif re.match(' vlan-group (.*)\n',list_line[i]):
                                    temp_name = re.match(' vlan-group (.*)\n',list_line[i]).groups()[0]
                                    i += 1
                                    while list_line[i][0:2]=='  ':
                                        #print 'Truoc khi match if:',i,list_line[i]
                                        if re.match('  user-queue cir ([\d]*) pir ([\d]*)(?: flow-queue ([\S]*)'
                                                    ' flow-mapping ([\S]*) )? (inbound|outbound)',list_line[i]):
                                            #print 'Kiem tra policy:',list_line[i]
                                            temp_search = re.match('  user-queue cir ([\d]*) pir ([\d]*)(?: flow-queue '
                                                                  '([\S]*) flow-mapping ([\S]*))? (inbound|outbound)'
                                                                  ,list_line[i]).groups()
                                            list_line[i]='\n'
                                            temp_policy_map = Policy_map()
                                            temp_policy_map.Name = temp_search[0] + '_' + temp_search[1]
                                            temp_policy_map.CIR = int(temp_search[0])
                                            temp_policy_map.PIR = int(temp_search[1])
                                            if temp_search[2] is not None:
                                                j=0
                                                while j<total_lines:
                                                    if re.match('flow_mapping (.*)\n',list_line[j]):
                                                        temp_search1 = re.match('flow_mapping (.*)\n',list_line[j]).groups()[0]
                                                        if temp_search1 == temp_search[2]:
                                                            j += 1
                                                            while ('flow-mapping ' not in list_line[j])\
                                                                and(list_line[j]!='#\n'):
                                                                if 'map flow-queue ' in list_line[j]:
                                                                    temp_policy_map.Class = list_line[j].strip().split()[-1]
                                                                    list_line[j]='\n'
                                                                j +=1
                                                            j -= 1
                                                            break
                                                    j += 1

                                            if temp_search[4] is not None:
                                                if temp_search[4] == 'inbound':
                                                    if temp_ifl_name == temp_ifd_name + '.0' :
                                                        dict_policy_map[temp_ifd_name + '/' + temp_name + '_in'] = temp_policy_map
                                                    else:
                                                        dict_policy_map[
                                                            temp_ifl_name + '/' + temp_name + '_in'] = temp_policy_map
                                                elif temp_search[4] == 'outbound':
                                                    if temp_ifl_name == temp_ifd_name + '.0':
                                                        dict_policy_map[temp_ifd_name + '/' + temp_name + '_out'] = temp_policy_map
                                                    else:
                                                        dict_policy_map[
                                                            temp_ifl_name + '/' + temp_name + '_out'] = temp_policy_map
                                                #if temp_ifd_name=='GigabitEthernet4/1/2':
                                                #    print 'Key:',temp_ifd_name + '/' + temp_name
                                                #    print 'IFL:',temp_ifl_name
                                                #    temp_policy_map.showdata()
                                        elif list_line[i]==' [\S].*\n':
                                            break
                                        i += 1
                                    i -= 1
                                    list_line[i]='\n'
                                elif re.match(' qinq stacking vid ([\d]*(?: to [\d]*)?)(?: vlan-group (.*))?\n',list_line[i]):
                                    temp_search = re.match(' qinq stacking vid ([\d]*(?: to [\d]*)?)(?: vlan-group (.*))?\n',
                                                           list_line[i]).groups()
                                    #print 'Stacking:',list_line[i]
                                    #print 'Result regex:',temp_search
                                    if ' to ' in temp_search[0]:
                                        temp_str = temp_search[0].split()[0] + '-' + temp_search[0].split()[2]
                                    else:
                                        temp_str = temp_search[0]
                                    if dict_ifl[temp_ifl_name].SVLAN == '':
                                        dict_ifl[temp_ifl_name].SVLAN = temp_str
                                    else:
                                        dict_ifl[temp_ifl_name].SVLAN = dict_ifl[temp_ifl_name].SVLAN + ',' + temp_str
                                    if temp_search[1] is not None:
                                        if (temp_ifl_name + '/' + temp_search[1] +'_in') in dict_policy_map:
                                            dict_ifl[temp_ifl_name].Service_pol_in =\
                                            dict_policy_map[temp_ifl_name + '/' + temp_search[1] +'_in'].Name
                                        if (temp_ifl_name + '/' + temp_search[1] +'_out') in dict_policy_map:
                                            dict_ifl[temp_ifl_name].Service_pol_out =\
                                            dict_policy_map[temp_ifl_name + '/' + temp_search[1] +'_out'].Name
                                    dict_ifl[temp_ifl_name].Vlan_mapping='push'
                                    dict_ifl[temp_ifl_name].Vlan_translate = '1'
                                    #if hostname == 'LSN02VLG':
                                    #    dict_ifl[temp_ifl_name].showdata()
                                    list_line[i] ='\n'
                                elif re.match('^ mtu (.*)\n', list_line[i]):
                                    dict_ifl[temp_ifl_name].MTU=int(re.match('^ mtu (.*)\n', list_line[i]).groups()[0])
                                    list_line[i] = "\n"
                                elif re.match(' qinq termination l2 symmetry',list_line[i]):
                                    dict_ifl[temp_ifl_name].Vlan_mapping='pop'
                                    dict_ifl[temp_ifl_name].Vlan_translate = '1'
                                    list_line[i] = "\n"
                                elif re.match(' qinq termination pe-vid ([\d]*) ce-vid ([\d]*(?: to [\d]*)?)'
                                              '(?: vlan-group ([\d]*))?\n',list_line[i]):
                                    #print 'Gia tri xu ly qinq ter:',list_line[i]
                                    temp_search = re.match(' qinq termination pe-vid ([\d]*) ce-vid ([\d]*(?: to [\d]*)?)'
                                                           '(?: vlan-group ([\d]*))?\n',list_line[i]).groups()
                                    dict_ifl[temp_ifl_name].SVLAN = temp_search[0]
                                    if ' to ' in temp_search[1]:
                                        temp_str = temp_search[1].split()[0] + '-' + temp_search[1].split()[2]
                                    else:
                                        temp_str = temp_search[1]
                                    if dict_ifl[temp_ifl_name].CVLAN == '':
                                        dict_ifl[temp_ifl_name].CVLAN = temp_str
                                    else:
                                        dict_ifl[temp_ifl_name].CVLAN = dict_ifl[temp_ifl_name].CVLAN + ',' + temp_str
                                    #print temp_ifl_name,dict_ifl[temp_ifl_name].SVLAN,dict_ifl[temp_ifl_name].CVLAN
                                    if dict_ifl[temp_ifl_name].Vlan_mapping=='':
                                        dict_ifl[temp_ifl_name].Vlan_mapping = 'pop'
                                        dict_ifl[temp_ifl_name].Vlan_translate = '2'
                                    if temp_search[2] is not None:
                                        if (temp_ifl_name + '/' + temp_search[2] + '_in') in dict_policy_map:
                                            dict_ifl[temp_ifl_name].Service_pol_in = \
                                                dict_policy_map[temp_ifl_name + '/' + temp_search[2] + '_in'].Name
                                        if (temp_ifl_name + '/' + temp_search[2] + '_out') in dict_policy_map:
                                            #print 'Gia tri policy:',dict_policy_map[temp_ifd_name + '/' + temp_search[2] + '_out'].Name
                                            dict_ifl[temp_ifl_name].Service_pol_out = \
                                                dict_policy_map[temp_ifl_name + '/' + temp_search[2] + '_out'].Name
                                    list_line[i] = "\n"
                                elif re.match(' trust upstream [\S]+\n',list_line[i]):
                                    #print('get_inft.py,line 1315',list_line[i])
                                    dict_ifl[temp_ifl_name].trust_upstream = True
                                    list_line[i] = '\n'
                                elif re.match(' trust 8021p\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].p1 = True
                                    list_line[i]='\n'
                                elif re.match(' diffserv-mode pipe (.*)\n',list_line[i]):
                                    temp_search = re.match(' diffserv-mode pipe (.*)\n',list_line[i]).groups()
                                    dict_ifl[temp_ifl_name].classifier = temp_search[0]
                                    list_line[i]='\n'
                                elif re.match('^ ip binding vpn-instance ([\S]+)\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].VRF_Name = re.match('^ ip binding vpn-instance ([\S]+)\n',
                                                                                list_line[i]).groups()[0]
                                    dict_ifl[temp_ifl_name].Service = 'l3vpn'
                                    if dict_ifl[temp_ifl_name].VRF_Name in dict_vrf:
                                        dict_ifl[temp_ifl_name].df_classifier = \
                                            dict_vrf[dict_ifl[temp_ifl_name].VRF_Name].classifier
                                    list_line[i] = "\n"
                                elif re.match(' arp detect-mode unicast\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].ARP_Unicast = True
                                    list_line[i] = '\n'
                                elif re.match(' arp expire-time ([\d]+)\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].ARP_exp = int(re.match(' arp expire-time ([\d]+)\n',
                                                                                   list_line[i]).groups()[0])
                                    list_line[i]='\n'
                                elif re.match(' mpls l2vc(?: instance-name [\S]*)? ((?:[\d]{1,3}[\.]){3,3}[\d]{1,3}) ([\d]*)(?: tunnel-policy ([\S]+))?'
                                              '( no-control-word| control-word)?\n', list_line[i]):
                                    temp_search = re.match(' mpls l2vc(?: instance-name [\S]*)? ((?:[\d]{1,3}[\.]){3,3}[\d]{1,3}) ([\d]*)(?: tunnel-policy ([\S]+))?'
                                                           '( no-control-word| control-word)?\n', list_line[i]).groups()
                                    temp_l2vpn = L2VPN()
                                    temp_l2vpn.Peer = temp_search[0]
                                    temp_l2vpn.VC_ID = temp_search[1]
                                    temp_l2vpn.Type = 'l2circuit'
                                    temp_l2vpn.MTU = dict_ifl[temp_ifl_name].MTU
                                    dict_ifl[temp_ifl_name].Service = 'l2circuit'
                                    dict_ifl[temp_ifl_name].vsi_encap = 'tagged'
                                    if temp_search[2] is not None:
                                        temp_l2vpn.PW_Class = temp_search[2]
                                    if (temp_search[3] is not None)and(' control-word' in temp_search[3]):
                                        temp_l2vpn.CW = True
                                    temp_l2vpn.IFL = temp_ifl_name
                                    list_line[i]='\n'
                                    if 'secondary' in list_line[i+1]:
                                        #print 'Loi vc secondary:',list_line[i+1]
                                        temp_search = re.match(' mpls l2vc ((?:[\d]{1,3}[\.]){3,3}[\d]{1,3})'
                                                               ' ([\d]*)(?: tunnel-policy ([\S]*))?( no-control-word| control-word)?'
                                                               ' secondary\n',list_line[i+1]).groups()
                                        temp_l2vpn.BK_Peer = temp_search[0]
                                        temp_l2vpn.Bk_vc_id = temp_search[1]
                                        if temp_search[2] is not None:
                                            temp_l2vpn.PW_class_bk = temp_search[2]
                                        if (temp_search[3] is not None)and(' control-word' in temp_search[3]):
                                            temp_l2vpn.CW = True
                                        list_line[i+1]='\n'
                                        i +=1
                                    dict_l2vpn[temp_l2vpn.Peer+'/'+str(temp_l2vpn.VC_ID)] = temp_l2vpn
                                elif re.match(' l2 binding vsi (.*)\n',list_line[i]):
                                    temp_search = re.match(' l2 binding vsi (.*)\n',list_line[i]).groups()
                                    dict_ifl[temp_ifl_name].Service='vpls'
                                    dict_ifl[temp_ifl_name].BD_ID = temp_search[0]
                                    if dict_ifl[temp_ifl_name].BD_ID in dict_vsi:
                                        dict_ifl[temp_ifl_name].vsi_encap = \
                                            dict_vsi[dict_ifl[temp_ifl_name].BD_ID].encap
                                        dict_ifl[temp_ifl_name].Split_horizon = \
                                            dict_vsi[dict_ifl[temp_ifl_name].BD_ID].isolate
                                        dict_ifl[temp_ifl_name].df_classifer = \
                                            dict_vsi[dict_ifl[temp_ifl_name].BD_ID].classifier
                                    list_line[i]='\n'
                                elif re.match(' rrpp snooping enable\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].rrpp=True
                                    list_line[i] = '\n'
                                elif re.match(' rrpp snooping vsi ([\S]*)\n',list_line[i]):
                                    temp_search = re.match(' rrpp snooping vsi ([\S]*)\n',list_line[i]).groups()
                                    if dict_ifl[temp_ifl_name].rrpp_vsi_list =='':
                                        dict_ifl[temp_ifl_name].rrpp_vsi_list = temp_search[0]
                                    else:
                                        dict_ifl[temp_ifl_name].rrpp_vsi_list = dict_ifl[temp_ifl_name].rrpp_vsi_list +\
                                                                                ' '+ temp_search[0]
                                    list_line[i]='\n'
                                elif re.match(' isis enable .*\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].Routing_type = 'isis'
                                    list_line[i]='\n'
                                elif re.match(' isis circuit-type p2p\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].ISIS_circuit_type = 'p2p'
                                    list_line[i]='\n'
                                elif re.match(' isis circuit-level (.*)\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].ISIS_circuit_type = re.match(' isis circuit-level (.*)\n',
                                                                                         list_line[i]).groups()[0]
                                    list_line[i]='\n'
                                elif re.match(' isis ldp-sync\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].ldp_sync = True
                                    list_line[i]='\n'
                                elif re.match(' isis bfd min-tx-interval ([\d]*) min-rx-interval ([\d]*) detect-multiplier ([\d]*)',
                                              list_line[i]):
                                    temp_search = re.match(' isis bfd min-tx-interval ([\d]*) min-rx-interval ([\d]*)'
                                                           ' detect-multiplier ([\d]*)', list_line[i]).groups()
                                    dict_ifl[temp_ifl_name].isis_bfd = temp_search[0] + '/' + temp_search[1] \
                                                                       + '/' + temp_search[2]
                                    list_line[i]='\n'
                                elif re.match(' isis cost (.*)\n',list_line[i]):
                                    print(list_line[i])
                                    dict_ifl[temp_ifl_name].Intf_metric= int(re.match(' isis cost ([0-9]*).*\n',
                                                                             list_line[i]).groups()[0])
                                    list_line[i] = '\n'
                                elif re.match(' isis authentication-mode md5 .*\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].isis_authen = True
                                    list_line[i]='\n'
                                elif re.match(' pim sm\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].PIM= True
                                    list_line[i] = '\n'
                                elif re.match(' mpls te\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].RSVP = True
                                    list_line[i] = '\n'
                                elif re.match(' mpls ldp\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].MPLS = True
                                    list_line[i] = '\n'
                                elif re.match(' mpls\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].MPLS = True
                                    list_line[i] = '\n'
                                elif re.match(' igmp enable',list_line[i]):
                                    dict_ifl[temp_ifl_name].igmp = True
                                    list_line[i] = '\n'
                                elif re.match(' igmp static-group (.*) source (.*)\n',list_line[i]):
                                    temp_search = re.match(' igmp static-group (.*) source (.*)\n',list_line[i]).groups()
                                    dict_ifl[temp_ifl_name].igmp_static = temp_search[0] + '/' + temp_search[1]
                                    list_line[i] = '\n'
                                elif re.match(' igmp ssm-mapping enable\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].igmp_ssm = 'enable'
                                elif re.match(' igmp group-policy (.*)\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].igmp_ssm = 'enable'+ re.match(' igmp group-policy (.*)\n'
                                                                                          , list_line[i]).groups()[0]
                                    list_line[i] = '\n'
                                elif re.match(' ip relay address (.*)\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].IP_helper = re.match(' ip relay address (.*)\n',
                                                                                 list_line[i]).groups()[0]
                                    list_line[i] = '\n'
                                elif re.match(' dhcp snooping enable\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].dhcp_snoop = True
                                    list_line[i] = '\n'
                                elif re.match(' dhcp snooping trusted\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].dhcp_trust = True
                                    list_line[i] = '\n'
                                elif re.match(' vrrp vrid ([\d]*) virtual-ip ((?:[\d]{1,3}[\.]){3,3}[\d]{1,3})\n',
                                              list_line[i]):
                                    temp_search = re.match(' vrrp vrid ([\d]*) virtual-ip ((?:[\d]{1,3}[\.]){3,3}[\d]{1,3})\n',
                                              list_line[i]).groups()
                                    dict_ifl[temp_ifl_name].vrrp= True
                                    if dict_ifl[temp_ifl_name].vrrp_group =='':
                                        dict_ifl[temp_ifl_name].vrrp_group = temp_search[0]
                                        #dict_ifl[temp_ifl_name].vrrp_prio = temp_search[0] + '_100'
                                    else:
                                        if temp_search[0] not in dict_ifl[temp_ifl_name].vrrp_group:
                                            dict_ifl[temp_ifl_name].vrrp_group = dict_ifl[temp_ifl_name].vrrp_group +\
                                                                             '/' + temp_search[0]

                                    if dict_ifl[temp_ifl_name].vrrp_vip == '':
                                        dict_ifl[temp_ifl_name].vrrp_vip = temp_search[0] + '_' + temp_search[1]
                                    else:
                                        dict_ifl[temp_ifl_name].vrrp_vip = dict_ifl[temp_ifl_name].vrrp_vip + '/' + \
                                                                           temp_search[0] + '_' + temp_search[1]

                                    list_line[i] = '\n'
                                elif re.match(' vrrp vrid ([\d]*) priority ([\d]*)\n',list_line[i]):
                                    temp_search = re.match(' vrrp vrid ([\d]*) priority ([\d]*)\n',list_line[i]).groups()
                                    if dict_ifl[temp_ifl_name].vrrp_prio=='':
                                        dict_ifl[temp_ifl_name].vrrp_prio = temp_search[0]+'_'+temp_search[1]
                                    else:
                                        dict_ifl[temp_ifl_name].vrrp_prio = dict_ifl[temp_ifl_name].vrrp_prio + '/' +\
                                                temp_search[0] + '_' + temp_search[1]
                                    list_line[i] = '\n'
                                elif re.match(' vrrp vrid ([\d]*) preempt-mode timer delay ([\d]*)\n',list_line[i]):
                                    temp_search=re.match(' vrrp vrid ([\d]*) preempt-mode timer delay ([\d]*)\n',
                                                                                      list_line[i]).groups()
                                    if dict_ifl[temp_ifl_name].vrrp_delay =='':
                                        dict_ifl[temp_ifl_name].vrrp_delay = temp_search[0] + '_' + temp_search[1]
                                    else:
                                        dict_ifl[temp_ifl_name].vrrp_delay = dict_ifl[temp_ifl_name].vrrp_delay + '/' +\
                                                                             temp_search[0] + '_' + temp_search[1]
                                    list_line[i] = '\n'
                                elif re.match(' vrrp vrid ([\d]*) track interface ([\S]+) reduced ([\d]+)\n',list_line[i]):
                                    temp_search = re.match(' vrrp vrid ([\d]*) track interface ([\S]+) reduced ([\d]+)\n',
                                                           list_line[i]).groups()
                                    if dict_ifl[temp_ifl_name].vrrp_track =='':
                                        dict_ifl[temp_ifl_name].vrrp_track = temp_search[0] + '_' + temp_search[1]
                                    else:
                                        dict_ifl[temp_ifl_name].vrrp_track = dict_ifl[temp_ifl_name].vrrp_track + '/' +\
                                                                             temp_search[0] + '_' + temp_search[1]
                                    if dict_ifl[temp_ifl_name].vrrp_reduce == '':
                                        dict_ifl[temp_ifl_name].vrrp_reduce = temp_search[0] + '_' +temp_search[2]
                                    else:
                                        dict_ifl[temp_ifl_name].vrrp_reduce = dict_ifl[temp_ifl_name].vrrp_reduce +\
                                                                              +'/' + temp_search[0] + '_' + temp_search[2]
                                    list_line[i] = '\n'
                                elif re.match(' loop-detect enable\n',list_line[i]):
                                    if (len(temp_vlan_list)>0)and((temp_ifd_name+'.0')==temp_ifl_name):
                                        for idx in temp_vlan_list:
                                            dict_ifl[temp_ifd_name+'.'+idx].loop_detect = True
                                    list_line[i] = '\n'
                                elif re.match(' shutdown\n',list_line[i]):
                                    dict_ifl[temp_ifl_name].Admin_status = False
                                    list_line[i] = "\n"
                                i += 1
                            i -= 1
                elif re.match('interface (Tunnel.*)\n',list_line[i]):
                    temp_search = re.match('interface (Tunnel.*)\n',list_line[i]).groups()
                    temp_lsp = LSP()
                    temp_lsp.Name = temp_search[0]
                    i += 1
                    while list_line[i] != '#\n':
                        if re.match(' description (.*)\n', list_line[i]):
                            temp_search = re.match(' description (.*)\n', list_line[i]).groups()
                            temp_lsp.Description = temp_search[0]
                        elif re.match(' destination (.*)\n', list_line[i]):
                            temp_search = re.match(' destination (.*)\n', list_line[i]).groups()
                            temp_lsp.Dest = temp_search[0]
                        elif re.match(' tunnel-protocol mpls te\n',list_line[i]):
                            temp_lsp.TE = True
                        elif re.match(' mpls te bfd enable\n', list_line[i]):
                            temp_lsp.bfd = True
                        elif re.match(' mpls te bfd min-tx-interval ([\d]*) '
                                      'min-rx-interval ([\d]*) detect-multiplier ([\d]*)\n', list_line[i]):
                            temp_search = re.match(' mpls te bfd min-tx-interval ([\d]*) '
                                      'min-rx-interval ([\d]*) detect-multiplier ([\d]*)\n', list_line[i]).groups()
                            temp_lsp.bfd_info = temp_search[0] + '/' + temp_search[1] + '/' + temp_search[2]
                        elif re.match(' ip address (?:(?:unnumbered interface ([\S]*))|([\S]*))\n',list_line[i]):
                            temp_search=re.match(' ip address (?:(?:unnumbered interface ([\S]*))|([\S]*))\n',
                                                 list_line[i]).groups()
                            if temp_search[0] is not None:
                                temp_lsp.Src = temp_search[0]
                            if temp_search[1] is not None:
                                temp_lsp.Src = temp_search[1]
                        elif re.match(' mpls te path explicit-path ([\S]*)(?:  )?( secondary)?\n',list_line[i]):
                            #print(list_line[i])
                            temp_search = re.match(' mpls te path explicit-path ([\S]*)(?:  )?( secondary)?\n',
                                                   list_line[i]).groups()
                            if temp_search[1] is not None:
                                temp_lsp.Backup_path = temp_search[0]
                            else:
                                temp_lsp.Path = temp_search[0]
                        elif re.match(' mpls te backup ordinary best-effort[\s]?\n',list_line[i]):
                            temp_lsp.Bk_path_org=True
                        elif re.match(' mpls te backup hot-standby mode revertive wtr [\d]+[\s]?\n',list_line[i]):
                            temp_lsp.Bk_host_stb = True
                        elif list_line[i].strip() == "shutdown":
                            temp_lsp.Admin_status = False
                        list_line[i] = "\n"
                        i += 1
                    i -= 1
                    dict_lsp[temp_lsp.Name] = temp_lsp
                elif re.match('[\s]?ccc ([\S]+) interface ([\S]+)( '
                              'tagged)? out-interface ([\S]+)( tagged)?\n',list_line[i]):
                    temp_search=re.match('[\s]?ccc ([\S]+) interface ([\S]+)( '
                              'tagged)? out-interface ([\S]+)( tagged)?\n',list_line[i]).groups()

                    if '.' not in temp_search[1]:
                        temp_ifl1 = temp_search[1]+'.0'
                    else:
                        temp_ifl1 = temp_search[1]
                    if '.' not in temp_search[3]:
                        temp_ifl2 = temp_search[3]+'.0'
                    else:
                        temp_ifl2 = temp_search[3]
                    if temp_search[2] is not None:
                        if (temp_ifl1 in dict_ifl)and(temp_ifl2 in dict_ifl):
                            dict_ifl[temp_ifl1].Service='ccc-tag'
                            dict_ifl[temp_ifl1].CCC_Intf = temp_ifl2
                            dict_ifl[temp_ifl1].CCC_Name = temp_search[0]
                            dict_ifl[temp_ifl2].Service = 'ccc-tag'
                            dict_ifl[temp_ifl2].CCC_Intf = temp_ifl1
                            dict_ifl[temp_ifl2].CCC_Name = temp_search[0]
                        else:
                            print(hostname,'Chua khai bao ifl:',temp_ifl1,temp_ifl2)
                    else:
                        if (temp_ifl1 in dict_ifl)and(temp_ifl2 in dict_ifl):
                            if re.match('.*\.0$',temp_ifl1):
                                dict_ifl[temp_ifl1].Service='ccc'
                            else:
                                dict_ifl[temp_ifl1].Service = 'ccc-tag'
                            dict_ifl[temp_ifl1].CCC_Intf = temp_ifl2
                            dict_ifl[temp_ifl1].CCC_Name = temp_search[0]
                            if re.match('.*\.0$', temp_ifl2):
                                dict_ifl[temp_ifl2].Service = 'ccc'
                            else:
                                dict_ifl[temp_ifl2].Service = 'ccc-tag'
                            dict_ifl[temp_ifl2].CCC_Intf = temp_ifl1
                            dict_ifl[temp_ifl2].CCC_Name = temp_search[0]
                        else:
                            print(hostname,'Chua khai bao ifl:',temp_ifl1,temp_ifl2)
                    list_line[i]='\n'
                i += 1

            i =0
            while i<total_lines:
                if re.match('bfd ([\S]*) bind peer-ip ([\S]*)(?: vpn-instance ([\S]*))? interface ([\S]*)'
                            '(?: source-ip ([\S]*))?(?: auto)?\n',list_line[i]):
                    temp_search = re.match('bfd ([\S]*) bind peer-ip ([\S]*)(?: vpn-instance ([\S]*))? interface ([\S]*)'
                            '(?: source-ip ([\S]*))?(?: auto)?\n',list_line[i]).groups()
                    temp_bfd = BFD()
                    temp_bfd.Name = temp_search[0]
                    temp_bfd.Peer_ip = temp_search[1]
                    if temp_search[2] is not None:
                        temp_bfd.VRF_Name = temp_search[2]
                    if temp_search[3] is not None:
                        temp_bfd.IFL = temp_search[3]
                    if temp_search[4] is not None:
                        temp_bfd.Source_ip = temp_search[4]
                    i += 1
                    while list_line[i]!='#\n':
                        if re.match(' discriminator local ([\d]*)\n',list_line[i]):
                            temp_bfd.Disc_local = int(re.match(' discriminator local ([\d]*)\n',list_line[i]).groups()[0])
                        elif re.match(' discriminator remote ([\d]*)\n',list_line[i]):
                            temp_bfd.Disc_remote = int(re.match(' discriminator remote ([\d]*)\n',list_line[i]).groups()[0])
                        elif re.match(' detect-multiplier ([\d]*)\n',list_line[i]):
                            temp_bfd.Multiplier = int(re.match(' detect-multiplier ([\d]*)\n',list_line[i]).groups()[0])
                        elif re.match(' min-tx-interval ([\d]*)\n',list_line[i]):
                            temp_bfd.Min_tx = int(re.match(' min-tx-interval ([\d]*)\n',list_line[i]).groups()[0])
                        elif re.match(' min-rx-interval ([\d]*)\n',list_line[i]):
                            temp_bfd.Min_rx = int(re.match(' min-rx-interval ([\d]*)\n',list_line[i]).groups()[0])
                        elif re.match(' wtr ([\d]*)\n',list_line[i]):
                            temp_bfd.Wtr = int(re.match(' wtr ([\d]*)\n',list_line[i]).groups()[0])
                        elif re.match(' process-interface-status\n',list_line[i]):
                            temp_bfd.Process_intf = True
                        list_line[i]='\n'
                        i += 1
                    dict_bfd[temp_bfd.Name]= temp_bfd
                    i -= 1
                i += 1
            print('Data Policy:processing')
            for key in dict_policy_map:
                #print key,dict_policy_map[key].showdata()
                dict_policy_map[key].insert(cursor)
            print('Data IFD:processing')
            for key in list_ifd:
                if (key!='LoopBack')and(key!='Vlanif'):
                    dict_ifl_filter = {k:v for k,v in dict_ifl.items() if key + '.' in k}
                    #print key,dict_ifl_filter
                    if len(dict_ifl_filter)>1:
                        #print 'Gia tri len > 1 :',dict_ifl_filter
                        list_ifd[key].Flex_service = True
                        list_ifd[key].Flex_vlan_tag = True
                    elif len(dict_ifl_filter) == 1:
                        #print 'Gia tri =1', key, dict_ifl_filter
                        if (key + '.0' not in dict_ifl_filter) :
                            #print 'Gia tri ko co .0:',dict_ifl_filter
                            list_ifd[key].Flex_service = True
                            list_ifd[key].Flex_vlan_tag = True
                #list_ifd[key].showdata()
                list_ifd[key].insert(cursor)

            print('Data l2vpn:processing')
            for key in dict_l2vpn:
                dict_l2vpn[key].insert(cursor)
            print('Data LSP:processing')
            for key in dict_lsp:
                dict_lsp[key].showdata()
                dict_lsp[key].insert(cursor)
            print('Data BFD:processing')
            for key in dict_bfd:
                dict_bfd[key].insert(cursor)
            print('Data IFL:processing')
            for key in dict_ifl:
                if (dict_ifl[key].Routing_type == 'isis') and (dict_ifl[key].MPLS == True) and \
                        (dict_ifl[key].RSVP == True):
                    dict_ifl[key].Service = 'CORE'
                if (dict_ifl[key].IP_helper!='')and(dict_ifl[key].VRF_Name!=''):
                    temp_vrf = VRF()
                    temp_vrf.Name = dict_ifl[key].VRF_Name
                    temp_vrf.DHCP_Relay = True

                    if 'Vlanif' in key:
                        temp_ifl = IFL()
                        temp_ifl.IFD = 'LoopBack'
                        temp_ifl.Unit = dict_ifl[key].Unit
                        temp_ifl.Unit1 = dict_ifl[key].Unit
                        temp_ifl.VRF_Name = dict_ifl[key].VRF_Name
                        temp_ifl.Service = "L3VPN"
                        temp_ifl.df_classifier = dict_ifl[key].df_classifier

                        if dict_ifl[key].IP!='':
                            temp_network = dict_ifl[key].IP.split()[0]+'/'+dict_ifl[key].IP.split()[1]
                            temp_static = Static_Route()

                            temp_ip = IPNetwork(temp_network)
                            temp_static.Net = str(temp_ip.network) + ' ' + str(temp_ip.netmask)
                            temp_static.VRF_Name = dict_ifl[key].VRF_Name
                            temp_static.description = 'Static route for DHCP clients'
                            temp_static.insert(cursor)
                            temp_vrf.Static_routing = True
                            #temp_vrf.showdata()
                            temp_ifl.IP = dict_ifl[key].IP.split()[0]+' ' + '255.255.255.255'

                        #temp_ifl.IP_helper = dict_ifl[key].IP_helper
                        temp_ifl.MTU = dict_ifl[key].MTU
                        temp_ifl.Admin_status = dict_ifl[key].Admin_status
                        dict_ifl['LoopBack'+str(temp_ifl.Unit)]=temp_ifl

                        for key1 in dict_ifl:
                            if (dict_ifl[key1].Unit == dict_ifl[key].Unit) and (dict_ifl[key1].Service=='vpls'):
                                dict_ifl[key1].VRF_Name = dict_ifl[key].VRF_Name
                                dict_ifl[key1].IP = 'lo0.'+str(dict_ifl[key].Unit)
                                dict_ifl[key1].IP_helper = dict_ifl[key].IP_helper
                                dict_ifl[key1].Service='L3VPN'
                                dict_ifl[key1].BD_ID=''
                                dict_ifl[key1].df_classifier = dict_ifl[key].df_classifier
                                if dict_ifl[key].IP!='':
                                    dict_ifl[key1].dhcp_gw=dict_ifl[key].IP.split()[0]
                                #dict_ifl[key1].MTU = dict_ifl[key].MTU
                        dict_ifl.pop(key)
                    if temp_vrf.Static_routing == True:
                        temp_vrf.update_dhcp_static(cursor)
                    else:
                        temp_vrf.insert_dhcp_relay(cursor)
                elif (dict_ifl[key].IP_helper != ''):
                    print('Xay ra truong hop dhcp global')
                    dict_ifl[key].showdata()
                elif ('Vlanif' in key) and(dict_ifl[key].IP_helper==''):# and (dict_ifl[key].IP!=''):
                    dict_ifl[key].Stitching = True
                    dict_ifl[key].Service='l3/vpls'
                #if dict_ifl[key].IFD=='Loopback':
                #    dict_ifl[key].showdata()
                #dict_ifl[key].showdata()
            for key in dict_ifl:
                #dict_ifl[key].showdata()
                #loai bo cac interface ifl ko co service 6/4/2020 line 1745
                if dict_ifl[key].Service!="":
                    dict_ifl[key].insert(cursor)
            i = 0
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