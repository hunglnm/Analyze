from mysql.connector import MySQLConnection,Error
import mysql.connector
import os,sys
from os.path import exists

#Get Hostname
def get_hostname():
	global Hostname
	i=0
	while (f_line[i].strip()!="end"):
		if f_line[i].strip().split(" ")[0]=="hostname":
			Hostname=f_line[i].strip().split(" ")[1]
			break
		i+=1
#Find keyword positions
def pos_key():
	if "76" in Hostname:
		print "The device is C76xx"
	#group level 1 :vrf>dhcp>policy-map>l2 vfi>interface>interface vlan>router>router bgp>static>ACL>route-map
		global cfg_start
		global pos_vrf_start
		global pos_dhcp_start
		global pos_policy_start
		global pos_vfi_start
		global pos_interface_start
		global pos_interface_vlan_start
		global pos_router_start
		global pos_router_bgp_start
		global pos_static_start
		global pos_acl_start
		global pos_route_map_start
		global cfg_end
		cfg_start=0
		pos_vrf_start=0
		pos_dhcp_start=0
		pos_policy_start=0
		pos_vfi_start=0
		pos_interface_start=0
		pos_interface_vlan_start=0
		pos_router_start=0
		pos_router_bgp_start=0
		pos_static_start=0
		pos_acl_start=0
		pos_route_map_start=0
		cfg_end=0
		i=0
		while (i<numlines):
			if ("Building configuration" in f_line[i]):
				cfg_start=i
				break
			i+=1
		if cfg_start==0:
			i=0
		print "Position of configuration start:",cfg_start
		while (i<numlines):
			if ("ip vrf " in f_line[i]):
				pos_vrf_start=i
				break
			i+=1
		if pos_vrf_start==0 :
			i=cfg_start
		print "Position of VRF start:",pos_vrf_start		
		while (i<numlines):
			if ("ip dhcp pool " in f_line[i]):
				pos_dhcp_start=i
				break
			i+=1
		if pos_dhcp_start==0 :
			i=pos_vrf_start+1
		print "Position of DHCP start:",pos_dhcp_start
		while (i<numlines):
			if ("policy-map"==f_line[i].strip().split(" ")[0]):
				pos_policy_start=i
				break
			i+=1
		if pos_policy_start==0 :
			i=pos_vrf_start+1
		print "Position of policy start:",pos_policy_start
		while (i<numlines):
			if ("l2 vfi " in f_line[i]):
				pos_vfi_start=i
				break
			i+=1
		if pos_vfi_start==0 :
			i=pos_vrf_start+1
		print "Position of VFI start:",pos_vfi_start
		while (i<numlines):
			if ("interface " in f_line[i]):
				pos_interface_start=i
				break
			i+=1
		if pos_interface_start==0 :
			i=pos_vrf_start+1
		print "Position of interface start:",pos_interface_start
		while (i<numlines):
			if ("interface Vlan" in f_line[i]):
				pos_interface_vlan_start=i
				break
			i+=1
		if pos_interface_vlan_start==0 :
			i=pos_vrf_start+1
		print "Position of vlan interface start:",pos_interface_vlan_start
		while (i<numlines):
			if ("router"==f_line[i].strip().split(" ")[0]):
				pos_router_start=i
				break
			i+=1
		if pos_router_start==0 :
			i=pos_vrf_start+1
		print "Position of router start:",pos_router_start
		while (i<numlines):
			if ("router bgp " in f_line[i]):
				pos_router_bgp_start=i
				break
			i+=1
		if pos_router_bgp_start==0 :
			i=pos_vrf_start+1
		print "Position of bgp start:",pos_router_bgp_start
		while (i<numlines):
			if ("ip route vrf " in f_line[i]):
				pos_static_start=i
				break
			i+=1
		if pos_static_start==0 :
			i=pos_vrf_start+1
		print "Position of static start:",pos_static_start
		while (i<numlines):
			if ("ip access-list " in f_line[i]):
				pos_acl_start=i
				break
			i+=1	
		if pos_acl_start==0 :
			i=pos_vrf_start+1
		print "Position of ACL start:",pos_acl_start
		while (i<numlines):
			if ("route-map " in f_line[i]):
				pos_route_map_start=i
				break
			i+=1		
		if pos_route_map_start==0 :
			i=pos_vrf_start+1
		print "Position of route-map start:",pos_route_map_start
		while (i<numlines):
			if f_line[i]=="end\n":
				cfg_end=i
				break
			i+=1
		print "Position of configuration end:",cfg_end
