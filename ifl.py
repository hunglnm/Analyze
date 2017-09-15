class IFL:
    Hostname=""

    def __init__(self):
        self.IFD = ""
        self.Unit = 0
        self.Unit1=0
        self.Description = ""
        self.Service = ""
        self.IP=""
        self.Routing_type = ""
        self.ISIS_circuit_type = ""
        self.Routing_intf_type = ""
        self.Intf_metric = 0
        self.RSVP = False
        self.PIM = False
        self.MPLS = False
        self.SVLAN = ""
        self.CVLAN = ""
        self.Vlan_mapping = ""
        self.Vlan_translate = ""
        self.Vlan_map_svlan = ""
        self.Vlan_map_cvlan = ""
        self.VRF_Name = ""
        self.BD_ID = ""
        self.Split_horizon = False
        self.Service_pol_in = ""
        self.Service_pol_out = ""
        self.MTU = 0
        self.CLNS_MTU = 0
        self.Admin_status = True
        self.Stitching = False
        self.Switchport = False
        self.Switch_mode=""
        self.IP_helper=""
        self.Backup_path = ''
        self.FF_in = ''
        self.FF_out=''
        self.p1= False
        self.classifier = ''
        self.isis_bfd= ''
        self.ldp_sync = False
        self.igmp = False
        self.igmp_ssm = ''
        self.igmp_static = ''
        self.dhcp_snoop = False
        self.dhcp_trust = False
        self.loop_detect = False
        self.vrrp = False
        self.vrrp_group=''
        self.vrrp_vip=''
        self.vrrp_prio= 0
        self.vrrp_delay = 0
        self.ARP_Unicast=False
        self.ARP_exp = 0
        self.CCC_Intf = ''
        self.CCC_Name=''
        self.rrpp = False
        self.rrpp_vsi_list = ''
        self.vsi_encap = ''
        self.dhcp_gw=''
        self.df_classifier=''

    def showdata(self):
        attrs = vars(self)
        print IFL.Hostname,',',','.join("%s: %s" % item for item in attrs.items())

    def insert(self, cursor):
        add_ifl = ("INSERT INTO IFL "
                    "(IFD,Hostname,Unit,Unit1,Description,Service,IP,Routing_type,ISIS_circuit_type, "
                    "Routing_intf_type,Intf_metric,RSVP,PIM,MPLS,SVLAN,CVLAN,Vlan_mapping, "
                    "Vlan_translate,Vlan_map_svlan,Vlan_map_cvlan,VRF_Name,BD_ID,Split_horizon, "
                    "Service_pol_in,Service_pol_out,MTU,CLNS_MTU,Admin_status,Stitching,Switchport,Switch_mode,IP_helper"
                   ", Backup_path, FF_in,Trust_8021p,Classifier,ISIS_BFD,LDP_SYNC,IGMP,IGMP_SSM,IGMP_Static,DHCP_snoop,"
                   "DHCP_trust,Loop_detect,VRRP,VRRP_group,VRRP_vip,VRRP_prio,VRRP_delay,ARP_Unicast,ARP_exp,CCC_Intf,"
                   "CCC_Name,RRPP,RRPP_vsi_list,VSI_encap,FF_out,DHCP_GW,DF_classifier )"
                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                   "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                    "ON DUPLICATE KEY UPDATE Unit1=VALUES(Unit1),Description=VALUES(Description), "
                    "Service=VALUES(Service),IP=VALUES(IP),Routing_type=VALUES(Routing_type), "
                    "ISIS_circuit_type=VALUES(ISIS_circuit_type),Routing_intf_type=VALUES(Routing_intf_type), "
                    "Intf_metric=VALUES(Intf_metric),RSVP=VALUES(RSVP),PIM=VALUES(PIM),MPLS=VALUES(MPLS), "
                    "SVLAN=VALUES(SVLAN),CVLAN=VALUES(CVLAN),Vlan_mapping=VALUES(Vlan_mapping), "
                    "Vlan_translate=VALUES(Vlan_translate),Vlan_map_svlan=VALUES(Vlan_map_svlan), "
                    "Vlan_map_cvlan=VALUES(Vlan_map_cvlan),VRF_Name=VALUES(VRF_Name),BD_ID=VALUES(BD_ID), "
                    "Split_horizon=VALUES(Split_horizon),Service_pol_in=VALUES(Service_pol_in), "
                    "Service_pol_out=VALUES(Service_pol_out),MTU=VALUES(MTU), "
                    "CLNS_MTU=VALUES(CLNS_MTU),Admin_status=VALUES(Admin_status),Stitching=VALUES(Stitching), "
                    "Switchport=VALUES(Switchport),Switch_mode=VALUES(Switch_mode),IP_helper=VALUES(IP_helper),"
                   "Backup_path=VALUES(Backup_path),FF_in=VALUES(FF_in),Trust_8021p=VALUES(Trust_8021p), "
                   "Classifier=VALUES(Classifier),ISIS_BFD=VALUES(ISIS_BFD),LDP_SYNC=VALUES(LDP_SYNC),IGMP=VALUES(IGMP),"
                   "IGMP_SSM=VALUES(IGMP_SSM),IGMP_Static=VALUES(IGMP_Static),DHCP_snoop=VALUES(DHCP_snoop),"
                   "DHCP_trust=VALUES(DHCP_trust),Loop_detect=VALUES(Loop_detect),VRRP=VALUES(VRRP),"
                   "VRRP_group=VALUES(VRRP_group),VRRP_vip=VALUES(VRRP_vip),VRRP_prio=VALUES(VRRP_prio),"
                   "VRRP_delay=VALUES(VRRP_delay),ARP_Unicast=VALUES(ARP_Unicast),ARP_exp=VALUES(ARP_exp),"
                   "CCC_Intf=VALUES(CCC_Intf),CCC_Name=VALUES(CCC_Name),RRPP=VALUES(RRPP),RRPP_vsi_list="
                   "VALUES(RRPP_vsi_list),VSI_encap=VALUES(VSI_encap),FF_out=VALUES(FF_out),DHCP_GW=VALUES(DHCP_GW),"
                   "DF_classifier=VALUES(DF_classifier) ")
        data_ifl = (self.IFD,IFL.Hostname,self.Unit,self.Unit1,self.Description,self.Service,
                    self.IP,self.Routing_type,self.ISIS_circuit_type,self.Routing_intf_type,
                    self.Intf_metric,self.RSVP,self.PIM,self.MPLS,self.SVLAN,self.CVLAN,self.Vlan_mapping,
                    self.Vlan_translate,self.Vlan_map_svlan,self.Vlan_map_cvlan,self.VRF_Name,self.BD_ID,
                    self.Split_horizon,self.Service_pol_in,self.Service_pol_out,self.MTU,self.CLNS_MTU,
                    self.Admin_status,self.Stitching,self.Switchport,self.Switch_mode,self.IP_helper,
                    self.Backup_path,self.FF_in,self.p1,self.classifier,self.isis_bfd,self.ldp_sync,self.igmp,
                    self.igmp_ssm,self.igmp_static,self.dhcp_snoop,self.dhcp_trust,self.loop_detect,self.vrrp,
                    self.vrrp_group,self.vrrp_vip,self.vrrp_prio,self.vrrp_delay,self.ARP_Unicast,self.ARP_exp,
                    self.CCC_Intf,self.CCC_Name,self.rrpp,self.rrpp_vsi_list,self.vsi_encap,self.FF_out,self.dhcp_gw,
                    self.df_classifier)
        cursor.execute(add_ifl, data_ifl)

    def update_bgp_mpls(self, cursor):
        add_ifl = ("INSERT INTO IFL (IFD,Hostname,Unit,MPLS)"
                   "VALUES (%s,%s,%s,%s) "
                   "ON DUPLICATE KEY UPDATE MPLS=VALUES(MPLS)")
        data_ifl = (self.IFD, IFL.Hostname, self.Unit, self.MPLS)
        cursor.execute(add_ifl, data_ifl)
