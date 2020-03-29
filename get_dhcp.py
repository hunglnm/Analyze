from dhcp import DHCP
from vrf import VRF
import pymysql
import os


def get_dhcp_from_log(list_line, hostname, Dev, total_lines, log_path, conn, cursor):
    # Connect and update database
    try:
        i = 0
        DHCP.Hostname = hostname
        VRF.Hostname = hostname
        DHCP.Exclude=""
        if not os.path.exists(log_path + "Logs/DHCP"):
            os.mkdir(log_path + "Logs/DHCP")
        with open(log_path + "Logs/DHCP/" + hostname + ".txt", "w") as f:
            f.write("=========Get DHCP informations of routers==========\n")
        f = open(log_path + "Logs/DHCP/" + hostname + ".txt", "a")
        if Dev == "C76xx":
            while i < total_lines:
                if ("ip dhcp " in list_line[i])and("relay" not in list_line[i]):
                    if "ip dhcp excluded" in list_line[i]:
                        DHCP.Exclude = DHCP.Exclude+";"+ list_line[i].strip().split(" ")[-1].strip()
                        f.write("\n")
                    elif "ip dhcp pool " in list_line[i]:
                        temp_dhcp = DHCP()
                        temp_dhcp.Name = list_line[i].strip().split(" ")[-1].strip()
                        f.write("\n")
                        i += 1
                        while "!" not in list_line[i]:
                            if " vrf " in list_line[i]:
                                temp_dhcp.VRF_Name = list_line[i].strip().split(" ")[-1].strip()
                                temp_vrf = VRF ()
                                temp_vrf.Name = temp_dhcp.VRF_Name
                                temp_vrf.DHCP_Server = True
                                temp_vrf.insert_dhcp_server(cursor)
                                f.write("\n")
                            elif " network " in list_line[i]:
                                temp_dhcp.NW = list_line[i].strip()[8:]
                                f.write("\n")
                            elif " default-router " in list_line[i]:
                                temp_dhcp.GW = list_line[i].strip().split(" ")[-1].strip()
                                f.write("\n")
                            elif " dns-server " in list_line[i]:
                                temp_dhcp.DNS = list_line[i].strip().split(" ")[-1].strip()
                                f.write("\n")
                            i += 1
                        temp_dhcp.insert(cursor)
                else:
                    f.write(list_line[i])
                i +=1
        elif Dev == "ASR9k":
            while i < total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev == 'HW':
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
