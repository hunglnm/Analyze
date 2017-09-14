class Classmap:
    Hostname = ""

    def __init__(self):
        self.Name = ""
        self.Cond = ""
        self.ACL = ""
        self.MPLS = ""
        self.IP_Pre = ""
        self.DSCP = ""
        self.CoS = ""
        self.or_and = ''
        self.prefix_list = ''

    def showdata(self):
        attrs = vars(self)
        print Classmap.Hostname, ',', ','.join("%s: %s" % item for item in attrs.items())

    def insert(self, cursor):
        add_classmap = ("INSERT INTO Classmap "
                        "(Name,Hostname,Cond,MPLS,IP_Pre,DSCP,CoS,ACL,OR_AND,Prefix_list) "
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                        "ON DUPLICATE KEY UPDATE Cond=VALUES(Cond), "
                        "MPLS=VALUES(MPLS),IP_Pre=VALUES(IP_Pre), "
                        "DSCP=VALUES(DSCP),CoS=VALUES(CoS),ACL=VALUES(ACL),OR_AND=VALUES(OR_AND),"
                        "Prefix_list=VALUES(Prefix_list)")
        data_classmap = (self.Name, Classmap.Hostname, self.Cond, self.MPLS, self.IP_Pre, self.DSCP, self.CoS, self.ACL,
                         self.or_and,self.prefix_list)
        cursor.execute(add_classmap, data_classmap)
