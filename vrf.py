class VRF:
    Hostname = ""

    def __init__(self,seq_exp=0,seq_imp=0):
        self.Name = ""
        self.RD = ""
        self.DHCP_Server = False
        self.DHCP_Relay = False
        self.Static_routing = False
        self.BGP = False
        self.OSPF = False
        self.seq_exp = seq_exp
        self.seq_imp = seq_imp
        self.Max_prefix = 0
        self.tnl_policy = ''
        self.classifier = ''
        self.color = ''
        self.frr = False
        self.Exp_extcom = ''
        self.Imp_extcom = ''
        self.description = ''

    def showdata(self):
        attrs = vars(self)
        print VRF.Hostname,',',','.join("%s: %s" % item for item in attrs.items())

    def insert(self, cursor):
        add_l3vpn = ("INSERT INTO VRF "
                     "(Hostname,Name,RD,DHCP_Server,DHCP_Relay,Static_routing,BGP,OSPF,Max_prefix,Tnl_policy, "
                     "Classifier,Color,FRR,Exp_extcom,Imp_extcom,Description) "
                     "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                     "ON DUPLICATE KEY UPDATE RD=VALUES(RD),DHCP_Server=VALUES(DHCP_Server),DHCP_Relay=VALUES(DHCP_Relay), "
                     "Static_routing=VALUES(Static_routing),BGP=VALUES(BGP),OSPF=VALUES(OSPF),Max_prefix=VALUES"
                     "(Max_prefix),Tnl_policy=VALUES(Tnl_policy),Classifier=VALUES(Classifier),Color=VALUES(Color), "
                     "FRR=VALUES(FRR),Exp_extcom=VALUES(Exp_extcom),Imp_extcom=VALUES(Imp_extcom),"
                     "Description=VALUES(Description)")
        data_l3vpn = (VRF.Hostname,self.Name,self.RD,self.DHCP_Server,self.DHCP_Relay,self.Static_routing,
                      self.BGP,self.OSPF,self.Max_prefix,self.tnl_policy,self.classifier,self.color,self.frr,
                      self.Exp_extcom,self.Imp_extcom,self.description)
        cursor.execute(add_l3vpn, data_l3vpn)

    def insert_dhcp_server(self,cursor):
        add_l3vpn = ("INSERT INTO VRF "
                     "(Hostname,Name,DHCP_Server) "
                     "VALUES (%s,%s,%s) "
                     "ON DUPLICATE KEY UPDATE DHCP_Server=VALUES(DHCP_Server)")
        data_l3vpn = (VRF.Hostname, self.Name,self.DHCP_Server)
        cursor.execute(add_l3vpn, data_l3vpn)

    def insert_dhcp_relay(self,cursor):
        add_l3vpn = ("INSERT INTO VRF "
                     "(Hostname,Name,DHCP_Relay) "
                     "VALUES (%s,%s,%s) "
                     "ON DUPLICATE KEY UPDATE DHCP_Relay=VALUES(DHCP_Relay)")
        data_l3vpn = (VRF.Hostname, self.Name,self.DHCP_Relay)
        cursor.execute(add_l3vpn, data_l3vpn)

    def update_dhcp_static(self,cursor):
        add_l3vpn = ("INSERT INTO VRF "
                     "(Hostname,Name,Static_routing,DHCP_Relay) "
                     "VALUES (%s,%s,%s,%s) "
                     "ON DUPLICATE KEY UPDATE Static_routing=VALUES(Static_routing),DHCP_Relay=VALUES(DHCP_Relay)")
        data_l3vpn = (VRF.Hostname, self.Name,self.Static_routing,self.DHCP_Relay)
        cursor.execute(add_l3vpn, data_l3vpn)

    def insert_static(self,cursor):
        add_l3vpn = ("INSERT INTO VRF "
                     "(Hostname,Name,Static_routing) "
                     "VALUES (%s,%s,%s) "
                     "ON DUPLICATE KEY UPDATE Static_routing=VALUES(Static_routing)")
        data_l3vpn = (VRF.Hostname, self.Name, self.Static_routing)
        cursor.execute(add_l3vpn, data_l3vpn)

    def insert_new(self,cursor):
        add_l3vpn = ("INSERT INTO VRF "
                     "(Hostname,Name,Static_routing,BGP,FRR) "
                     "VALUES (%s,%s,%s,%s,%s) "
                     "ON DUPLICATE KEY UPDATE Static_routing=VALUES(Static_routing),BGP=VALUES(BGP),FRR=VALUES(FRR)")
        data_l3vpn = (VRF.Hostname, self.Name,self.Static_routing,self.BGP,self.frr)
        cursor.execute(add_l3vpn, data_l3vpn)

    def insert_new1(self,cursor):
        add_l3vpn = ("INSERT INTO VRF "
                     "(Hostname,Name,BGP,FRR) "
                     "VALUES (%s,%s,%s,%s) "
                     "ON DUPLICATE KEY UPDATE BGP=VALUES(BGP),FRR=VALUES(FRR)")
        data_l3vpn = (VRF.Hostname, self.Name,self.BGP,self.frr)
        cursor.execute(add_l3vpn, data_l3vpn)

    def insert_bgp(self,cursor):
        add_l3vpn = ("INSERT INTO VRF "
                     "(Hostname,Name,BGP) "
                     "VALUES (%s,%s,%s) "
                     "ON DUPLICATE KEY UPDATE BGP=VALUES(BGP)")
        data_l3vpn = (VRF.Hostname, self.Name,self.BGP)
        cursor.execute(add_l3vpn, data_l3vpn)

    def insert_ospf(self,cursor):
        add_l3vpn = ("INSERT INTO VRF "
                     "(Hostname,Name,OSPF) "
                     "VALUES (%s,%s,%s) "
                     "ON DUPLICATE KEY UPDATE OSPF=VALUES(OSPF)")
        data_l3vpn = (VRF.Hostname, self.Name,self.OSPF)
        cursor.execute(add_l3vpn, data_l3vpn)



