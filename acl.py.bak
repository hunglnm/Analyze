import MySQLdb

class ACL:
    Hostname = ""

    def __init__(self):
        self.Name = ""
        self.Type = ""
        self.Description =""
        self.Purpose = ""

    def showdata(self):
        attrs = vars(self)
        print ACL.Hostname,',',','.join("%s: %s" % item for item in attrs.items())

    def insert(self, cursor):
        add_acl = ("INSERT INTO ACL "
                   "(Name, Hostname, Description, Type,Purpose) "
                   "VALUES (%s,%s,%s,%s,%s) "
                   "ON DUPLICATE KEY UPDATE Description=VALUES(Description),Type=VALUES(Type),Purpose=VALUES(Purpose)")
        data_acl = (self.Name, ACL.Hostname, self.Description, self.Type, self.Purpose)
        cursor.execute(add_acl, data_acl)


class ACL_detail:
    Hostname = ""

    def __init__(self):
        self.Name = ""
        self.Index_1 = 0
        self.Action_1 = ""
        self.Protocol_1 = ""
        self.Prefix_Source = ""
        self.S_Port = ""
        self.Prefix_Dest = ""
        self.D_Port = ""
        self.Option_1 = ""
        self.IP_Pre =""
        self.ToS = ""
        self.DSCP= ""
        self.Log = False
        self.VRF_Name = ''

    def showdata(self):
        attrs = vars(self)
        print ACL_detail.Hostname, ',', ','.join("%s: %s" % item for item in attrs.items())

    def insert(self, cursor):
        add_acl_detail = ("INSERT INTO ACL_detail "
                          "(Name, Hostname, Index_1, Action_1, Protocol_1, Prefix_Source, S_Port, Prefix_Dest,"
                          "D_Port, Option_1, IP_Pre, ToS, DSCP, Log,VRF_Name) "
                          "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                          "ON DUPLICATE KEY UPDATE Action_1=VALUES(Action_1), Protocol_1=VALUES(Protocol_1), "
                          "Prefix_Source=VALUES(Prefix_Source),S_Port=VALUES(S_Port),Prefix_Dest=VALUES(Prefix_Dest), "
                          "D_Port=VALUES(D_Port),Option_1=VALUES(Option_1),IP_Pre=VALUES(IP_Pre), "
                          "ToS=VALUES(ToS),DSCP=VALUES(DSCP), Log=VALUES(Log),VRF_Name=VALUES(VRF_Name)")
        data_acl_detail = (self.Name, ACL_detail.Hostname, self.Index_1, self.Action_1, self.Protocol_1,
                           self.Prefix_Source, self.S_Port, self.Prefix_Dest, self.D_Port, self.Option_1,
                           self.IP_Pre, self.ToS, self.DSCP, self.Log,self.VRF_Name)
        cursor.execute(add_acl_detail, data_acl_detail)

    @staticmethod
    def convert_acl_detail(info):
        temp_acl_detail = ACL_detail()
        temp_acl_detail.Name = info[0]
        temp_acl_detail.Index_1 = info[1]
        temp_acl_detail.Action_1 = info[2]
        temp_acl_detail.Protocol_1 = info[3]
        temp_acl_detail.Prefix_Source = info[4]
        temp_acl_detail.S_Port = info[5]
        temp_acl_detail.Prefix_Dest = info[6]
        temp_acl_detail.D_Port = info[7]
        return temp_acl_detail