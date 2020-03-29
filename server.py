class Server:
    Hostname=""

    def __init__(self):
        self.IP = ""
        self.Purpose = ""
        self.Key = ""
        self.Source = ""
        self.ACL = ''
        self.pref = False

    def showdata(self):
        attrs = vars(self)
        print(Server.Hostname,',',','.join("%s: %s" % item for item in list(attrs.items())))

    def insert(self, cursor):
        add_server =("INSERT INTO Server "
                     "(IP,Hostname,Source,Purpose,ACL,Prefer) "
                     "VALUES (%s,%s,%s,%s,%s,%s)"
                     "ON DUPLICATE KEY UPDATE "
                     "Source=VALUES(Source) ,Purpose=VALUES(Purpose),ACL=VALUES(ACL),Prefer=VALUES(Prefer)")
        data_server = (self.IP, Server.Hostname, self.Source, self.Purpose,self.ACL,self.pref)
        cursor.execute(add_server, data_server)