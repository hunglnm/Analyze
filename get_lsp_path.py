from path import Path, Path_detail
import os
import re
import MySQLdb


def get_lsp_path_from_log(list_line,hostname,Dev,total_lines,log_path, conn, cursor):
    try:
        i = 0
        Path.Hostname = hostname
        Path_detail.Hostname = hostname
        if not os.path.exists(log_path + "Logs/LSP_Path"):
            os.mkdir(log_path + "Logs/LSP_Path")
        with open(log_path + "Logs/LSP_Path/" + hostname + ".txt", "w") as f:
            f.write("=========Get LSP Path informations of routers==========\n")
        if Dev == "C76xx":
            while i < total_lines:
                if re.match("ip explicit-path ",list_line[i].strip()):
                    temp_path_name = list_line[i].strip().split(" ")[-2].strip()
                    temp_path = Path()
                    temp_path.Name = temp_path_name
                    if list_line[i].strip().split()[-1]=='enable':
                        temp_path.Admin_status = True
                    temp_path.insert(cursor)
                    i += 1
                    temp_index = 0
                    while "!" not in list_line[i]:
                        if "next-address" in list_line[i]:
                            temp_path_detail = Path_detail()
                            temp_path_detail.Index_1 = temp_index
                            temp_path_detail.Name = temp_path_name
                            temp_path_detail.NH =list_line[i].strip().split()[-1]
                            temp_path_detail.Type = "next-address"
                            temp_path_detail.insert(cursor)
                            temp_index += 1
                            list_line[i]="\n"
                        elif "exclude-address" in list_line[i]:
                            temp_path_detail = Path_detail()
                            temp_path_detail.Index_1 = temp_index
                            temp_path_detail.Name = temp_path_name
                            temp_path_detail.NH = list_line[i].strip().split()[-1]
                            temp_path_detail.Type = "exclude-address"
                            temp_path_detail.insert(cursor)
                            temp_index += 1
                            list_line[i] = "\n"
                        i +=1
                i += 1

            i = 0
            f = open(log_path + "Logs/LSP_Path/" + hostname + ".txt", "a")
            while i<total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev == "ASR9k":
            while i < total_lines:
                if re.match('explicit-path name (.*)\n', list_line[i]):
                    temp_path_name = re.match('explicit-path name (.*)', list_line[i].strip()).groups()[0]
                    temp_path = Path()
                    temp_path.Name = temp_path_name
                    temp_path.Admin_status = True
                    temp_path.insert(cursor)
                    i += 1
                    while "!" not in list_line[i]:
                        temp_result= re.match('^ index ([\d]+)+ (next-address .*|exclude-address)?'
                                              ' ipv4 unicast (.*)\n',list_line[i])
                        if temp_result:
                            temp_path_detail = Path_detail()
                            temp_path_detail.Index_1 = temp_result.groups()[0]
                            temp_path_detail.Name = temp_path_name
                            temp_path_detail.NH = temp_result.groups()[2]
                            temp_path_detail.Type = temp_result.groups()[1]
                            temp_path_detail.insert(cursor)
                            list_line[i]="\n"
                        i +=1
                i += 1

            i = 0
            f = open(log_path + "Logs/LSP_Path/" + hostname + ".txt", "a")
            while i<total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev == 'HW':
            while i < total_lines:
                if re.match('^ explicit-path ([\S]*)\n',list_line[i]):
                    temp_search = re.match('^ explicit-path ([\S]*)\n',list_line[i]).groups()
                    temp_path = Path()
                    temp_path.Name = temp_search[0]
                    temp_path_name = temp_search[0]
                    temp_path.Admin_status=True
                    temp_path.insert(cursor)
                    list_line[i]='\n'
                    temp_index = 0
                    i +=1
                    while list_line[i]!='#\n':
                        if re.match('  next hop ((?:[\d]{1,3}[\.]){3}[\d]{1,3})\n',list_line[i]):
                            temp_search = re.match('  next hop ((?:[\d]{1,3}[\.]){3}[\d]{1,3})\n',list_line[i]).groups()
                            temp_path_detail = Path_detail()
                            temp_path_detail.Index_1 = temp_index
                            temp_path_detail.Name = temp_path_name
                            temp_path_detail.NH = temp_search[0]
                            temp_path_detail.insert(cursor)
                            temp_index += 1
                            list_line[i] = "\n"
                        i += 1
                    i -= 1
                i += 1
            i = 0
            f = open(log_path + "Logs/LSP_Path/" + hostname + ".txt", "a")
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