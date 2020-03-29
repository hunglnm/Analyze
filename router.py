class Router:
    def __init__(self,Hostname):
        self.Hostname = Hostname
        self.Device = ""
        self.RID = ""
        self.Timezone = ""
        self.SNMP_Comm = ""
        self.SNMP_Trap = False
        self.Login = ""
        self.L2_age_time = 0
        self.Multicast = False
        self.IGMP_SSM=False
        self.PIM = False
        self.TE = False
        self.LDP = False
        self.LDP_Session_Protect = False
        self.DHCP_Relay=False
        self.loop_detect= False
        self.bfd_mpls = False
        self.DHCP_Snoop = False

    def insert(self, cursor):
        add_router = ("INSERT INTO Router "
                      "(Hostname,Device,RID,Timezone,SNMP_Comm,SNMP_Trap,Login,L2_age_time,Multicast, "
                      "IGMP_SSM,PIM,TE,LDP,LDP_Session_Protect,DHCP_Relay,Loop_detect,BFD_MPLS,DHCP_Snoop) "
                      "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                      "ON DUPLICATE KEY UPDATE Device=VALUES(DEVICE), RID=VALUES(RID), Timezone=VALUES(Timezone), "
                      "SNMP_Comm=VALUES(SNMP_Comm), SNMP_Trap=VALUES(SNMP_Trap),Login=VALUES(Login), "
                      "L2_age_time=VALUES(L2_age_time),Multicast=VALUES(Multicast), IGMP_SSM=VALUES(IGMP_SSM), "
                      "PIM=VALUES(PIM),TE=VALUES(TE),LDP=VALUES(LDP),LDP_Session_Protect=VALUES(LDP_Session_Protect), "
                      "DHCP_Relay=VALUES(DHCP_Relay),Loop_detect=VALUES(Loop_detect),BFD_MPLS=VALUES(BFD_MPLS), "
                      "DHCP_Snoop=VALUES(DHCP_Snoop)")
        data_router = (Router.Hostname,self.Device, self.RID, self.Timezone,self.SNMP_Comm,self.SNMP_Trap,self.Login,
                       self.L2_age_time, self.Multicast, self.IGMP_SSM, self.PIM, self.TE, self.LDP,
                       self.LDP_Session_Protect,self.DHCP_Relay,self.loop_detect,self.bfd_mpls,self.DHCP_Snoop)
        cursor.execute(add_router, data_router)

    @staticmethod
    def query(self, cursor):
        query_router = "SELECT * FROM Router "
        cursor.execute(query_cli_router)
        return cursor.fetchall()

    @staticmethod
    def delete(self, cursor):
        delete_cli_router = ("DELETE * FROM CLI_Router "
                             "WHERE Hostname='%s'")
        data_cli_router = (CLI_Router.Hostname)

        cursor.execute(delete_cli_router, data_cli_router)

    def getdata(self, result_query):
        for row in result_query:
            print(row)  # Xu ly truoc khi print

    def showdata(self):
        print("Hostname:", self.Hostname)
        print("Device:", self.Device)
        print("RID:",self.RID)
        print("Timezone:", self.Timezone)
        print("SNMP community:", self.SNMP_Comm)
        print("SNMP Trap:", self.SNMP_Trap)
        print("Login:", self.Login)
        print("L2 Age time:", self.L2_age_time)
        print("Multicast:", self.Multicast)
        print("IGMP SSM:", self.IGMP_SSM)
        print("PIM:", self.PIM)
        print("TE:", self.TE)
        print("LDP:", self.LDP)
        print("LDP Session Protect:", self.LDP_Session_Protect)