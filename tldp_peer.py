class TLDP_Peer:
    Hostname=""

    def __init__(self):
        self.IP = ""
        self.PWD = ""
        self.desc = ""

    def showdata(self):
        attrs = vars(self)
        print(TLDP_Peer.Hostname, ',', ','.join("%s: %s" % item for item in list(attrs.items())))

    def insert(self, cursor):
        add_tldp_peer = ("INSERT INTO TLDP_Peer "
                         "(IP,Hostname,PWD,Descr) "
                         "VALUES (%s,%s,%s,%s) "
                         "ON DUPLICATE KEY UPDATE PWD=VALUES(PWD),Descr=VALUES(Descr)")
        data_tldp_peer = (self.IP,TLDP_Peer.Hostname,self.PWD,self.desc)
        cursor.execute(add_tldp_peer, data_tldp_peer)
