class BFD:
    Hostname = ""

    def __init__(self):
        self.Name = ''
        self.VRF_Name = ''
        self.Peer_ip = ''
        self.Source_ip = ''
        self.IFL = ''
        self.Disc_local = 0
        self.Disc_remote = 0
        self.Process_intf = False
        self.Multiplier = 0
        self.Min_tx = 0
        self.Min_rx = 0
        self.Wtr = 0

    def showdata(self):
        attrs = vars(self)
        print BFD.Hostname,',',','.join("%s: %s" % item for item in attrs.items())

    def insert(self, cursor):
        add_bfd = ("INSERT INTO BFD "
                   "(Name,Hostname,VRF_Name,Peer_ip,Source_ip,IFL,Disc_local,Disc_remote,Process_intf,"
                   "Multiplier,Min_tx,Min_rx,Wtr) "
                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                   "ON DUPLICATE KEY UPDATE VRF_Name=VALUES(VRF_Name),Peer_ip=VALUES(Peer_ip), "
                   "Source_ip=VALUES(Source_ip),IFL=VALUES(IFL),Disc_local=VALUES(Disc_local),Disc_remote=VALUES(Disc_remote), "
                   "Process_intf=VALUES(Process_intf),Multiplier=VALUES(Multiplier),Min_tx=VALUES(Min_tx), "
                   "Min_rx=VALUES(Min_rx),Wtr=VALUES(Wtr)")
        data_bfd = (self.Name,BFD.Hostname,self.VRF_Name,self.Peer_ip,self.Source_ip,self.IFL,self.Disc_local,self.Disc_remote,
                    self.Process_intf,self.Multiplier,self.Min_tx,self.Min_rx,self.Wtr)
        cursor.execute(add_bfd, data_bfd)
