#May-08-2020
import datetime
import time
from get_router import *
from get_vrf import *
from get_dhcp import *
from get_igmp_ssm import *
from get_sla import  *
from get_tldp_peer import *
from get_vlan import *
from get_classmap import *
from get_policy_map import *
from get_pw_class import *
from get_l2vpn import *
from get_interface import *
from get_routing import *
from get_lsp_path import *
from get_acl import *
from get_server import *
from get_route_map import *
import pymysql
from get_policy_db import *


def about_router(s_path, conn, cursor):
    ifile = 0
    dirs = os.listdir(s_path)
    with open(s_path + "selected_files.txt", "w") as f:
        f.write(str(datetime.datetime.now().date())+"---Router---")
    check_continue = "y"
    for file in dirs:
        print(file)
        file_name_cnf = file
        complete_path = s_path + file_name_cnf
        # how many lines in this file ?
        if os.path.isfile(complete_path):
            with open(complete_path, "r") as f:
                numlines = sum(1 for line in f)
            print("Total command lines on cisco routers : ", numlines)
            # split the file to lines
            with open(complete_path, "r") as f:
                f_line = f.readlines()
            host_dev = get_hostname_from_txt(f_line, numlines)
            Hostname = host_dev[0]
            Device = host_dev[1]
            s_notification = ""
            if Hostname == "":
                print("Please check file:", file)
                s_notification = "Please check this file:missing hostname"
            else:
                if Device == '':
                    print("Please check file:", file)
                    s_notification = "Please check this file:cannot detect type of router"
                else:
                    print("Processing for ", Hostname)
                    print(Device)
                    delete_db(Hostname, conn, cursor)
                    log_path = s_path + "Logs/"
                    get_router_from_txt(f_line, Hostname, Device, numlines, log_path, conn, cursor)
                    #check_continue = raw_input("Do you continue?")
                    #if check_continue == "n":
                    #    break
            with open(s_path + "selected_files.txt", "a") as f:
                f.write(str(datetime.datetime.now().date()) + "/" + str(ifile)+ ">" + file + "(" + s_notification + ")\n")
            ifile += 1


def about_vrf(s_path,conn ,cursor):
    ifile = 0
    s_path1 = s_path + "Logs/"
    dirs = os.listdir(s_path1)
    with open(s_path + "selected_files.txt", "w") as f:
        f.write(str(datetime.datetime.now().date())+"---VRF---")
    check_continue = "y"
    for file in dirs:
        print(file)
        file_name_cnf = file
        complete_path = s_path1 + file_name_cnf
        # how many lines in this file ?
        if os.path.isfile(complete_path):
            f_file = ''
            with open(complete_path, "r") as f:
                numlines = sum(1 for line in f)
            print("Total command lines on cisco routers : ", numlines)
            # split the file to lines
            with open(complete_path, "r") as f:
                f_line = f.readlines()
            with open(complete_path,'r') as f:
                f_file = f.read()
            host_dev = get_hostname_from_txt(f_line, numlines)
            Hostname = host_dev[0]
            Device = host_dev[1]
            #print("line 92 in main.py",Device)
            s_notification = ""
            if Device == "":
                print("Please check file:", file)
                s_notification = "Please check this file"
            else:
                #print s_path1
                get_vrf_from_log(f_line, Hostname, Device, numlines, s_path1, f_file, conn ,cursor)
                #check_continue = raw_input("Do you continue?")
                #if check_continue == "n":
                #    break
            with open(s_path + "selected_files.txt", "a") as f:
                f.write(str(datetime.datetime.now().date()) + "/" +\
                        str(ifile) + ">" + file + "(" + s_notification + ")\n")
        ifile += 1


