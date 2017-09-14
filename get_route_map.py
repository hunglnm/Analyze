from route_map  import Route_map
from mysql.connector import MySQLConnection,Error
import mysql.connector
import os
import re
import MySQLdb

def IsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def get_route_map_from_log(list_line,hostname,Dev,total_lines,log_path,conn,cursor):
    try:
        i = 0
        Route_map.Hostname = hostname
        if not os.path.exists(log_path + "Logs/Route_map"):
            os.mkdir(log_path + "Logs/Route_map")
        with open(log_path + "Logs/Route_map/" + hostname + ".txt", "w") as f:
            f.write("=========Get Route Map informations of routers==========\n")

        if Dev == "C76xx":
            while i < total_lines:
                if "route-map" == list_line[i].strip().split(" ")[0]:
                    while "!" not in list_line[i]:
                        if "route-map" in list_line[i]:
                            temp_route_map = Route_map()
                            temp_route_map.Name = list_line[i].strip().split(" ")[1]
                            temp_route_map.Seq = list_line[i].strip().split(" ")[-1]
                        elif "match ip" in list_line[i]:
                            temp_route_map.ACL = list_line[i].strip().split(" ")[-1]
                        elif "set extcommunity rt" in list_line[i]:
                            if "additive" in list_line[i]:
                                temp_route_map.Extcomm = list_line[i].strip().split(" ")[-2]
                                temp_route_map.Action_1 ='additive'
                            else:
                                temp_route_map.Extcomm = list_line[i].strip().split(" ")[-1]
                        i +=1
                    temp_route_map.insert(cursor)
                i += 1

            i = 0
            f = open(log_path + "Logs/Route_map/" + hostname + ".txt", "a")
            while i<total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev == "ASR9k":
            while i < total_lines:
                if re.match('route-policy (.*)\n',list_line[i]):
                    print re.match('route-policy (.*)\n',list_line[i]).groups()
                    temp_route_map_name = re.match('route-policy (.*)\n',list_line[i]).groups()[0]
                    temp_Seq = 0
                    temp_create_route_map = True
                    temp_route_map = Route_map()
                    i += 1
                    while list_line[i] != 'end-policy\n':
                        if temp_create_route_map:
                            temp_route_map = Route_map()
                            temp_route_map.Name = temp_route_map_name
                            temp_route_map.Seq = temp_Seq
                            temp_create_route_map = False
                        if "if extcommunity rt" in list_line[i]:
                            temp_extcomm = list_line[i].strip().split()[4]
                            list_line[i] = '\n'
                            temp_extcomm_list = ''

                            j = 0
                            while j < total_lines:
                                if re.match('extcommunity-set rt '+temp_extcomm+'\n',list_line[j]):
                                    while list_line[j] != '!\n':
                                        if re.match('^  (?:.* )?([\']?\d+\:\d+(?:\.\*\'?)?).*\n',list_line[j]):
                                            temp_result = re.match('^  (?:.* )?([\']?\d+\:\d+(?:\.\*\')?).*\n',
                                                                   list_line[j])
                                            if temp_extcomm_list !='':
                                                temp_extcomm_list = temp_extcomm_list + ' ' + \
                                                                    temp_result.groups()[0]
                                            else:
                                                temp_extcomm_list = temp_result.groups()[0]
                                            list_line[j]='\n'
                                        j += 1
                                    break
                                j += 1
                            temp_route_map.Extcomm = temp_extcomm_list
                        elif "pass" in list_line[i]:
                            temp_route_map.Action_1 = 'accept'
                            temp_create_route_map = True
                            temp_route_map.insert(cursor)
                            temp_Seq += 1
                            list_line[i] = '\n'
                        elif "drop" in list_line[i]:
                            temp_route_map.Action_1 = 'reject'
                            temp_create_route_map = True
                            temp_route_map.insert(cursor)
                            temp_Seq += 1
                            list_line[i] = '\n'
                        i += 1
                i += 1
            i = 0
            f = open(log_path + "Logs/Route_map/" + hostname + ".txt", "a")
            while i<total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev =='HW':
            i = 0
            f = open(log_path + "Logs/Route_map/" + hostname + ".txt", "a")
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