from tldp_peer import TLDP_Peer
import MySQLdb
import os
import re


def get_tldp_peer_from_log(list_line, hostname, Dev, total_lines, log_path, conn, cursor):
    try:
        i = 0
        TLDP_Peer.Hostname = hostname
        if not os.path.exists(log_path + "Logs/TLDP_Peer"):
            os.mkdir(log_path + "Logs/TLDP_Peer")
        with open(log_path + "Logs/TLDP_Peer/" + hostname + ".txt", "w") as f:
            f.write("=========Get TLDP_Peer informations of routers==========\n")
        f = open(log_path + "Logs/TLDP_Peer/" + hostname + ".txt", "a")
        if Dev == "C76xx":
            while i < total_lines:
                if "mpls ldp neighbor" in list_line[i]:
                    temp_tldp_peer = TLDP_Peer()
                    temp_tldp_peer.IP = list_line[i].strip().split(" ")[3].strip()
                    temp_tldp_peer.PWD = "juniper@123"  # tam thoi
                    temp_tldp_peer.insert(cursor)
                    f.write("\n")
                else:
                    f.write(list_line[i])
                i += 1
        elif Dev == "ASR9k":
            while i < total_lines:
                if re.match('mpls ldp\n', list_line[i]):
                    i += 1
                    while (list_line[i] != ' neighbor\n') and (i < total_lines):
                        i += 1
                    i += 1
                    while (list_line[i] != ' !\n') and (i < total_lines):
                        if ':' in list_line[i]:
                            temp_tldp_peer = TLDP_Peer()
                            temp_tldp_peer.IP = list_line[i].strip().split(':')[0]
                            temp_tldp_peer.insert(cursor)
                            list_line[i] = '\n'
                        i += 1
                    break
                i += 1
            i = 0
            while i < total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev == "HW":
            list_tldp ={}
            while i < total_lines:
                if re.match('mpls ldp\n',list_line[i]):
                    while list_line[i]!='#\n':
                        #print 'Dang xu ly mpls ldp:', list_line[i]
                        if 'md5-password cipher' in list_line[i]:
                            temp_tldp_peer = TLDP_Peer()
                            temp_tldp_peer.IP = list_line[i].strip().split()[2]
                            temp_tldp_peer.PWD = list_line[i].strip().split()[3]
                            list_tldp[temp_tldp_peer.IP] = temp_tldp_peer
                        i += 1
                    i -= 1
                elif re.match('[\s]?mpls ldp remote-peer (.*)\n', list_line[i]):
                    temp_tldp_peer = TLDP_Peer()
                    while (list_line[i] != '#\n') and (i < total_lines):
                        #print 'Dang xu ly remote ldp:', list_line[i]
                        if 'mpls ldp remote-peer' in list_line[i]:
                            temp_tldp_peer.desc = list_line[i].strip().split()[-1]
                        elif 'remote-ip' in list_line[i]:
                            temp_tldp_peer.IP = list_line[i].strip().split()[-1]
                            list_line[i] = '\n'
                        i += 1
                    if temp_tldp_peer.IP in list_tldp:
                        list_tldp[temp_tldp_peer.IP].desc = temp_tldp_peer.desc
                    else:
                        list_tldp[temp_tldp_peer.IP] = temp_tldp_peer
                    i -= 1
                i += 1
            for key in list_tldp:
                if key!='':
                    list_tldp[key].insert(cursor)
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