def about_dhcp(s_path, conn, cursor):
    ifile = 0
    s_path1 = s_path + "Logs/VRF/"
    dirs = os.listdir(s_path1)
    with open(s_path + "selected_files.txt", "w") as f:
        f.write(str(datetime.datetime.now().date())+"---DHCP---")
    for file in dirs:
        print(file)
        file_name_cnf = file
        complete_path = s_path1 + file_name_cnf
        # how many lines in this file ?
        if (os.path.isfile(complete_path)):
            with open(complete_path, "r") as f:
                numlines = sum(1 for line in f)
            print("Total command lines on cisco routers : ", numlines)
            # split the file to lines
            with open(complete_path, "r") as f:
                f_line = f.readlines()
            host_dev = get_hostname_from_txt(f_line, numlines)
            Hostname = host_dev[0]
            Device = host_dev[1]
            s_notification = ""
            if Device == "":
                print("Please check file:", file)
                s_notification = "Please check this file"
            else:
                get_dhcp_from_log(f_line,Hostname,Device,numlines,s_path, conn, cursor)
        with open(s_path + "selected_files.txt", "a") as f:
            f.write(str(datetime.datetime.now().date()) + "/" +\
                    str(ifile) + ">" + file + "(" + s_notification + ")\n")
        ifile += 1


def about_igmp_ssm(s_path, conn, cursor):
    ifile = 0
    s_path1 = s_path + "Logs/DHCP/"
    dirs = os.listdir(s_path1)
    with open(s_path + "selected_files.txt", "w") as f:
        f.write(str(datetime.datetime.now().date())+"---IGMP SSM---")
    for file in dirs:
        print(file)
        file_name_cnf = file
        complete_path = s_path1 + file_name_cnf
        f_file = ''
        # how many lines in this file ?
        if (os.path.isfile(complete_path)):
            with open(complete_path, "r") as f:
                numlines = sum(1 for line in f)
            with open(complete_path,'r') as f:
                f_file = f.read()
            print("Total command lines on cisco routers : ", numlines)
            # split the file to lines
            with open(complete_path, "r") as f:
                f_line = f.readlines()
            host_dev = get_hostname_from_txt(f_line, numlines)
            Hostname = host_dev[0]
            Device = host_dev[1]
            s_notification = ""
            if Device == "":
                print("Please check file:", file)
                s_notification = "Please check this file"
            else:
                get_igmp_ssm_from_log(f_line, Hostname, Device, numlines, s_path, f_file, conn, cursor)
        with open(s_path + "selected_files.txt", "a") as f:
            f.write(str(datetime.datetime.now().date()) + "/" +\
                    str(ifile) + ">" + file + "(" + s_notification + ")\n")
        ifile += 1


def about_sla(s_path, conn, cursor):
    ifile = 0
    s_path1 = s_path + "Logs/IGMP_SSM/"
    dirs = os.listdir(s_path1)
    with open(s_path + "selected_files.txt", "w") as f:
        f.write(str(datetime.datetime.now().date())+"---SLA---")
    check_continue ="y"
    for file in dirs:
        print(file)
        file_name_cnf = file
        complete_path = s_path1 + file_name_cnf
        # how many lines in this file ?
        if (os.path.isfile(complete_path)):
            with open(complete_path, "r") as f:
                numlines = sum(1 for line in f)
            print("Total command lines on cisco routers : ", numlines)
            # split the file to lines
            with open(complete_path, "r") as f:
                f_line = f.readlines()
            host_dev = get_hostname_from_txt(f_line, numlines)
            Hostname = host_dev[0]
            Device = host_dev[1]
            s_notification = ""
            if Device == "":
                print("Please check file:", file)
                s_notification = "Please check this file"
            else:
                get_sla_from_log(f_line,Hostname,Device,numlines,s_path, conn, cursor)
                #check_continue = raw_input("Do you continue?")
                #if check_continue == "n":
                #    break
        with open(s_path + "selected_files.txt", "a") as f:
            f.write(str(datetime.datetime.now().date()) + "/" +\
                    str(ifile) + ">" + file + "(" + s_notification + ")\n")
        ifile += 1


