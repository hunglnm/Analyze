from sla import SLA
import MySQLdb
import os


def get_sla_from_log(list_line,hostname,Dev,total_lines,log_path, conn, cursor):
    try:
        i = 0
        print '---Check SLA---'
        SLA.Hostname = hostname
        if not os.path.exists(log_path + "Logs/SLA"):
            os.mkdir(log_path + "Logs/SLA")
        with open(log_path + "Logs/SLA/" + hostname + ".txt", "w") as f:
            f.write("=========Get SLA informations of routers==========\n")
        f = open(log_path + "Logs/SLA/" + hostname + ".txt", "a")
        if Dev == "C76xx":
            while i < total_lines:
                if ("ip sla " in list_line[i]) and ("schedule" not in list_line[i])and \
                        ("responder" not in list_line[i]) and("track" not in list_line[i]):
                    temp_sla = SLA()
                    temp_sla.SLA_ID = int(list_line[i].strip().split(" ")[2].strip())
                    f.write("\n")
                    i += 1
                    while ("ip sla " not in list_line[i]) and ("schedule" not in list_line[i])and("kron" not in list_line[i]):
                        if ("icmp" in list_line[i]) or ("path-echo" in list_line[i]):
                            if "source-ip" in list_line[i]:
                                temp_sla.Src = list_line[i].strip().split(" ")[3]
                            temp_sla.Dest = list_line[i].strip().split(" ")[1]
                            f.write("\n")
                        elif "vrf" in list_line[i]:
                            temp_sla.VRF_Name = list_line[i].strip().split(" ")[1]
                            f.write("\n")
                        elif "data-size" in list_line[i]:
                            temp_sla.Data_size = int(list_line[i].strip().split(" ")[-1])
                            f.write("\n")
                        elif "timeout" in list_line[i]:
                            temp_sla.Timeout = int(list_line[i].strip().split(" ")[-1])
                            f.write("\n")
                        elif "frequency" in list_line[i]:
                            temp_sla.Freq = int(list_line[i].strip().split(" ")[-1])
                            f.write("\n")
                        i += 1
                    if "schedule" in list_line[i]:
                        temp_sla.Start = list_line[i].strip().split(" ")[-1]
                        i +=1
                        f.write("\n")
                    i -=1
                    j=0
                    while j<total_lines:
                        if (list_line[j].strip().split(" ")[0].strip() == "track")and(\
                                    int(list_line[j].strip().split(" ")[4].strip()) ==temp_sla.SLA_ID):
                            temp_sla.Track=int(list_line[j].strip().split(" ")[1].strip())
                            f.write("\n")
                            break
                        j +=1
                    temp_sla.insert(cursor)
                else:
                    f.write(list_line[i])
                i += 1
        elif Dev == "ASR9k":
            while i < total_lines:
                f.write(list_line[i])
                i += 1
        elif Dev == 'HW':
            i = 0
            temp_sla_id = 0
            while i < total_lines:
                #print 'Test:',i,list_line[i]
                if 'nqa-server ' in list_line[i]:
                    #print 'Test:', i, list_line[i]
                    temp_sla = SLA()
                    temp_sla.SLA_ID = temp_sla_id
                    temp_sla_id += 1
                    temp_sla.test_type = list_line[i].strip().split()[1]
                    temp_sla.Src = list_line[i].strip().split()[2]
                    temp_sla.s_port = int(list_line[i].strip().split()[3])
                    #temp_sla.showdata()
                    temp_sla.insert(cursor)
                elif 'nqa ' in list_line[i]:
                    temp_sla = SLA()
                    temp_sla.SLA_ID = temp_sla_id
                    temp_sla_id += 1
                    temp_sla.probe = list_line[i].strip().split()[2]
                    temp_sla.test_name = list_line[i].strip().split()[3]
                    i += 1
                    while (list_line[i]!='#\n')and('nqa test-instance' not in list_line[i]):
                        if 'test-type' in list_line[i]:
                            temp_sla.test_type = list_line[i].strip().split()[-1]
                        elif 'lsp-tetunnel' in list_line[i]:
                            temp_sla.Src = list_line[i].strip().split()[-1]
                        elif 'destination-address ipv4' in list_line[i]:
                            temp_sla.Dest = list_line[i].strip().split()[-1]
                        elif 'destination-port ' in list_line[i]:
                            temp_sla.d_port = int(list_line[i].strip().split()[-1])
                        elif 'frequency' in list_line[i]:
                            temp_sla.Freq = int(list_line[i].strip().split()[-1])
                        elif 'datasize' in list_line[i]:
                            temp_sla.Data_size = int(list_line[i].strip().split()[-1])
                        elif 'fail-percent' in list_line[i]:
                            temp_sla.fail_percent = int(list_line[i].strip().split()[-1])
                        elif 'source-address ipv4' in list_line[i]:
                            temp_sla.Src = list_line[i].strip().split()[-1]
                        elif 'local-pw-id' in list_line[i]:
                            temp_sla.local_pw_id = int(list_line[i].strip().split()[-1])
                        elif ' start ' in list_line[i]:
                            temp_sla.Start = list_line[i].strip().split()[-1]
                        list_line[i]='\n'
                        i += 1
                    i -= 1
                    #temp_sla.showdata()
                    temp_sla.insert(cursor)
                i += 1
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