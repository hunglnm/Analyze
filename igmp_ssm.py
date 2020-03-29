class IGMP_SSM:
    Hostname = ""

    def __init__(self):
        self.ACL = ""
        self.Source = ""

    def showdata(self):
        print(self.Hostname)
        print(self.ACL)
        print(self.Source)

    def insert(self, cursor):
        add_igmp_ssm = ("INSERT INTO IGMP_SSM "
                        "(ACL,Hostname,Source) "
                        "VALUES (%s,%s,%s) "
                        "ON DUPLICATE KEY UPDATE ACL=VALUES(ACL),Hostname=VALUES(Hostname),Source=VALUES(Source)")
        data_igmp_ssm = (self.ACL,IGMP_SSM.Hostname,self.Source)
        cursor.execute(add_igmp_ssm, data_igmp_ssm)