def about_tldp_peer(s_path, conn, cursor):
    ifile = 0
    s_path1 = s_path + "Logs/SLA/"
    dirs = os.listdir(s_path1)
    with open(s_path + "selected_files.txt", "w") as f:
        f.write(str(datetime.datetime.now().date())+"---TLDP-Peer---")
    check_continue ="y"
    for file in dirs:
        print(file)
        file_name_cnf = file
        complete_path = s_path1 + file_name_cnf
        # how many lines in this file ?
        if (os.path.isfile(complete_path)):
            with open(complete_path, "r") as f:
                numlines = sum(1 for line in f)
            print("Total command lines on cisco routers : ", numlines)
            # split the file to lines
            with open(complete_path, "r") as f:
                f_line = f.readlines()
            host_dev = get_hostname_from_txt(f_line, numlines)
            Hostname = host_dev[0]
            Device = host_dev[1]
            s_notification = ""
            if Device == "":
                print("Please check file:", file)
                s_notification = "Please check this file"
            else:
                get_tldp_peer_from_log(f_line,Hostname,Device,numlines,s_path, conn, cursor)
                #check_continue = raw_input("Do you continue?")
                #if check_continue == "n":
                #    break
        with open(s_path + "selected_files.txt", "a") as f:
            f.write(str(datetime.datetime.now().date()) + "/" +\
                    str(ifile) + ">" + file + "(" + s_notification + ")\n")
        ifile += 1


def about_vlan(s_path, conn, cursor):
    ifile = 0
    s_path1 = s_path + "Logs/TLDP_Peer/"
    dirs = os.listdir(s_path1)
    with open(s_path + "selected_files.txt", "w") as f:
        f.write(str(datetime.datetime.now().date())+"---VLAN---")
    check_continue ="y"
    for file in dirs:
        print(file)
        file_name_cnf = file
        complete_path = s_path1 + file_name_cnf
        # how many lines in this file ?
        if (os.path.isfile(complete_path)):
            with open(complete_path, "r") as f:
                numlines = sum(1 for line in f)
            print("Total command lines on cisco routers : ", numlines)
            # split the file to lines
            with open(complete_path, "r") as f:
                f_line = f.readlines()
            host_dev = get_hostname_from_txt(f_line, numlines)
            Hostname = host_dev[0]
            Device = host_dev[1]
            s_notification = ""
            print(Hostname)
            print(Device)
            if Device == "":
                print("Please check file:", file)
                s_notification = "Please check this file"
            else:
                get_vlan_from_log(f_line,Hostname,Device,numlines,s_path, conn, cursor)
                #check_continue = raw_input("Do you continue?")
                #if check_continue == "n":
                #    break
        with open(s_path + "selected_files.txt", "a") as f:
            f.write(str(datetime.datetime.now().date()) + "/" +\
                    str(ifile) + ">" + file + "(" + s_notification + ")\n")
        ifile += 1


def about_classmap(s_path, conn, cursor):
    ifile = 0
    s_path1 = s_path + "Logs/VLAN/"
    dirs = os.listdir(s_path1)
    with open(s_path + "selected_files.txt", "w") as f:
        f.write(str(datetime.datetime.now().date())+"---Classmap---")
    check_continue ="y"
    for file in dirs:
        print(file)
        file_name_cnf = file
        complete_path = s_path1 + file_name_cnf
        # how many lines in this file ?
        if (os.path.isfile(complete_path)):
            with open(complete_path, "r") as f:
                numlines = sum(1 for line in f)
            print("Total command lines on cisco routers : ", numlines)
            # split the file to lines
            with open(complete_path, "r") as f:
                f_line = f.readlines()
            host_dev = get_hostname_from_txt(f_line, numlines)
            Hostname = host_dev[0]
            Device = host_dev[1]
            s_notification = ""
            print(Hostname)
            print(Device)
            if Device == "":
                print("Please check file:", file)
                s_notification = "Please check this file"
            else:
                get_classmap_from_log(f_line,Hostname,Device,numlines,s_path, conn, cursor)
                #check_continue = raw_input("Do you continue?")
                #if check_continue == "n":
                #    break
        with open(s_path + "selected_files.txt", "a") as f:
            f.write(str(datetime.datetime.now().date()) + "/" +\
                    str(ifile) + ">" + file + "(" + s_notification + ")\n")
        ifile += 1


