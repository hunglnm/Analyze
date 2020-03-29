class Redistribute:
    Hostname = ""

    def __init__(self):
        self.VRF_Name = ""
        self.Type = ""
        self.Metric = 0
        self.level = ""

    def showdata(self):
        attrs = vars(self)
        print(Redistribute.Hostname,','.join("%s: %s" % item for item in list(attrs.items())))

    def insert(self, cursor):
        add_redistribute = ("INSERT INTO Redistribute "
                            "(VRF_Name,Type,Hostname,Metric,Level) "
                            "VALUES (%s,%s,%s,%s,%s) "
                            "ON DUPLICATE KEY UPDATE "
                            "VRF_Name=VALUES(VRF_Name),Type=VALUES(Type),Hostname=VALUES(Hostname), "
                            "Metric=VALUES(Metric),Level=VALUES(Level)")

        data_redistribute = (self.VRF_Name,self.Type,Redistribute.Hostname,self.Metric,self.level)
        cursor.execute(add_redistribute, data_redistribute)