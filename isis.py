class ISIS:
    Hostname=""
    def __init__(self):
        self.Name = ""
        self.VRF_Name = ""
        self.Net = ""
        self.Level = ""
        self.Metric_style = ""
        self.Overloadbit = ""
        self.max_lsp_lifetime = 0
        self.lsp_refresh_interval = 0
        self.Authen_key = ""
        self.Redistribute = ""
        self.Distance=""
        self.Authen_mode=""
        self.Metric =""
        self.DF = ""
        self.gr = False
        self.BW = 0

    def showdata(self):
        attrs = vars(self)
        print(ISIS.Hostname,',',','.join("%s: %s" % item for item in list(attrs.items())))

    def insert(self, cursor):
        add_isis = ("INSERT INTO ISIS "
                    "(Name,Hostname,VRF_Name,Net,Level,Metric_style,Overloadbit,max_lsp_lifetime, "
                    "lsp_refresh_interval,Authen_mode,Authen_key,Redistribute,Distance,Metric,DF,GR,BW) "
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                        "ON DUPLICATE KEY UPDATE VRF_Name=VALUES(VRF_Name),Net=VALUES(Net),Level=VALUES(Level), "
                        "Metric_style=VALUES(Metric_style), "
                        "Overloadbit=VALUES(Overloadbit),max_lsp_lifetime=VALUES(max_lsp_lifetime), "
                        "lsp_refresh_interval=VALUES(lsp_refresh_interval),Authen_mode=VALUES(Authen_mode), "
                        "Authen_key=VALUES(Authen_key),Redistribute=VALUES(Redistribute),Distance=VALUES(Distance),Metric=VALUES(Metric), "
                        "DF=VALUES(DF),GR=VALUES(GR),BW=VALUES(BW)")

        data_isis = (self.Name, ISIS.Hostname, self.VRF_Name,self.Net,self.Level,self.Metric_style,self.Overloadbit,self.max_lsp_lifetime, \
                     self.lsp_refresh_interval,self.Authen_mode,self.Authen_key,self.Redistribute,self.Distance, \
                     self.Metric,self.DF,self.gr,self.BW)
        cursor.execute(add_isis, data_isis)