def about_policy(s_path, conn, cursor):
    ifile = 0
    s_path1 = s_path + "Logs/Classmap/"
    dirs = os.listdir(s_path1)
    with open(s_path + "selected_files.txt", "w") as f:
        f.write(str(datetime.datetime.now().date())+"---Policy-map---")
    check_continue ="y"
    for file in dirs:
        print(file)
        file_name_cnf = file
        complete_path = s_path1 + file_name_cnf
        # how many lines in this file ?
        if (os.path.isfile(complete_path)):
            with open(complete_path, "r") as f:
                numlines = sum(1 for line in f)
            print("Total command lines on cisco routers : ", numlines)
            # split the file to lines
            with open(complete_path, "r") as f:
                f_line = f.readlines()
            host_dev = get_hostname_from_txt(f_line, numlines)
            Hostname = host_dev[0]
            Device = host_dev[1]
            s_notification = ""
            print(Hostname)
            print(Device)
            if Device == "":
                print("Please check file:", file)
                s_notification = "Please check this file"
            else:
                get_policy_map_from_log(f_line,Hostname,Device,numlines,s_path, conn, cursor)
                #check_continue = raw_input("Do you continue?")
                #if check_continue == "n":
                #    break
        with open(s_path + "selected_files.txt", "a") as f:
            f.write(str(datetime.datetime.now().date()) + "/" +\
                    str(ifile) + ">" + file + "(" + s_notification + ")\n")
        ifile += 1


def about_pw_class(s_path, conn, cursor):
    ifile = 0
    s_path1 = s_path + "Logs/Policy/"
    dirs = os.listdir(s_path1)
    with open(s_path + "selected_files.txt", "w") as f:
        f.write(str(datetime.datetime.now().date())+"---PW Class---")
    check_continue ="y"
    for file in dirs:
        print(file)
        file_name_cnf = file
        complete_path = s_path1 + file_name_cnf
        # how many lines in this file ?
        if (os.path.isfile(complete_path)):
            with open(complete_path, "r") as f:
                numlines = sum(1 for line in f)
            print("Total command lines on cisco routers : ", numlines)
            # split the file to lines
            with open(complete_path, "r") as f:
                f_line = f.readlines()
            host_dev = get_hostname_from_txt(f_line, numlines)
            Hostname = host_dev[0]
            Device = host_dev[1]
            s_notification = ""
            print(Hostname)
            print(Device)
            if Device == "":
                print("Please check file:", file)
                s_notification = "Please check this file"
            else:
                get_pw_class_from_log(f_line,Hostname,Device,numlines,s_path, conn, cursor)
                #check_continue = raw_input("Do you continue?")
                #if check_continue == "n":
                #    break
        with open(s_path + "selected_files.txt", "a") as f:
            f.write(str(datetime.datetime.now().date()) + "/" +\
                    str(ifile) + ">" + file + "(" + s_notification + ")\n")
        ifile += 1


def about_l2vpn(s_path, conn, cursor):
    ifile = 0
    s_path1 = s_path + "Logs/PW_Class/"
    dirs = os.listdir(s_path1)
    with open(s_path + "selected_files.txt", "w") as f:
        f.write(str(datetime.datetime.now().date())+"---L2VPN---")
    check_continue ="y"
    for file in dirs:
        print(file)
        file_name_cnf = file
        complete_path = s_path1 + file_name_cnf
        # how many lines in this file ?
        if (os.path.isfile(complete_path)):
            with open(complete_path, "r") as f:
                numlines = sum(1 for line in f)
            print("Total command lines on cisco routers : ", numlines)
            # split the file to lines
            with open(complete_path, "r") as f:
                f_line = f.readlines()
            host_dev = get_hostname_from_txt(f_line, numlines)
            Hostname = host_dev[0]
            Device = host_dev[1]
            s_notification = ""
            print(Hostname)
            print(Device)
            if Device == "":
                print("Please check file:", file)
                s_notification = "Please check this file"
            else:
                get_l2vpn_from_log(f_line,Hostname,Device,numlines,s_path, conn, cursor)
                #check_continue = raw_input("Do you continue?")
                #if check_continue == "n":
                #    break
        with open(s_path + "selected_files.txt", "a") as f:
            f.write(str(datetime.datetime.now().date()) + "/" +\
                    str(ifile) + ">" + file + "(" + s_notification + ")\n")
        ifile += 1


