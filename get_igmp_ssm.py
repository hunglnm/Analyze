from igmp_ssm import IGMP_SSM
import pymysql
import os
import re


def get_igmp_ssm_from_log(list_line, hostname, Dev, total_lines, log_path, f_file, conn, cursor):
    try:
        i = 0
        IGMP_SSM.Hostname = hostname
        if not os.path.exists(log_path + "Logs/IGMP_SSM"):
            os.mkdir(log_path + "Logs/IGMP_SSM")
        with open(log_path + "Logs/IGMP_SSM/" + hostname + ".txt", "w") as f:
            f.write("=========Get IGMP SSM informations of routers==========\n")
        f = open(log_path + "Logs/IGMP_SSM/" + hostname + ".txt", "a")
        if Dev == "C76xx":
            while i < total_lines:
                if "ip igmp ssm-map static" in list_line[i]:
                    temp_igmp_ssm = IGMP_SSM()
                    temp_igmp_ssm.ACL = list_line[i].strip().split(" ")[4].strip()
                    temp_igmp_ssm.Source = list_line[i].strip().split(" ")[-1].strip()
                    f.write("\n")
                    temp_igmp_ssm.insert(cursor)
                else:
                    f.write(list_line[i])
                i += 1
        elif Dev == "ASR9k":
            tmp_str = re.search('ssm range (.*)\n', f_file)
            if tmp_str is not None:
                temp_igmp_ssm = IGMP_SSM()
                temp_igmp_ssm.ACL = tmp_str.groups()[0]
                f_file = re.sub('ssm range (.*)\n', '\n', f_file)
                temp_igmp_ssm.insert(cursor)
            f.write(f_file)
        elif Dev == 'HW':
            while i < total_lines:
                if re.search('^ ssm-mapping (.*)\n',list_line[i]):
                    tmp_str = re.search(' ssm-mapping (.*)\n',list_line[i])
                    #print 'Bi loi gi :',list_line[i],tmp_str.group(1)
                    if tmp_str is not None:
                        temp_igmp_ssm = IGMP_SSM()
                        tmp_str_list = tmp_str.group(1).split()
                        temp_igmp_ssm.ACL = tmp_str_list[0] + '/' + tmp_str_list[1]
                        temp_igmp_ssm.Source = tmp_str_list[2]
                        temp_igmp_ssm.insert(cursor)
                        f.write("\n")
                else:
                    f.write(list_line[i])
                i += 1
        else:
            print("Device is not support in this script")
        conn.commit()
    except pymysql.Error as error:
        print(error)
    finally:
        f.close()
