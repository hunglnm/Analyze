class OSPF_Passive:
    Hostname=""
    def __init__(self):
        self.IFL = ""
        self.VRF_Name = ""
        self.OSPF = ""
        self.Passive = False
        self.Area =""

    def showdata(self):
        print self.IFL
        print self.Hostname
        print self.VRF_Name
        print self.OSPF
        print self.Passive
        print self.Area

    def insert(self, cursor):
        add_ospf_ifl = ("INSERT INTO OSPF_Passive "
                        "(IFL,Hostname,VRF_Name,OSPF,Passive,Area) "
                        "VALUES (%s,%s,%s,%s,%s,%s) "
                        "ON DUPLICATE KEY UPDATE VRF_Name=VALUES(VRF_Name), "
                        "OSPF=VALUES(OSPF),Passive=VALUES(Passive),Area=VALUES(Area)")
        data_ospf_ifl = (self.IFL, OSPF_Passive.Hostname, self.VRF_Name,self.OSPF,self.Passive,self.Area)
        cursor.execute(add_ospf_ifl, data_ospf_ifl)