def about_interface(s_path, conn, cursor):
    ifile = 0
    s_path1 = s_path + "Logs/L2VPN/"
    dirs = os.listdir(s_path1)
    with open(s_path + "selected_files.txt", "w") as f:
        f.write(str(datetime.datetime.now().date())+"---Interface---")
    check_continue ="y"
    for file in dirs:
        print(file)
        file_name_cnf = file
        complete_path = s_path1 + file_name_cnf
        # how many lines in this file ?
        if (os.path.isfile(complete_path)):
            with open(complete_path, "r") as f:
                numlines = sum(1 for line in f)
            print("Total command lines on cisco routers : ", numlines)
            # split the file to lines
            with open(complete_path, "r") as f:
                f_line = f.readlines()
            host_dev = get_hostname_from_txt(f_line, numlines)
            Hostname = host_dev[0]
            Device = host_dev[1]
            s_notification = ""
            print(Hostname)
            print(Device)
            if Device == "":
                print("Please check file:", file)
                s_notification = "Please check this file"
            else:
                get_interface_from_log(f_line,Hostname,Device,numlines,s_path, conn, cursor)
                #check_continue = raw_input("Do you continue?")
                #if check_continue == "n":
                #    break
        with open(s_path + "selected_files.txt", "a") as f:
            f.write(str(datetime.datetime.now().date()) + "/" +\
                    str(ifile) + ">" + file + "(" + s_notification + ")\n")
        ifile += 1


def about_routing(s_path, conn, cursor):
    ifile = 0
    s_path1 = s_path + "Logs/Interface/"
    dirs = os.listdir(s_path1)
    with open(s_path + "selected_files.txt", "w") as f:
        f.write(str(datetime.datetime.now().date())+"---Routing---")
    check_continue ="y"
    for file in dirs:
        print(file)
        file_name_cnf = file
        complete_path = s_path1 + file_name_cnf
        # how many lines in this file ?
        if (os.path.isfile(complete_path)):
            with open(complete_path, "r") as f:
                numlines = sum(1 for line in f)
            print("Total command lines on cisco routers : ", numlines)
            # split the file to lines
            with open(complete_path, "r") as f:
                f_line = f.readlines()
            host_dev = get_hostname_from_txt(f_line, numlines)
            Hostname = host_dev[0]
            Device = host_dev[1]
            s_notification = ""
            print(Hostname)
            print(Device)
            if Device == "":
                print("Please check file:", file)
                s_notification = "Please check this file"
            else:
                get_routing_from_log(f_line,Hostname,Device,numlines,s_path, conn, cursor)
                #check_continue = raw_input("Do you continue?")
                #if check_continue == "n":
                #    break
        with open(s_path + "selected_files.txt", "a") as f:
            f.write(str(datetime.datetime.now().date()) + "/" +\
                    str(ifile) + ">" + file + "(" + s_notification + ")\n")
        ifile += 1


def about_lsp_path(s_path, conn, cursor):
    ifile = 0
    s_path1 = s_path + "Logs/Routing/"
    dirs = os.listdir(s_path1)
    with open(s_path + "selected_files.txt", "w") as f:
        f.write(str(datetime.datetime.now().date())+"---LSP Path---")
    check_continue ="y"
    for file in dirs:
        print(file)
        file_name_cnf = file
        complete_path = s_path1 + file_name_cnf
        # how many lines in this file ?
        if (os.path.isfile(complete_path)):
            with open(complete_path, "r") as f:
                numlines = sum(1 for line in f)
            print("Total command lines on cisco routers : ", numlines)
            # split the file to lines
            with open(complete_path, "r") as f:
                f_line = f.readlines()
            host_dev = get_hostname_from_txt(f_line, numlines)
            Hostname = host_dev[0]
            Device = host_dev[1]
            s_notification = ""
            print(Hostname)
            print(Device)
            if Device == "":
                print("Please check file:", file)
                s_notification = "Please check this file"
            else:
                get_lsp_path_from_log(f_line,Hostname,Device,numlines,s_path, conn, cursor)
                #check_continue = raw_input("Do you continue?")
                #if check_continue == "n":
                #    break
        with open(s_path + "selected_files.txt", "a") as f:
            f.write(str(datetime.datetime.now().date()) + "/" +\
                    str(ifile) + ">" + file + "(" + s_notification + ")\n")
        ifile += 1


