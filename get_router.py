from router import Router
import pymysql
import re
import os


def get_hostname_from_txt(list_line, total_lines):
    hostname = ''
    dev_type = ''
    host_dev = []
    i = 0
    while i<total_lines:
        if list_line[i].strip() !='':
            if list_line[i].strip().split()[0] == "hostname":
                hostname = list_line[i].strip().split(" ")[1]
                break
            elif list_line[i].strip().split()[0] == "sysname":
                hostname = list_line[i].strip().split()[1]
                dev_type = 'HW'
                break
        i += 1
    if dev_type == '':
        if "760" in hostname:
            dev_type = "C76xx"
        elif "ASR9" in hostname:
            dev_type = "ASR9k"
        else:
            print("Script not support for this device ")
    host_dev.append(hostname)
    host_dev.append(dev_type)
    return host_dev


def get_router_from_txt(list_line, hostname, Dev, total_lines, log_path, conn, cursor):
    i = 0
    Router.Hostname = hostname
    temp_router = Router(hostname)
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    with open(log_path + hostname + ".txt", "w") as f:
        f.write("=========Get general informations of routers==========\n")
    f = open(log_path + hostname + ".txt", "a")
    if Dev == "C76xx":
        while i < total_lines:
            if list_line[i].strip().split(" ")[0] == "hostname":
                temp_router.Device = Dev
                f.write("\n")
            elif "clock timezone " in list_line[i]:
                temp_router.Timezone = "GMT 7"
                f.write("\n")
            elif "ip dhcp relay information option" == list_line[i].strip():
                temp_router.DHCP_Relay = True
                f.write("\n")
            elif "ip multicast" in list_line[i]:
                temp_router.Multicast = True
                f.write("\n")
            elif "ip igmp ssm-map enable" in list_line[i]:
                temp_router.IGMP_SSM = True
                f.write("\n")
            elif "mpls ldp session protection" in list_line[i]:
                temp_router.LDP_Session_Protect = True
                f.write("\n")
            elif "mpls traffic-eng tunnels" in list_line[i]:
                temp_router.TE = True
                f.write("\n")
            elif "mpls ldp router-id" in list_line[i]:
                temp_router.RID = list_line[i].strip().split(" ")[3]
                f.write("\n")
            elif "snmp-server community" in list_line[i]:
                temp_router.SNMP_Comm = list_line[i].strip().split(" ")[2]
                f.write("\n")
            elif "snmp-server trap-source" in list_line[i]:
                temp_router.SNMP_Trap = True
                f.write("\n")
            elif " transport input telnet ssh" in list_line[i]:
                temp_router.Login = "telnet/ssh"
                f.write("\n")
            elif ("mac-address-table aging-time" in list_line[i])and("vlan" not in list_line[i]):
                temp_router.L2_age_time = list_line[i].strip().split(" ")[2]
                f.write("\n")
            else:
                f.write(list_line[i])
            i +=1
    elif Dev == "ASR9k":
        while i < total_lines:
            if len(list_line[i].strip())>0:
                if list_line[i].strip().split()[0] == "hostname":
                    temp_router.Device = Dev
                    list_line[i] = "\n"
                elif "clock timezone " in list_line[i]:
                    temp_router.Timezone = list_line[i].strip()[len('clock timezone '):]
                    list_line[i] = "\n"
                elif "multicast-routing" in list_line[i]:
                    temp_router.Multicast = True
                elif "router igmp" in list_line[i]:
                    temp_router.IGMP_SSM = True
                elif "router pim" in list_line[i]:
                    temp_router.PIM = True
                elif re.match('mpls ldp',list_line[i].strip()):
                    while not re.match('!',list_line[i]):
                        if list_line[i].strip()=='session protection':
                            temp_router.LDP = True
                            temp_router.LDP_Session_Protect = True
                            list_line[i]='\n'
                            break
                        i += 1
                elif list_line[i].strip()=='mpls traffic-eng':
                    temp_router.TE = True
                elif re.match('router-id',list_line[i].strip()):
                    temp_router.RID = list_line[i].strip().split()[-1]
                    list_line[i] = "\n"
                elif "snmp-server community" in list_line[i]:
                    temp_router.SNMP_Comm = list_line[i].strip().split()[2]
                    list_line[i] = "\n"
                elif "telnet vrf " in list_line[i]:
                    temp_router.Login = "telnet"
                    list_line[i] = "\n"
            i += 1
        i = 0
        while i<total_lines:
            f.write(list_line[i])
            i += 1
    elif Dev == 'HW':
        temp_router.Timezone = "GMT 7"
        while i < total_lines:
            if len(list_line[i].strip())>0:
                if list_line[i].strip().split()[0] == "sysname":
                    temp_router.Device = Dev
                elif "multicast routing-enable" in list_line[i]:
                    temp_router.Multicast = True
                    temp_router.IGMP_SSM = True
                    temp_router.PIM = True
                    list_line[i]= '\n'
                elif 'loop-detection enable' in list_line[i]:
                    temp_router.loop_detect = True
                    list_line[i] = '\n'
                elif list_line[i] == 'bfd\n':
                    if 'mpls-passive' in list_line[i+1]:
                        temp_router.bfd_mpls = True
                        list_line[i] = '\n'
                        list_line[i+1] = '\n'
                elif re.match('mpls\n',list_line[i]):
                    if re.match(' mpls te\n',list_line[i+1]):
                        temp_router.TE = True
                        list_line[i] =='\n'
                        list_line[i + 1] = '\n'
                elif re.match('mpls lsr-id',list_line[i].strip()):
                    temp_router.RID = list_line[i].strip().split()[-1]
                    list_line[i] = "\n"
                elif 'dhcp snooping enable' in list_line[i]:
                    temp_router.DHCP_Snoop = True
                    list_line[i] = '\n'
                elif "service-type telnet ssh" in list_line[i]:
                    temp_router.Login = "telnet ssh"
                    list_line[i] = '\n'
                elif "service-type ftp telnet" in list_line[i]:
                    temp_router.Login = "ftp telnet"
                    list_line[i] = '\n'
                elif "service-type telnet" in list_line[i]:
                    temp_router.Login = "telnet"
                    list_line[i] = '\n'
                elif re.match('[\s]?snmp-agent community read  ([\S]+) acl ([\S]+)\n',list_line[i]):
                    temp_search = re.match('[\s]?snmp-agent community read  ([\S]+) acl ([\S]+)\n',list_line[i]).groups()
                    temp_router.SNMP_Comm = temp_search[0]
                    list_line[i]='\n'
            i += 1
        i=0
        while i<total_lines:
            #print 'Cac gia tri duoc luu:',list_line[i]
            f.write(list_line[i])
            i += 1
    else:
        print("Device is not support in this script")
        # Connect and update database
    try:
        temp_router.insert(cursor)
        conn.commit()
    except pymysql.Error as error:
        print(error)
    finally:
        f.close()
