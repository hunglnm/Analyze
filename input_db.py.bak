#from __future__ import print_function
from mysql.connector import MySQLConnection,Error
import mysql.connector
import os
from os.path import exists


#############search procedure#############
def search_pos(str_var,start_index):
	i=start_index
	while (i<numlines):
		if str_var in list_f[i]:
			search_pos=i
			return search_pos
			break
		i+=1
###############Insert data into table Router############
def insert_data_router():
	global Hostname
	i=pos_start
	Hostname=""
	RID=""
	SNMP_Comm=""
	SNMP_Source=""
	Login=""
	L2_age_time=0
	Multicast=0
	PIM=0
	TE=0
	LDP=0
	LDP_Session_Protect=0
	
	while (f_line[i].strip()!="end"):
		if f_line[i].strip().split(" ")[0]=="hostname":
			Hostname=f_line[i].strip().split(" ")[1]
		elif f_line[i].strip()=="ip multicast-routing":
			Multicast=1
		elif "ip pim sparse-mode" in f_line[i].strip():
			PIM=1
		elif f_line[i].strip()=="mpls traffic-eng tunnels":
			TE=1
		elif f_line[i].strip()=="mpls label protocol ldp":
			LDP=1
		elif f_line[i].strip()=="mpls ldp session protection":
			LDP_Session_Protect=1
		elif "mpls ldp router-id" in f_line[i].strip():
			RID=f_line[i].strip().split(" ")[-1].strip()
		elif "snmp-server community " in f_line[i].strip():
			SNMP_Comm=f_line[i].strip().split(" ")[2].strip()
		elif "snmp-server trap-source " in f_line[i].strip():
			SNMP_Source=f_line[i].strip().split(" ")[2].strip()
		elif "transport input " in f_line[i].strip():
			Login=f_line[i].strip()[16:]
		elif "mac-address-table aging-time " in f_line[i].strip():
			L2_age_time=int(f_line[i].strip().split(" ")[2].strip())
		i+=1		
########Template ###########
	add_router=("INSERT INTO Router "
				"(Hostname, RID, SNMP_Comm, SNMP_Source,Login, L2_age_time,Multicast,PIM,TE,LDP,LDP_Session_Protect) "
				"VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s) "
				"ON DUPLICATE KEY UPDATE SNMP_Comm=VALUES(SNMP_Comm), SNMP_Source=VALUES(SNMP_Source), "
				"Login=VALUES(Login), L2_age_time=VALUES(L2_age_time),Multicast=VALUES(Multicast), "
				"PIM=VALUES(PIM),TE=VALUES(TE),LDP=VALUES(LDP),LDP_Session_Protect=VALUES(LDP_Session_Protect)")
	data_router=(Hostname, RID, SNMP_Comm, SNMP_Source,Login, L2_age_time,Multicast,PIM,TE,LDP,LDP_Session_Protect)
	
	#Open and insert data into database 

	try:
		conn =mysql.connector.connect(user='root', password='hunglnm2307',host='127.0.0.1',database='hcmpt')
		cursor = conn.cursor()
		# Insert new router
		cursor.execute(add_router, data_router)
		
		if cursor.lastrowid:
			print('last insert id', cursor.lastrowid)
		else:
			print('last insert id not found')
		conn.commit()
	except Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()
###############Insert data into table IFD############
def insert_data_ifd():
	i=pos_interface_start
	print Hostname
	while i<pos_interface_vlan_start:
		Name=""
		Type="non-ae"#ae/non-ae
		Parent_link=""
		MTU=0
		Description=""
		Line=0
		AE_type=""
		AE_mode=""
		if f_line[i].strip().split(" ")[0]=="interface":
			if ((("Port-channel" in f_line[i].strip().split(" ")[1]) or ("TenGigabitEthernet" in f_line[i].strip().split(" ")[1])or("GigabitEthernet" in f_line[i].strip().split(" ")[1]))and("." not in f_line[i].strip().split(" ")[1])):
				Line=i
				Name=f_line[i].strip().split(" ")[1]
				print Name
				if ("Port-channel" in f_line[i].strip().split(" ")[1]) :
					Type="ae"
				i+=1
				while (f_line[i].strip().split(" ")[0]!="interface") and (f_line[i].strip().split(" ")[0]!="service")and(i<pos_interface_vlan_start):
					if (f_line[i].strip().split(" ")[0]=="description"):
						Description=f_line[i].strip()[12:].strip()
					elif (f_line[i].strip().split(" ")[0]=="mtu"):
						MTU=int(f_line[i].strip().split(" ")[1].strip())
					elif f_line[i].strip().split(" ")[0]=="channel-protocol": 
						AE_type=f_line[i].strip().split(" ")[1].strip()
					elif f_line[i].strip().split(" ")[0]=="channel-group":
						Parent_link=f_line[i].strip().split(" ")[1].strip()
						AE_mode=f_line[i].strip().split(" ")[-1].strip()
					i+=1
				########Template ###########
				add_ifd=("INSERT INTO IFD "
				"(Name,Hostname,Type,Parent_link,MTU,Description,Line,AE_type,AE_mode) "
				"VALUES (%s, %s, %s, %s,%s, %s,%s, %s, %s) "
				"ON DUPLICATE KEY UPDATE Type=VALUES(Type),Parent_link=VALUES(Parent_link), "
				"MTU=VALUES(MTU),Description=VALUES(Description),Line=VALUES(Line),AE_type=VALUES(AE_type), "
				"AE_mode=VALUES(AE_mode)")
				data_ifd=(Name,Hostname,Type,Parent_link,MTU,Description,Line,AE_type,AE_mode)
				#Open and insert data into database 
				try:
					conn =mysql.connector.connect(user='root', password='hunglnm2307',host='127.0.0.1',database='hcmpt')
					cursor = conn.cursor()
					# Insert new router
					cursor.execute(add_ifd, data_ifd)
		
					if cursor.lastrowid:
						print('last insert id', cursor.lastrowid)
					else:
						print('last insert id not found')
					conn.commit()
				except Error as error:
					print(error)
				finally:
					cursor.close()
					conn.close()
		i+=1