def about_acl(s_path, conn, cursor):
    ifile = 0
    s_path1 = s_path + "Logs/LSP_Path/"
    dirs = os.listdir(s_path1)
    with open(s_path + "selected_files.txt", "w") as f:
        f.write(str(datetime.datetime.now().date())+"---ACL---")
    check_continue ="y"
    for file in dirs:
        print(file)
        file_name_cnf = file
        complete_path = s_path1 + file_name_cnf
        # how many lines in this file ?
        if (os.path.isfile(complete_path)):
            with open(complete_path, "r") as f:
                numlines = sum(1 for line in f)
            print("Total command lines on cisco routers : ", numlines)
            # split the file to lines
            with open(complete_path, "r") as f:
                f_line = f.readlines()
            host_dev = get_hostname_from_txt(f_line, numlines)
            Hostname = host_dev[0]
            Device = host_dev[1]
            s_notification = ""
            print(Hostname)
            print(Device)
            if Device == "":
                print("Please check file:", file)
                s_notification = "Please check this file"
            else:
                get_acl_from_log(f_line,Hostname,Device,numlines,s_path, conn, cursor)
                #check_continue = raw_input("Do you continue?")
                #if check_continue == "n":
                #    break
        with open(s_path + "selected_files.txt", "a") as f:
            f.write(str(datetime.datetime.now().date()) + "/" +\
                    str(ifile) + ">" + file + "(" + s_notification + ")\n")
        ifile += 1


def about_server(s_path, conn, cursor):
    ifile = 0
    s_path1 = s_path + "Logs/ACL/"
    dirs = os.listdir(s_path1)
    with open(s_path + "selected_files.txt", "w") as f:
        f.write(str(datetime.datetime.now().date())+"---Server---")
    check_continue ="y"
    for file in dirs:
        print(file)
        file_name_cnf = file
        complete_path = s_path1 + file_name_cnf
        f_file = ''
        # how many lines in this file ?
        if (os.path.isfile(complete_path)):
            with open(complete_path, "r") as f:
                numlines = sum(1 for line in f)
            print("Total command lines on cisco routers : ", numlines)
            # split the file to lines
            with open(complete_path, "r") as f:
                f_line = f.readlines()
            host_dev = get_hostname_from_txt(f_line, numlines)
            Hostname = host_dev[0]
            Device = host_dev[1]
            s_notification = ""
            print(Hostname)
            print(Device)
            if Device == "":
                print("Please check file:", file)
                s_notification = "Please check this file"
            else:
                get_server_from_log(f_line, Hostname, Device, numlines, s_path, conn, cursor)
                #check_continue = raw_input("Do you continue?")
                #if check_continue == "n":
                #    break
        with open(s_path + "selected_files.txt", "a") as f:
            f.write(str(datetime.datetime.now().date()) + "/" +\
                    str(ifile) + ">" + file + "(" + s_notification + ")\n")
        ifile += 1


