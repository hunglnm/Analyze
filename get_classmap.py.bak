from classmap import Classmap
import MySQLdb
import os
import re


def get_classmap_from_log(list_line, hostname, Dev, total_lines, log_path, conn, cursor):
    try:
        i = 0
        Classmap.Hostname = hostname
        if not os.path.exists(log_path + "Logs/Classmap"):
            os.mkdir(log_path + "Logs/Classmap")
        with open(log_path + "Logs/Classmap/" + hostname + ".txt", "w") as f:
            f.write("=========Get Classmap informations of routers==========\n")
        f = open(log_path + "Logs/Classmap/" + hostname + ".txt", "a")
        if Dev == "C76xx":
            while i < total_lines:
                if "class-map" in list_line[i]:
                    temp_classmap = Classmap()
                    temp_classmap.Name = list_line[i].strip().split(" ")[-1].strip()
                    temp_classmap.Cond = list_line[i].strip().split(" ")[1].strip()
                    temp_classmap.DSCP = ""
                    f.write("\n")
                    i += 1
                    while "class-map" not in list_line[i]:
                        if "mpls" in list_line[i]:
                            temp_classmap.MPLS = list_line[i].strip().split(" ")[-1].strip()
                            f.write("\n")
                        elif "precedence" in list_line[i]:
                            if temp_classmap.IP_Pre =="" :
                                temp_classmap.IP_Pre = list_line[i].strip().split(" ")[-1].strip()
                            else :
                                temp_classmap.IP_Pre = temp_classmap.IP_Pre +" "+ list_line[i].strip().split(" ")[-1].strip()
                            f.write("\n")
                        elif "dscp" in list_line[i]:
                            if temp_classmap.DSCP == "":
                                temp_classmap.DSCP = list_line[i].strip().split(" ")[-1].strip()
                            else:
                                temp_classmap.DSCP = temp_classmap.DSCP + " " + list_line[i].strip().split(" ")[-1].strip()
                            f.write("\n")
                        elif "cos" in list_line[i]:
                            temp_classmap.CoS = list_line[i].strip().split(" ")[-1].strip()
                            f.write("\n")
                        elif "access-group" in list_line[i]:
                            temp_classmap.ACL = list_line[i].strip().split(" ")[-1].strip()
                            f.write("\n")
                        elif "!" in list_line[i]:
                            f.write(list_line[i])
                            break
                        i += 1
                    #temp_classmap.showdata()
                    temp_classmap.insert(cursor)
                    if "class-map" in list_line[i] :
                        i -= 1
                else:
                    f.write(list_line[i])
                i += 1
        elif Dev == "ASR9k":
            while i < total_lines:
                if re.match("class-map ", list_line[i]):
                    temp_classmap = Classmap()
                    temp_classmap.Name = list_line[i].strip().split(" ")[-1].strip()
                    temp_classmap.Cond = list_line[i].strip().split(" ")[1].strip()
                    temp_classmap.DSCP = ""
                    f.write("\n")
                    i += 1
                    while "end-class-map" not in list_line[i]:
                        if "mpls" in list_line[i]:
                            temp_classmap.MPLS = list_line[i].strip().split(" ")[-1].strip()
                            f.write("\n")
                        elif "precedence" in list_line[i]:
                            if temp_classmap.IP_Pre == "":
                                temp_classmap.IP_Pre = list_line[i].strip().split(" ")[-1].strip()
                            else:
                                temp_classmap.IP_Pre = temp_classmap.IP_Pre + " " + list_line[i].strip().split(" ")[
                                    -1].strip()
                            f.write("\n")
                        elif "dscp" in list_line[i]:
                            if temp_classmap.DSCP == "":
                                temp_classmap.DSCP = list_line[i].strip().split(" ")[-1].strip()
                            else:
                                temp_classmap.DSCP = temp_classmap.DSCP + " " + list_line[i].strip().split(" ")[
                                    -1].strip()
                            f.write("\n")
                        elif "cos" in list_line[i]:
                            temp_classmap.CoS = list_line[i].strip().split(" ")[-1].strip()
                            f.write("\n")
                        elif "access-group" in list_line[i]:
                            temp_classmap.ACL = list_line[i].strip().split(" ")[-1].strip()
                            f.write("\n")
                        elif "!" in list_line[i]:
                            f.write(list_line[i])
                            break
                        i += 1
                    if 'end-class-map' in list_line[i]:
                        list_line[i]='\n'
                    #temp_classmap.showdata()
                    temp_classmap.insert(cursor)
                else:
                    f.write(list_line[i])
                i += 1
        elif Dev == 'HW':
            list_class = {}
            while i < total_lines:
                if re.match("traffic classifier ", list_line[i]):
                    temp_classmap = Classmap()
                    temp_classmap.Name = list_line[i].strip().split()[2]
                    temp_classmap.or_and = list_line[i].strip().split()[-1]
                    i += 1
                    while (list_line[i]!='#\n')and('traffic classifier' not in list_line[i]):
                        #print i,list_line[i]
                        if 'if-match' in list_line[i]:
                            if ' any' in list_line[i]:
                                temp_classmap.Cond = 'any'
                            elif ' acl name ' in list_line[i]:
                                if temp_classmap.ACL == '':
                                    temp_classmap.ACL = list_line[i].strip().split()[-1]
                                else:
                                    temp_classmap.ACL = temp_classmap.ACL + ' ' + list_line[i].strip().split()[-1]
                            elif ' acl ' in list_line[i]:
                                if temp_classmap.ACL == '':
                                    temp_classmap.ACL = list_line[i].strip().split()[-1]
                                else:
                                    temp_classmap.ACL = temp_classmap.ACL + ' ' + list_line[i].strip().split()[-1]
                            elif ' dscp ' in list_line[i]:
                                if temp_classmap.DSCP == '':
                                    temp_classmap.DSCP = list_line[i].strip().split()[-1]
                                else:
                                    temp_classmap.DSCP = temp_classmap.DSCP + ' ' + list_line[i].strip().split()[-1]
                        i += 1
                    list_class[temp_classmap.Name] = temp_classmap
                    i -= 1
                i += 1
            for key in list_class:
                #list_class[key].showdata()
                list_class[key].insert(cursor)
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