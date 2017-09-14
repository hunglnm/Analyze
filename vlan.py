class VLAN:
    Hostname = ""
    def __init__(self):
        self.Vlan = 0
        self.Description=""
        self.L2_age_time=14400
    def showdata(self):
        print self.Hostname
        print self.Vlan
        print self.Description

    def insert(self, cursor):
        add_vlan = ("INSERT INTO VLAN "
                        "(Vlan,Hostname,Description,L2_age_time) "
                        "VALUES (%s,%s,%s,%s) "
                        "ON DUPLICATE KEY UPDATE Description=VALUES(Description),L2_age_time=VALUES(L2_age_time)")
        data_vlan = (self.Vlan,VLAN.Hostname,self.Description,self.L2_age_time)
        cursor.execute(add_vlan, data_vlan)
