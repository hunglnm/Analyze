class Static_Route:
    Hostname=""

    def __init__(self):
        self.Net = ""
        self.VRF_Name = ""
        self.Intf_name = ""
        self.NH = ""
        self.Track_ID = 0
        self.AD = 0
        self.tag = 0
        self.BFD = ''
        self.description = ''

    def showdata(self):
        attrs = vars(self)
        print Static_Route.Hostname,',',','.join("%s: %s" % item for item in attrs.items())

    def insert(self, cursor):
        add_static =("INSERT INTO Static_route "
                     "(Net,VRF_Name,Hostname,Intf_name,NH,Track_ID,AD,tag,BFD,Description) "
                     "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                     "ON DUPLICATE KEY UPDATE "
                     "Intf_name=VALUES(Intf_name),NH=VALUES(NH),Track_ID=VALUES(Track_ID),AD=VALUES(AD), "
                     "tag=VALUES(tag),BFD=VALUES(BFD),Description=VALUES(Description)")
        data_static = (self.Net,self.VRF_Name,Static_Route.Hostname,self.Intf_name,self.NH,
                       self.Track_ID,self.AD,self.tag,self.BFD,self.description)
        cursor.execute(add_static, data_static)