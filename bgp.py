class BGP:
    Hostname = ""
    BGP_log_change = False
    def __init__(self):
        self.Peer = ""
        self.Local_AS = ""
        self.RID = ""
        self.Peer_group = ""
        self.VRF_Name = ""
        self.Remote_AS = ""
        self.Update_Source = ""
        self.NLRI = ""
        self.DF=""
        self.df_metric =""
        self.BFD_interval = 0
        self.BFD_multiplier =0
        self.Export_policy = ''
        self.Import_policy = ''
        self.Cluster = False
        self.GR = False
        self.description = ''
        self.pw = ''
        self.cluster_id = ''

    def showdata(self):
        attrs = vars(self)
        print(BGP.Hostname,',',BGP.BGP_log_change,',',','.join("%s: %s" % item for item in list(attrs.items())))

    def insert(self, cursor):
        add_bgp = ("INSERT INTO BGP "
                   "(Peer,Hostname,Local_AS,RID,Peer_group,BGP_log_change,VRF_Name,Remote_AS,Update_Source, "
                   "NLRI,DF,df_metric,BFD_interval,BFD_multiplier,Export_policy, Import_policy, Cluster,GR, "
                   "Description,Cluster_id,PW) "
                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                   "ON DUPLICATE KEY UPDATE "
                   "RID=VALUES(RID),Peer_group=VALUES(Peer_group),BGP_log_change=VALUES(BGP_log_change), "
                   "VRF_Name=VALUES(VRF_Name),Remote_AS=VALUES(Remote_AS), "
                   "Update_Source=VALUES(Update_Source),NLRI=VALUES(NLRI), "
                   "DF=VALUES(DF),df_metric=VALUES(df_metric),BFD_interval=VALUES(BFD_interval), "
                   "BFD_multiplier=VALUES(BFD_multiplier),Export_policy=VALUES(Export_policy), "
                   "Import_policy=VALUES(Import_policy), Cluster=VALUES(Cluster),GR=VALUES(GR), "
                   "Description=VALUES(Description),Cluster_id=VALUES(Cluster_id),PW=VALUES(PW)")
        data_bgp = (self.Peer,self.Hostname,self.Local_AS,self.RID,self.Peer_group,BGP.BGP_log_change,
                    self.VRF_Name,self.Remote_AS,self.Update_Source,self.NLRI,self.DF,self.df_metric,
                    self.BFD_interval,self.BFD_multiplier,self.Export_policy,self.Import_policy,self.Cluster,
                    self.GR,self.description,self.cluster_id,self.pw)
        #print data_bgp
        cursor.execute(add_bgp, data_bgp)