def about_route_map(s_path, conn, cursor):
    ifile = 0
    s_path1 = s_path + "Logs/Server/"
    dirs = os.listdir(s_path1)
    with open(s_path + "selected_files.txt", "w") as f:
        f.write(str(datetime.datetime.now().date())+"---Route map---")
    check_continue ="y"
    for file in dirs:
        print(file)
        file_name_cnf = file
        complete_path = s_path1 + file_name_cnf
        # how many lines in this file ?
        if (os.path.isfile(complete_path)):
            with open(complete_path, "r") as f:
                numlines = sum(1 for line in f)
            print("Total command lines on cisco routers : ", numlines)
            # split the file to lines
            with open(complete_path, "r") as f:
                f_line = f.readlines()
            host_dev = get_hostname_from_txt(f_line, numlines)
            Hostname = host_dev[0]
            Device = host_dev[1]
            s_notification = ""
            print(Hostname)
            print(Device)
            if Device == "":
                print("Please check file:", file)
                s_notification = "Please check this file"
            else:
                get_route_map_from_log(f_line,Hostname,Device,numlines,s_path, conn, cursor)
                #check_continue = raw_input("Do you continue?")
                #if check_continue == "n":
                #    break
        with open(s_path + "selected_files.txt", "a") as f:
            f.write(str(datetime.datetime.now().date()) + "/" +\
                    str(ifile) + ">" + file + "(" + s_notification + ")\n")
        ifile += 1


def delete_db(hostname, conn, cursor):
    try:
        print ("coming into SQL")
        check_cont = 'y'
        list_db=['acl', 'acl_detail', 'bgp', 'classmap', 'dhcp', 'ifd', 'ifl', 'igmp_ssm', 'isis', 'isis_intf', \
                 'l2vpn', 'lsp', 'ospf', 'ospf_passive', 'path', 'path_detail', 'policy_map', 'pw_class', \
                 'redistribute', 'route_map', 'router', 'server', 'sla', 'static_route', 'tldp_peer', \
                 'vlan', 'vrf', 'vrf_ie', 'vsi','bfd']
        print('DB is deleting information of ', hostname)
        for item in list_db:
            print('You re working with ' + item)
            sql_query = ("select * from " + item + " where Hostname= '%s'") % hostname
            cursor.execute(sql_query)
            row = cursor.fetchall()
            if len(row) > 0:
                sql_query = ("delete from " + item + " WHERE Hostname= '%s' ") % hostname
                cursor.execute(sql_query)
                conn.commit()
            else:
                print("No information of %s in table %s" % (hostname,item))
        #check_cont=raw_input('Do you continue?')
        #if check_cont=='n':
        #    break
    except pymysql.Error as e:
        print (e)
        # rollback in case there is any error

def menu_1():
    print("1.Get informations of routers")
    print("2.Debug")
    print("3.Lay thong tin policy+acl")
    print("e.Exit")
    sel_index = input("Please choose above options:")
    return sel_index

