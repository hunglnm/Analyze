from server import  Server
import MySQLdb
import os
import re


def get_server_from_log(list_line,hostname,Dev,total_lines,log_path, conn, cursor):
    try:
        i = 0
        Server.Hostname = hostname
        if not os.path.exists(log_path + "Logs/Server"):
            os.mkdir(log_path + "Logs/Server")
        with open(log_path + "Logs/Server/" + hostname + ".txt", "w") as f:
            f.write("=========Get Server informations of routers==========\n")
        f = open(log_path + "Logs/Server/" + hostname + ".txt", "a")
        list_server = {}
        if Dev == "C76xx":
            while i < total_lines:
                if "snmp-server host " in list_line[i]:
                    temp_server = Server()
                    temp_server.IP = list_line[i].strip().split(" ")[2]
                    temp_server.Purpose = "SNMP-Trap"
                    list_server[temp_server.IP] = temp_server
                    list_line[i]='\n'
                elif "tacacs-server host" in list_line[i]:
                    temp_server = Server()
                    temp_server.IP = list_line[i].strip().split(" ")[2]
                    temp_server.Purpose = "TACACS"
                    list_server[temp_server.IP] = temp_server
                    list_line[i] = '\n'
                elif "ntp server" in list_line[i]:
                    temp_server = Server()
                    temp_server.IP = list_line[i].strip().split(" ")[2]
                    temp_server.Purpose = "NTP"
                    list_server[temp_server.IP] = temp_server
                    list_line[i] = '\n'
                elif ("logging" == list_line[i].strip().split(" ")[0]) and ("." in list_line[i]):
                    temp_server = Server()
                    temp_server.IP = list_line[i].strip().split(" ")[-1].strip()
                    temp_server.Purpose = "logging"
                    list_server[temp_server.IP] = temp_server
                    list_line[i] = '\n'
                i += 1
            for item in list_server:
                list_server[item].insert(cursor)
            i = 0
            while i < total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev == "ASR9k":
            temp_source_logging = ''
            temp_source_tacacs = ''
            while i < total_lines:
                if "tacacs-server host" in list_line[i]:
                    temp_server = Server()
                    temp_server.IP = list_line[i].strip().split(" ")[2]
                    temp_server.Purpose = "TACACS"
                    list_server[temp_server.IP] = temp_server
                    list_line[i] = '\n'
                elif "ntp\n" in list_line[i]:
                    while list_line[i] != '!\n':
                        if re.match('^ server .*\n',list_line[i]):
                            temp_server = Server()
                            temp_server.IP = list_line[i].strip().split()[1]
                            temp_server.Purpose = "NTP"
                            temp_server.Source = list_line[i].strip().split()[-1]
                            list_server[temp_server.IP] = temp_server
                            list_line[i] = '\n'
                        i += 1
                elif ("logging" == list_line[i].strip().split(" ")[0]) and ("." in list_line[i]):
                    temp_server = Server()
                    temp_server.IP = list_line[i].strip().split(" ")[1].strip()
                    temp_server.Purpose = "logging"
                    list_server[temp_server.IP] = temp_server
                    list_line[i] = '\n'
                elif 'logging source-interface' in list_line[i]:
                    temp_source_logging = list_line[i].strip().split()[-1].strip()
                    list_line[i] = '\n'
                elif 'tacacs source-interface' in list_line[i]:
                    temp_source_tacacs = list_line[i].strip().split()[2].strip()
                    list_line[i] = '\n'
                i += 1
            for item in list_server:
                if list_server[item].Purpose == 'logging':
                    list_server[item].Source = temp_source_logging
                elif list_server[item].Purpose == 'TACACS':
                    list_server[item].Source = temp_source_tacacs

                list_server[item].insert(cursor)
            i = 0
            while i < total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev == 'HW':
            temp_log_source = ''
            temp_ntp_acl = ''
            temp_snmp_acl = ''
            temp_snmp_source = ''
            while i < total_lines:
                if re.match('[\s]?ntp-service unicast-server ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) source-interface ([\S]+)'
                              '( preference)?\n',list_line[i]):
                    temp_search = re.match('[\s]?ntp-service unicast-server ((?:[\d]{1,3}[\.]){3}[\d]{1,3}) '
                                           'source-interface ([\S]+)( preference)?\n',list_line[i]).groups()
                    temp_server = Server()
                    temp_server.IP = temp_search[0]
                    temp_server.Purpose = "NTP"
                    temp_server.Source = temp_search[1]
                    temp_server.ACL = temp_ntp_acl
                    list_server['NTP/'+temp_server.IP] = temp_server
                    list_line[i] = '\n'
                elif re.match('[\s]?ntp-service access query ([\S]*)\n',list_line[i]):
                    temp_search=re.match('[\s]?ntp-service access query ([\S]*)\n',list_line[i]).groups()
                    temp_ntp_acl = temp_search[0]
                    list_line[i] = '\n'
                elif re.match('[\s]?snmp-agent target-host trap  address udp-domain '
                              '((?:[\d]{1,3}[\.]){3}[\d]{1,3}) .*\n',list_line[i]):
                    temp_search = re.match('[\s]?snmp-agent target-host trap  address udp-domain '
                              '((?:[\d]{1,3}[\.]){3}[\d]{1,3}) .*\n',list_line[i]).groups()
                    temp_server = Server()
                    temp_server.IP = temp_search[0]
                    temp_server.Purpose = "SNMP_Trap"
                    list_server['SNMP_Trap/' + temp_server.IP] = temp_server
                    list_line[i] = '\n'
                elif re.match('[\s]?snmp-agent trap source ([\S]+)\n',list_line[i]):
                    temp_search = re.match('[\s]?snmp-agent trap source ([\S]+)\n',list_line[i]).groups()
                    temp_snmp_source = temp_search[0]
                    list_line[i] = '\n'
                elif re.match('[\s]?info-center loghost source ([\S]+)\n',list_line[i]):
                    temp_log_source = re.match('[\s]?info-center loghost source ([\S]+)\n',list_line[i]).groups()[0]
                    list_line[i] = '\n'
                elif re.match('[\s]?info-center loghost ((?:[\d]{1,3}[\.]){3}[\d]{1,3})\n',list_line[i]):
                    temp_search = re.match('[\s]?info-center loghost ((?:[\d]{1,3}[\.]){3}[\d]{1,3})\n',
                                           list_line[i]).groups()
                    temp_server = Server()
                    temp_server.IP = temp_search[0]
                    temp_server.Purpose = "Logging"
                    list_server['Logging/' + temp_server.IP] = temp_server
                    list_line[i] = '\n'
                elif re.match(' set save-configuration backup-to-server server (([\d]{1,3}[\.]){3}[\d]{1,3}) '
                              'user ([\S]+) password [\S]+ path .*\n',list_line[i]):
                    temp_search=re.match(' set save-configuration backup-to-server server (([\d]{1,3}[\.]){3}[\d]{1,3}) '
                            'user ([\S]+) password [\S]+ path .*\n', list_line[i]).groups()
                    temp_server = Server()
                    temp_server.IP = temp_search[0]
                    temp_server.Purpose = "FTP"
                    list_server['FTP/' + temp_server.IP] = temp_server
                    list_line[i] = '\n'
                i += 1
            for item in list_server:
                if list_server[item].Purpose == 'Logging':
                    list_server[item].Source = temp_log_source
                elif list_server[item].Purpose == 'SNMP_Trap':
                    list_server[item].Source = temp_snmp_source
                elif list_server[item].Purpose == 'NTP':
                    list_server[item].ACL = temp_ntp_acl
                #list_server[item].showdata()
                list_server[item].insert(cursor)
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