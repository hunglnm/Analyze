from vlan import VLAN
import MySQLdb
import os


def get_vlan_from_log(list_line,hostname,Dev,total_lines,log_path,conn, cursor):
    try:
        i = 0
        VLAN.Hostname = hostname
        if not os.path.exists(log_path + "Logs/VLAN"):
            os.mkdir(log_path + "Logs/VLAN")
        with open(log_path + "Logs/VLAN/" + hostname + ".txt", "w") as f:
            f.write("=========Get VLAN informations of routers==========\n")
        f = open(log_path + "Logs/VLAN/" + hostname + ".txt", "a")
        if Dev == "C76xx":
            while i < total_lines:
                if ("vlan" == list_line[i].strip().split(" ")[0].strip()) and ("internal" not in list_line[i]) and (
                                                                                "access" not in list_line[i]):
                    vlans = list_line[i].strip().split(" ")[1].strip()
                    vlan_list = vlans.strip().split(",")
                    f.write("\n")
                    i += 1
                    temp_description=""
                    while "!" not in list_line[i]:
                        if "name" in list_line[i]:
                            temp_description = list_line[i].strip()[5:]
                            f.write("\n")
                        i += 1
                    for num in range(len(vlan_list)):
                        if vlan_list[num].isdigit():
                            temp_vlan = VLAN()
                            temp_vlan.Vlan = int(vlan_list[num])
                            temp_vlan.Description = temp_description
                            temp_vlan.insert(cursor)
                        elif "-" in vlan_list[num]:
                            min_vlan = int(vlan_list[num].split("-")[0])
                            max_vlan = int(vlan_list[num].split("-")[1])
                            j_vlan = min_vlan
                            while j_vlan < (max_vlan + 1):
                                temp_vlan = VLAN()
                                temp_vlan.Vlan = j_vlan
                                temp_vlan.Description = vlan_list[num]
                                temp_vlan.insert(cursor)
                                j_vlan += 1
                elif "mac-address-table aging-time" in list_line[i]:
                    temp_vlan_val = list_line[i].strip().split(" ")[-1].strip()
                    if temp_vlan_val.isdigit():
                        temp_vlan = VLAN()
                        temp_vlan.Vlan = temp_vlan_val
                        temp_vlan.L2_age_time = int(list_line[i].strip().split(" ")[2].strip())
                        temp_vlan.insert(cursor)
                        f.write("\n")
                else:
                    f.write(list_line[i])
                i += 1
        elif Dev == "ASR9k":
            while i < total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev == 'HW':
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
