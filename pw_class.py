class PW_Class:
    Hostname = ""

    def __init__(self):
        self.Name = ""
        self.LSP = ""
        self.Dest = ''

    def showdata(self):
        attrs = vars(self)
        print PW_Class.Hostname, ',', ','.join("%s: %s" % item for item in attrs.items())

    def insert(self, cursor):
        add_pw_class = ("INSERT INTO PW_Class "
                        "(Name,Hostname,LSP,Dest) "
                        "VALUES (%s,%s,%s,%s) "
                        "ON DUPLICATE KEY UPDATE LSP=VALUES(LSP),Dest=VALUES(Dest)")
        data_pw_class = (self.Name, PW_Class.Hostname, self.LSP,self.Dest)
        cursor.execute(add_pw_class, data_pw_class)