##############################Main procedure#####################################			
def main():
	##################global variables#########################
	global pos_start
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
	global Hostname
	global f_line
	#Information of file
	print "Copy this py file into the same folder with configuration files" 
	s_path=raw_input("Enter the path:")
	file_name_cnf = raw_input("Enter the currently configuration file name :")
	complete_path=s_path+file_name_cnf
	#Read file###########
	#how many lines in this file ?
	f=open(complete_path,"r")
	numlines = sum(1 for line in f)
	f.close()
	#split the file to lines 
	f=open(complete_path,"r")
	f_line=f.readlines()
	f.close()
	
	#The first index is 0
	i=0
	
	#group level 1 :vrf>dhcp>policy-map>l2 vfi>interface>interface vlan>router>router bgp>static>ACL>route-map
	pos_start=0
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
	
	while (i<numlines):
		if ("hostname"==f_line[i].strip().split(" ")[0]):
			pos_start=i
			print pos_start
			break
		i+=1
	while (i<numlines):
		if ("ip vrf " in f_line[i]):
			pos_vrf_start=i
			print pos_vrf_start
			break
		i+=1
	if pos_vrf_start==0 :
		i=pos_start
	while (i<numlines):
		if ("ip dhcp pool " in f_line[i]):
			pos_dhcp_start=i
			print pos_dhcp_start
			break
		i+=1
	if pos_dhcp_start==0:
		i=pos_vrf_start+1
	while (i<numlines):
		if ("policy-map"==f_line[i].strip().split(" ")[0]):
			pos_policy_start=i
			print pos_policy_start
			break
		i+=1
	if pos_policy_start==0:
		i=pos_vrf_start+1
	while (i<numlines):
		if ("l2 vfi " in f_line[i]):
			pos_vfi_start=i
			print pos_vfi_start
			break
		i+=1
	if pos_vfi_start==0:
		i=pos_vrf_start+1
	while (i<numlines):
		if ("interface " in f_line[i]):
			pos_interface_start=i
			print pos_interface_start
			break
		i+=1
	if pos_interface_start==0:
		i=pos_vrf_start+1
	while (i<numlines):
		if ("interface Vlan" in f_line[i]):
			pos_interface_vlan_start=i
			print pos_interface_vlan_start
			break
		i+=1
	if pos_interface_vlan_start==0:
		i=pos_vrf_start+1
	while (i<numlines):
		if ("router"==f_line[i].strip().split(" ")[0]):
			pos_router_start=i
			print pos_router_start
			break
		i+=1
	if pos_router_start==0:
		i=pos_vrf_start+1
	while (i<numlines):
		if ("router bgp " in f_line[i]):
			pos_router_bgp_start=i
			print pos_router_bgp_start
			break
		i+=1
	if pos_router_bgp_start==0:
		i=pos_vrf_start+1
	while (i<numlines):
		if ("ip route vrf " in f_line[i]):
			pos_static_start=i
			print pos_static_start
			break
		i+=1
	if pos_static_start==0:
		i=pos_vrf_start+1
	while (i<numlines):
		if ("ip access-list " in f_line[i]):
			pos_acl_start=i
			print pos_acl_start
			break
		i+=1	
	if pos_acl_start==0:
		i=pos_vrf_start+1
	while (i<numlines):
		if ("route-map " in f_line[i]):
			pos_route_map_start=i
			print pos_route_map_start
			break
		i+=1
	if pos_route_map_start==0:
		i=pos_vrf_start+1
	insert_data_router()
	insert_data_ifd()
if __name__ == '__main__':
    main()