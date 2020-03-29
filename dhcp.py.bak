class DHCP:
    Hostname = ""
    Exclude = ""
    def __init__(self):
        self.Name = ""
        self.VRF_Name = ""
        self.NW=""
        self.GW=""
        self.DNS=""

    def insert(self, cursor):
        add_dhcp = ("INSERT INTO DHCP "
                        "(Name,Hostname,VRF_Name,NW,GW,DNS,Exclude) "
                        "VALUES (%s,%s,%s,%s,%s,%s,%s) "
                        "ON DUPLICATE KEY UPDATE VRF_Name=VALUES(VRF_Name),NW=VALUES(NW),GW=VALUES(GW), "
                        "DNS=VALUES(DNS),Exclude=VALUES(Exclude)")
        data_dhcp = (self.Name,DHCP.Hostname,self.VRF_Name,self.NW,self.GW,self.DNS,DHCP.Exclude)
        cursor.execute(add_dhcp, data_dhcp)

    def showdata(self):
        print  "Hostname:", self.Hostname
        print  "Name:", self.Name
        print "VRF:",self.VRF_Name
        print "NW:",self.NW
        print "GW:",self.GW
        print "DNS:",self.DNS
        print "Exclude:",self.Exclude