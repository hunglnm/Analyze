from vrf_ie import VRF_IE
from vrf import VRF
import MySQLdb
import os
import re


def get_vrf_from_log(list_line, hostname, Dev, total_lines, log_path, f_file,conn ,cursor):
    # Connect and update database
    try:
        i = 0
        VRF.Hostname = hostname
        VRF_IE.Hostname = hostname
        if not os.path.exists(log_path + "VRF"):
            os.mkdir(log_path + "VRF")
        with open(log_path + "VRF/" + hostname + ".txt", "w") as f:
            f.write("=========Get L3VPN informations of routers==========\n")
        f = open(log_path + "VRF/" + hostname + ".txt", "a")
        if Dev == "C76xx":
            while i < total_lines:
                if ("ip vrf " in list_line[i]) and ("ip vrf forwarding " not in list_line[i]):
                    temp_vrf = VRF()
                # add VRF Name
                    temp_vrf.Name = list_line[i].strip().split(" ")[-1].strip()
                    f.write("\n")
                    i += 1
                    temp_seq_exp = 0
                    temp_seq_imp = 0
                    while "!" not in list_line[i]:
                        if " rd " in list_line[i]:
                        # add RD
                            temp_vrf.RD = list_line[i].strip().split(" ")[-1].strip()
                            temp_vrf.insert(cursor)
                            f.write("\n")
                        elif " export map " in list_line[i]:
                            temp_route_map_name = list_line[i].strip().split(" ")[-1].strip()
                            j=i
                            while j<total_lines:
                                if ("route-map " + temp_route_map_name) in list_line[j]:
                                    temp_vrf_ie = VRF_IE()
                                    temp_vrf_ie.Name = list_line[i].strip().split(" ")[-1].strip()
                                    temp_vrf_ie.VRF_Name = temp_vrf.Name
                                    temp_vrf_ie.IE = "exp"
                                    temp_vrf_ie.Seq = int(list_line[j].strip().split(" ")[-1].strip())
                                    j +=1
                                    while "!" not in list_line[j]:
                                        if "match ip " in list_line[j]:
                                            temp_vrf_ie.ACL = list_line[j].strip().split(" ")[-1].strip()
                                        elif "set extcommunity rt " in list_line[j]:
                                            temp_vrf_ie.Extcomm = list_line[j].strip().split(" ")[4]
                                            if "additive" in list_line[j]:
                                                temp_vrf_ie.Action = "add"
                                        j +=1
                                    temp_vrf_ie.insert(cursor)
                                j +=1
                            f.write("\n")
                        elif " route-target export" in list_line[i]:
                            temp_vrf_ie = VRF_IE()
                            temp_vrf_ie.Name = temp_vrf.Name + "_default_exp"  # xem nhu policy export default
                            temp_vrf_ie.VRF_Name = temp_vrf.Name
                            temp_vrf_ie.Seq = temp_seq_exp
                            temp_vrf_ie.ACL = ""
                            temp_vrf_ie.IE = "exp"
                            temp_vrf_ie.Action = "add"
                            temp_vrf_ie.Extcomm = list_line[i].strip().split(" ")[-1].strip()
                            temp_seq_exp += 1
                            temp_vrf_ie.insert(cursor)
                            f.write("\n")
                        elif " route-target import" in list_line[i]:
                            temp_vrf_ie = VRF_IE()
                            temp_vrf_ie.Name = temp_vrf.Name + "_default_imp"  # xem nhu policy import default
                            temp_vrf_ie.VRF_Name = temp_vrf.Name
                            temp_vrf_ie.Seq = temp_seq_imp
                            temp_vrf_ie.IE = "imp"
                            temp_vrf_ie.Action = ""
                            temp_vrf_ie.Extcomm = list_line[i].strip().split(" ")[-1].strip()
                            temp_seq_imp += 1
                            temp_vrf_ie.insert(cursor)
                            f.write("\n")
                        else:
                            f.write(list_line[i])
                        i += 1
                else:
                    f.write(list_line[i])
                i += 1
        elif Dev == "ASR9k":
            list_vrf = {}
            list_vrf_ie = {}
            while i < total_lines:
                if re.match('vrf ', list_line[i]):
                    temp_vrf = VRF()
                    temp_vrf.Name = list_line[i].strip().split()[-1]
                    list_vrf[temp_vrf.Name] = temp_vrf
                    i += 1
                    j = i
                    while j < total_lines:
                        if ('vrf ' + temp_vrf.Name) in list_line[j]:
                            if (j + 1) < total_lines:
                                if re.match('rd ',list_line[j+1].strip()):
                                    temp_vrf.RD = list_line[j+1].strip().split(" ")[-1].strip()
                                    list_line[j+1] = '\n'
                                    break
                        j += 1
                    temp_seq_exp = 0
                    temp_seq_imp = 0
                    while list_line[i] != '!\n':
                        if list_line[i].strip() == 'import route-target':
                            list_line[i] = '\n'
                            i += 1
                            while '!' not in list_line[i]:
                                temp_vrf_ie = VRF_IE()
                                temp_vrf_ie.Name = temp_vrf.Name + "_default_imp"  # xem nhu policy import default
                                temp_vrf_ie.VRF_Name = temp_vrf.Name
                                temp_vrf_ie.Seq = temp_seq_imp
                                temp_vrf_ie.IE = "imp"
                                temp_vrf_ie.Action = ""
                                temp_vrf_ie.Extcomm = list_line[i].strip().split(" ")[-1].strip()
                                temp_seq_imp += 1
                                list_vrf_ie[temp_vrf_ie.Name + '/' + str(temp_vrf_ie.Seq) + '/' +
                                            temp_vrf_ie.IE] = temp_vrf_ie
                                list_line[i] = '\n'
                                i += 1
                            i -= 1
                        elif list_line[i].strip() == 'export route-target':
                            list_line[i] = '\n'
                            i += 1
                            while '!' not in list_line[i]:
                                temp_vrf_ie = VRF_IE()
                                temp_vrf_ie.Name = temp_vrf.Name + "_default_exp"  # xem nhu policy export default
                                temp_vrf_ie.VRF_Name = temp_vrf.Name
                                temp_vrf_ie.Seq = temp_seq_exp
                                temp_vrf_ie.ACL = ""
                                temp_vrf_ie.IE = "exp"
                                temp_vrf_ie.Action = "add"
                                temp_vrf_ie.Extcomm = list_line[i].strip().split(" ")[-1].strip()
                                temp_seq_exp += 1
                                list_vrf_ie[temp_vrf_ie.Name + '/' + str(temp_vrf_ie.Seq)
                                            + '/' + temp_vrf_ie.IE] = temp_vrf_ie
                                list_line[i] = '\n'
                                i += 1
                            i -= 1
                        i += 1
                i += 1
            i = 0
            for item in list_vrf:
                list_vrf[item].insert(cursor)
            for item in list_vrf_ie:
                list_vrf_ie[item].insert(cursor)
            while i < total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev == 'HW':
            dict_vrf_ie = {}
            while i < total_lines:
                if ("ip vpn-instance " in list_line[i]):
                    temp_vrf = VRF()
                # add VRF Name
                    temp_vrf.Name = list_line[i].strip().split(" ")[-1].strip()
                    f.write("\n")
                    i += 1
                    while list_line[i] != '#\n':
                        if re.match(' description (.*)\n',list_line[i]):
                            temp_vrf.description = re.match(' description (.*)\n',list_line[i]).groups()[0]
                            f.write("\n")
                        elif " route-distinguisher " in list_line[i]:
                            # add RD
                            temp_vrf.RD = list_line[i].strip().split(" ")[-1].strip()
                            temp_vrf.insert(cursor)
                            f.write("\n")
                        elif 'diffserv-mode ' in list_line[i]:
                            temp_vrf.classifier = list_line[i].strip().split()[-2]
                            temp_vrf.color = list_line[i].strip().split()[-1]
                            f.write("\n")
                        elif 'tnl-policy' in list_line[i]:
                            temp_vrf.tnl_policy = list_line[i].strip().split()[-1].strip()
                            f.write("\n")
                        elif re.match('  vpn-target (.*) export-extcommunity', list_line[i]):
                            temp_txt=re.match('  vpn-target (.*) export-extcommunity', list_line[i]).group(1)
                            for item in temp_txt.split():
                                if temp_vrf.Exp_extcom == '':
                                    temp_vrf.Exp_extcom = item
                                else:
                                    temp_vrf.Exp_extcom = temp_vrf.Exp_extcom +' '+ item
                            f.write("\n")
                        elif re.match('  vpn-target (.*) import-extcommunity', list_line[i]):
                            temp_txt = re.match('  vpn-target (.*) import-extcommunity', list_line[i]).group(1)
                            for item in temp_txt.split():
                                if temp_vrf.Imp_extcom == '':
                                    temp_vrf.Imp_extcom = item
                                else:
                                    temp_vrf.Imp_extcom = temp_vrf.Imp_extcom + ' ' + item
                            f.write("\n")
                        else:
                            f.write(list_line[i])
                        i += 1
                    i -= 1
                    #temp_vrf.showdata()
                    temp_vrf.insert(cursor)
                else:
                    f.write(list_line[i])

                i += 1
        else:
            print "Device is not support in this script"
        conn.commit()
    except MySQLdb.Error as error:
        print(error)
        for key in dict_vrf_ie:
            dict_vrf_ie[key].showdata()
    finally:
        f.close()
