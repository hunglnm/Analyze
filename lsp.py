class LSP:
    Hostname = ""

    def __init__(self):
        self.Name = ""
        self.Description = ""
        self.Dest = ""
        self.Path = ""
        self.Src =""
        self.VRF_Name =""
        self.Backup_path=""
        self.Admin_status=True
        self.TE = False
        self.FRR= False
        self.bfd = False
        self.bfd_info = ''
        self.Metric = 0
        self.Bk_path_org = False
        self.Bk_host_stb = False

    def showdata(self):
        attrs = vars(self)
        print LSP.Hostname,',',','.join("%s: %s" % item for item in attrs.items())

    def insert(self, cursor):
        add_lsp = ("INSERT INTO LSP "
                   "(Name,Hostname,Description,Dest,Path,Src,VRF_Name,Backup_path,Admin_status,TE,FRR,Metric,BFD,"
                   "BFD_info,Bk_path_org,Bk_host_stb) "
                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                   "ON DUPLICATE KEY UPDATE Description=VALUES(Description), "
                   "Dest=VALUES(Dest),Path=VALUES(Path),Src=VALUES(Src),VRF_Name=VALUES(VRF_Name), "
                   "Backup_path=VALUES(Backup_path),Admin_status=VALUES(Admin_status),TE=VALUES(TE),"
                   "FRR=VALUES(FRR),Metric=VALUES(Metric),BFD=VALUES(BFD),BFD_info=VALUES(BFD_info),"
                   "Bk_path_org=VALUES(Bk_path_org),Bk_host_stb=VALUES(Bk_host_stb)")
        data_lsp = (self.Name,LSP.Hostname,self.Description,self.Dest,self.Path,self.Src,self.VRF_Name,
                    self.Backup_path,self.Admin_status,self.TE,self.FRR,self.Metric,self.bfd,self.bfd_info,
                    self.Bk_path_org,self.Bk_host_stb)
        cursor.execute(add_lsp, data_lsp)