def main():
    # #################global variables#########################
    # Total lines in original files
    #Testing github
    global numlines
    global f_line
    global s_path
    global txt_sql
    # Connector to mysql
    try:
        conn = pymysql.connect('127.0.0.1', 'root', '123456', 'vnpt')
        cursor = conn.cursor()
        # Information of file
        s_path = input("Enter the path:")
        if not os.path.isdir(s_path):
            print("This directory is not existed:", s_path, "Please check again")
            exit()
        if os.path.isfile(s_path + "selected_files.txt"):
            os.remove(s_path + "selected_files.txt")
        sel_index = menu_1()
        while sel_index != 'e':
            if sel_index == '1':
                print('Getting router information!')
                about_router(s_path, conn, cursor)
                time.sleep(5)
                print('Getting vrf information!')
                about_vrf(s_path, conn, cursor)
                time.sleep(5)
                print('Getting DHCP information!')
                about_dhcp(s_path, conn, cursor)
                time.sleep(5)
                print('Getting IGMP SSM information!')
                about_igmp_ssm(s_path, conn, cursor)
                time.sleep(5)
                print('Getting SLA information!')
                about_sla(s_path, conn, cursor)
                time.sleep(5)
                print('Getting TLDP information!')
                about_tldp_peer(s_path, conn, cursor)
                time.sleep(10)
                print('Getting VLAN information!')
                about_vlan(s_path, conn, cursor)
                time.sleep(5)
                print('Getting Traffic class information!')
                about_classmap(s_path, conn, cursor)
                time.sleep(5)
                print('Getting VRF import/export information!')
                about_policy(s_path, conn, cursor)
                time.sleep(5)
                print('Getting Tunnel information!')
                about_pw_class(s_path, conn, cursor)
                time.sleep(5)
                print('Getting L2VPN information!')
                about_l2vpn(s_path, conn, cursor)
                time.sleep(5)
                print('Getting IFD/IFL/L2circuit information!')
                about_interface(s_path, conn, cursor)
                time.sleep(15)
                print('Getting Routing/VRF import/export information!')
                about_routing(s_path, conn, cursor)
                time.sleep(15)
                print('Getting LSP Path information!')
                about_lsp_path(s_path, conn, cursor)
                time.sleep(5)
                print('Getting ACL information!')
                about_acl(s_path, conn, cursor)
                time.sleep(5)
                print('Getting Server information!')
                about_server(s_path, conn, cursor)
                time.sleep(5)
                print('Getting Route map information!')
                print('With HW,these info were get in routing part')
                about_route_map(s_path, conn, cursor)
                time.sleep(5)
                sel_index = 'e'
            elif sel_index == '2':
                print("==========================")
                print("1.Get general information of routers")
                print("2.Get L3VPN information")
                print("3.Get DHCP information")
                print("4.Get IGMP SSM")
                print("5.Get SLA")
                print("6.Get TLDP Peer")
                print("7.Get VLAN")
                print("8.Get Class-map")
                print("9.Get Policy-map")
                print("10.Get PW Class")
                print("11.Get L2VPN")
                print("12.Get interfaces(IFD/IFL)/LSP/Update IFL for L2circuit/ISIS-IFL")
                print("13.Get routing")
                print("14.Get LSP Path")
                print("15.Get ACL")
                print("16.Get server")
                print("17.Get Route-map")
                print("18.Delete database follow by hostname")
                print("19.Return main menu")
                sel_index1 = input("Please choose above options:")
                if sel_index1 == "1":
                    about_router(s_path)
                elif sel_index1 == "2":
                    about_vrf(s_path)
                elif sel_index1 == "3":
                    about_dhcp(s_path)
                elif sel_index1 == "4":
                    about_igmp_ssm(s_path)
                elif sel_index1 == "5":
                    about_sla(s_path)
                elif sel_index1 == "6":
                    about_tldp_peer(s_path)
                elif sel_index1 == "7":
                    about_vlan(s_path)
                elif sel_index1 == "8":
                    about_classmap(s_path)
                elif sel_index1 == "9":
                    about_policy(s_path)
                elif sel_index1 == "10":
                    about_pw_class(s_path)
                elif sel_index1 == "11":
                    about_l2vpn(s_path)
                elif sel_index1 == "12":
                    about_interface(s_path)
                elif sel_index1 == "13":
                    about_routing(s_path)
                elif sel_index1 == "14":
                    about_lsp_path(s_path)
                elif sel_index1 == "15":
                    about_acl(s_path)
                elif sel_index1 == "16":
                    about_server(s_path)
                elif sel_index1 == "17":
                    about_route_map(s_path)
                sel_index = menu_1()
            elif sel_index == '3':
                sql = 'select hostname from router'
                cursor.execute(sql)
                list_rows = cursor.fetchall()
                list_router = list([x[0] for x in list_rows])
                f = open(s_path + "policy_map.txt", "w")
                for item in list_router:
                    f.write('-----------------------------------\n')
                    f.write('Thong tin cua router ' + item + '\n')
                    list_policy_map = POLICYMAP.query_policy_name(item, cursor)
                    for key in list_policy_map:
                        f.write('Policy: ' + key + '\n')
                        if len(list_policy_map[key].mf_list) > 0:
                            for tmp_mf in list_policy_map[key].mf_list:
                                f.write('**MF chi tiet:\n')
                                attrs1 = vars(tmp_mf)
                                f.write(','.join("%s: %s" % item2 for item2 in list(attrs1.items())) + '\n')
                        f.write('-------------\n')
                        if len(list_policy_map[key].acl_list) > 0:
                            for tmp_acl in list_policy_map[key].acl_list:
                                f.write('**ACL chi tiet:\n')
                                attrs1 = vars(tmp_acl)
                                f.write(','.join("%s: %s" % item2 for item2 in list(attrs1.items())) + '\n')
                f.close()
                sel_index = 'e'
    except pymysql.Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    main()