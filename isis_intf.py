class ISIS_INTF:
    Hostname=""
    def __init__(self):
        self.IFL = ""
        self.VRF_Name = ""
        self.ISIS = ""
        self.Passive = False

    def showdata(self):
        attrs = vars(self)
        print(ISIS_INTF.Hostname,',',','.join("%s: %s" % item for item in list(attrs.items())))

    def insert(self, cursor):
        add_isis_ifl = ("INSERT INTO ISIS_INTF "
                        "(IFL,Hostname,VRF_Name,ISIS,Passive) "
                        "VALUES (%s,%s,%s,%s,%s) "
                        "ON DUPLICATE KEY UPDATE VRF_Name=VALUES(VRF_Name), "
                        "ISIS=VALUES(ISIS),Passive=VALUES(Passive)")
        data_isis_ifl = (self.IFL, ISIS_INTF.Hostname, self.VRF_Name,self.ISIS,self.Passive)
        cursor.execute(add_isis_ifl, data_isis_ifl)

    def insert_passive(self, cursor):
        add_isis_ifl = ("INSERT INTO ISIS_INTF "
                        "(IFL,Hostname,VRF_Name,ISIS,Passive) "
                        "VALUES (%s,%s,%s,%s,%s) "
                        "ON DUPLICATE KEY UPDATE VRF_Name=VALUES(VRF_Name),ISIS=VALUES(ISIS),Passive=VALUES(Passive)")
        data_isis_ifl = (self.IFL, ISIS_INTF.Hostname,self.VRF_Name,self.ISIS,self.Passive)
        cursor.execute(add_isis_ifl, data_isis_ifl)