#ASR
	elif Hostname[0:2]=="ASR":
		print "The device is ASR"	
		while (i<numlines):
			if ("Building configuration" in f_line[i]):
				cfg_start=i
				break
			i+=1
		if cfg_start==0:
			i=0
	
def insert_cli_into_db():
	#insert any CLIs haven't process
	#The first index is 0
	i=cfg_start
	Line=0
	CLI=""
	#Hostname=Hostname 
	if "76" in Hostname:
		while i<(cfg_end+1):
			Line=i
			CLI=f_line[i]
			Pos_key=""
			if i>0:
				if (Line==cfg_start):
					Pos_key="cfg_start"
				elif (Line==pos_vrf_start):
					Pos_key="vrf_start"
				elif (Line==pos_dhcp_start):
					Pos_key="dhcp_start"
				elif (Line==pos_policy_start):
					Pos_key="policy_start"
				elif (Line==pos_vfi_start):
					Pos_key="vfi_start"
				elif (Line==pos_interface_start):
					Pos_key="interface_start"
				elif (Line==pos_interface_vlan_start):
					Pos_key="interface_vlan_start"
				elif (Line==pos_router_start):
					Pos_key="router_start"
				elif (Line==pos_router_bgp_start):
					Pos_key="router_bgp_start"
				elif (Line==pos_static_start):
					Pos_key="static_start"
				elif (Line==pos_acl_start):
					Pos_key="acl_start"
				elif (Line==pos_route_map_start):
					Pos_key="route_map_start"
				elif (Line==cfg_end):
					Pos_key="cfg_end"
		########Template ###########
			add_cli_router=("INSERT INTO CLI_Router "
				"(Hostname,Line,CLI,Pos_key,Processed) "
				"VALUES (%s,%s,%s,%s,%s) "
				"ON DUPLICATE KEY UPDATE CLI=VALUES(CLI),Pos_key=VALUES(Pos_key),Processed=VALUES(Processed)")
			data_cli_router=(Hostname,Line,CLI,Pos_key,Processed)
			cursor.execute(add_cli_router, data_cli_router)
			i+=1
		conn.commit()
		
def delete_cli_db(name):
	query = "DELETE FROM CLI_Router WHERE Hostname = %s"
	cursor.execute(query, (name,))
	conn.commit()
def main():

	##################global variables#########################

	global numlines

	global f_line

	global conn
	global cursor
	#Information of file
	s_path=raw_input("Enter the path:")
	dirs=os.listdir(s_path)

	check_continue="y"
	ifile=0
	for file in dirs:
		print file
		get_inf=raw_input("Do you get information of this file?(y/n)")
		if get_inf!="y":
			check_continue=raw_input("Do you continue?(y/n)")
			if check_continue=="n":break
		else:
			ifile+=1
			f=open("selected_files.txt","w")
			f.write(str(ifile)+">"+file+"\n")
			file_name_cnf = file#raw_input("Enter the currently configuration file name :")
			complete_path=s_path+file_name_cnf
		#Read file
		#how many lines in this file ?
			f=open(complete_path,"r")
			numlines = sum(1 for line in f)
			print "Total command lines on cisco routers : ", numlines 
			f.close()
		#split the file to lines 
			f=open(complete_path,"r")
			f_line=f.readlines()
			f.close()
			
			get_hostname()
			pos_key()
			print "####################\nUpdate database.\nSelect:"
			print "1.Insert CLI for "+Hostname+" into DB.\n1d.Delete CLI with "+Hostname+" in CLI_Router."
			print "a.Insert all info for "+Hostname+" into DB.\nc.Cancel"
			selected_db=raw_input("Please select the above list:")
			try:
				conn =mysql.connector.connect(user='root', password='hunglnm2307',host='127.0.0.1',database='hcmpt')
				cursor = conn.cursor()
				if selected_db=="1":
					insert_cli_into_db()
				elif selected_db=="1d":
					delete_cli_db(Hostname);
				elif selected_db=="a":
					insert_cli_into_db()
				elif selected_db=="c":
					print "Nothing is updated!"
				else:
					print "Wrong selection!"
			except Error as error:
				print(error)
			finally:
				cursor.close()
				conn.close()
			
if __name__ == '__main__':
    main()