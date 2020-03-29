class OSPF:
    Hostname = ""

    def __init__(self):
        self.Name =""
        self.VRF_Name = ""
        self.Ref_BW=0
        self.Redistribute=""
        self.DF=""
        self.Authen=""
        self.Admin_Status=""
    def showdata(self):
        print(self.Name)
        print(self.Hostname)
        print(self.VRF_Name)
        print(self.Ref_BW)
        print(self.Redistribute)
        print(self.DF)
        print(self.Authen)
        print(self.Admin_Status)

    def insert(self, cursor):
        add_ospf = ("INSERT INTO OSPF "
                        "(Name,Hostname,VRF_Name,Ref_BW,Redistribute,DF,Authen,Admin_Status) "
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s) "
                        "ON DUPLICATE KEY UPDATE VRF_Name=VALUES(VRF_Name),Ref_BW=VALUES(Ref_BW), "
                        "Redistribute=VALUES(Redistribute),DF=VALUES(DF),Authen=VALUES(Authen), "
                        "Admin_Status=VALUES(Admin_Status)")
        data_ospf = (self.Name, OSPF.Hostname, self.VRF_Name,self.Ref_BW,self.Redistribute,self.DF,self.Authen, \
                     self.Admin_Status)
        cursor.execute(add_ospf, data_ospf)


