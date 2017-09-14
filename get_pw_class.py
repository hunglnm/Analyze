from pw_class import PW_Class
import MySQLdb
import os
import re


def get_pw_class_from_log(list_line,hostname,Dev,total_lines,log_path, conn, cursor):
    try:
        i = 0
        PW_Class.Hostname = hostname
        if not os.path.exists(log_path + "Logs/PW_Class"):
            os.mkdir(log_path + "Logs/PW_Class")
        with open(log_path + "Logs/PW_Class/" + hostname + ".txt", "w") as f:
            f.write("=========Get PW_Class informations of routers==========\n")
        f = open(log_path + "Logs/PW_Class/" + hostname + ".txt", "a")
        if Dev == "C76xx":
            while i < total_lines:
                if "pseudowire-class" == list_line[i].strip().split(" ")[0].strip():
                    temp_pw_class = PW_Class()
                    temp_pw_class.Name = list_line[i].strip().split(" ")[1].strip()
                    f.write("\n")
                    i += 1
                    while "!" not in list_line[i]:
                        if "preferred-path interface" in list_line[i]:
                            temp_pw_class.LSP = list_line[i].strip().split(" ")[-1].strip()
                        f.write("\n")
                        i += 1
                    if "!" in list_line[i]:
                        f.write(list_line[i])
                        temp_pw_class.insert(cursor)
                else:
                    f.write(list_line[i])
                i += 1
        elif Dev == "ASR9k":
            while i < total_lines:
                f.write(list_line[i])
                i +=1
        elif Dev == 'HW':
            list_pw_class = {}
            while i<total_lines:
                if re.match('tunnel-policy .*',list_line[i]):
                    temp_pw_class_name = list_line[i].strip().split()[-1]

                    i += 1
                    while list_line[i]!='#\n':
                        if re.match(' tunnel binding destination (.*) te (.*)\n',list_line[i]):
                            #print temp_pw_class_name
                            temp_pw_class = PW_Class()
                            temp_pw_class.Name = temp_pw_class_name
                            temp_list = re.match(' tunnel binding destination (.*) te (.*)\n',list_line[i]).groups()
                            #print temp_list
                            temp_pw_class.LSP = temp_list[1].strip()
                            temp_pw_class.Dest = temp_list[0].strip()
                            list_pw_class[temp_pw_class.Name]=temp_pw_class
                            list_line[i]='\n'
                        i += 1
                    i -= 1
                i +=1
            for key in list_pw_class:
                list_pw_class[key].insert(cursor)
            i = 0
            while i < total_lines:
                f.write(list_line[i])
                i +=1
        else:
            print "Device is not support in this script"
        conn.commit()
    except MySQLdb.Error as error:
        print(error)
    finally:
        f.close()