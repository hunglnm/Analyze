class Path:
    Hostname = ""

    def __init__(self):
        self.Name = ""
        self.Admin_status=False

    def showdata(self):
        attrs = vars(self)
        print Path.Hostname,',',','.join("%s: %s" % item for item in attrs.items())

    def insert(self, cursor):
        add_path = ("INSERT INTO Path "
                    "(Name, Hostname, Admin_status) "
                    "VALUES (%s,%s,%s) "
                    "ON DUPLICATE KEY UPDATE Admin_status=VALUES(Admin_status)")
        data_path = (self.Name,Path.Hostname,self.Admin_status)
        cursor.execute(add_path, data_path)

class Path_detail:
    Hostname = ""

    def __init__(self):
        self.Name = ""
        self.NH = ""
        self.Index_1 = 0
        self.Type = ""

    def showdata(self):
        attrs = vars(self)
        print Path_detail.Hostname,',',','.join("%s: %s" % item for item in attrs.items())

    def insert(self, cursor):
        add_path_detail = ("INSERT INTO Path_detail "
                           "(Name,Hostname,Index_1,NH,Type) "
                           "VALUES (%s,%s,%s,%s,%s) "
                           "ON DUPLICATE KEY UPDATE NH=VALUES(NH),Type=VALUES(Type)")
        data_path_detail = (self.Name,Path_detail.Hostname,self.Index_1,self.NH,self.Type)
        cursor.execute(add_path_detail, data_path_detail)