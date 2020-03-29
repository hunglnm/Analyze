class VSI:
    Hostname = ''

    def __init__(self):
        self.name = ''
        self.vsi_id = 0
        self.type = ''
        self.isolate = False
        self.classifier = ''
        self.encap ='tagged'
        self.MTU = 1500
        self.tnl_policy = ''
        self.mac_limit = 0
        self.loop_detect = False
        self.admin_vsi = False
        self.track_admin_vsi = False
        self.un_unicast= False
        self.un_multicast = False
        self.description = ''
        self.Admin_status=True

    def showdata(self):
        attrs = vars(self)
        print(VSI.Hostname,',',','.join("%s: %s" % item for item in list(attrs.items())))

    def insert(self, cursor):
        add_vsi = ("INSERT INTO VSI "
                   "(Name,Hostname,Vsi_id,Isolate,Classifier,Encap,MTU,Tnl_policy,Mac_limit,Loop_detect,Admin_vsi,"
                   "Track_admin_vsi,Type,un_unicast,un_multicast,Description,Admin_status) "
                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                   "ON DUPLICATE KEY UPDATE Vsi_id=VALUES(Vsi_id),Isolate=VALUES(Isolate),"
                   "Classifier=VALUES(Classifier),Encap=VALUES(Encap),MTU=VALUES(MTU),Tnl_policy=VALUES(Tnl_policy), "
                   "Mac_limit=VALUES(Mac_limit),Loop_detect=VALUES(Loop_detect),Admin_vsi=VALUES(Admin_vsi), "
                   "Track_admin_vsi=VALUES(Track_admin_vsi),Type=VALUES(Type),un_unicast=VALUES(un_unicast),"
                   "un_multicast=VALUES(un_multicast),Description=VALUES(Description),Admin_status=VALUES(Admin_status)")
        data_vsi = (self.name,self.Hostname,self.vsi_id,self.isolate,self.classifier,self.encap,self.MTU,
                    self.tnl_policy,self.mac_limit,self.loop_detect,self.admin_vsi,self.track_admin_vsi,
                    self.type,self.un_unicast,self.un_multicast,self.description,self.Admin_status)
        cursor.execute(add_vsi, data_vsi)

class L2VPN:
    Hostname = ""

    def __init__(self):
        self.Peer = ""
        self.VC_ID = 0
        self.Name =""
        self.BD_ID = ""
        self.No_split = False
        self.BK_Peer = ""
        self.Type = ""
        self.PW_Class = ""
        self.MTU = 0
        self.Encap =""
        self.Description = ""
        self.VPN_ID=0
        self.IFL = ""
        self.mac_limit = 0
        self.Meshgroup = ''
        self.Admin_status = True
        self.UPE = False
        self.BUM = 0
        self.Bk_vc_id = 0
        self.PW_class_bk = ''
        self.UPE_bk = False
        self.CW = False
        self.Bk_cw = False


    def showdata(self):
        attrs = vars(self)
        print(L2VPN.Hostname,',',','.join("%s: %s" % item for item in list(attrs.items())))

    def insert(self, cursor):
        add_l2vpn = ("INSERT INTO L2VPN "
                     "(Peer,Hostname,VC_ID,Name,BD_ID,No_split,BK_Peer,Type,PW_Class,MTU,Encap,Description,VPN_ID"
                     ", IFL, Mac_limit, Meshgroup,Admin_status,UPE,BUM,BK_vc_id,PW_class_bk,UPE_bk,CW,Bk_cw) "
                     "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                     "ON DUPLICATE KEY UPDATE Name=VALUES(Name),BD_ID=VALUES(BD_ID), "
                     "No_split=VALUES(No_split),BK_Peer=VALUES(BK_Peer), "
                     "Type=VALUES(Type),PW_Class=VALUES(PW_Class),MTU=VALUES(MTU),Encap=VALUES(Encap), "
                     "Description=VALUES(Description),VPN_ID=VALUES(VPN_ID),IFL=VALUES(IFL),"
                     "Mac_limit=VALUES(Mac_limit),Meshgroup=VALUES(Meshgroup),Admin_status=VALUES(Admin_status), "
                     "UPE=VALUES(UPE),BUM=VALUES(BUM),BK_vc_id=VALUES(BK_vc_id),PW_class_bk=VALUES(PW_class_bk), "
                     "UPE_bk=VALUES(UPE_bk),CW=VALUES(CW),Bk_cw=VALUES(Bk_cw)")
        data_l2vpn = (self.Peer, L2VPN.Hostname, self.VC_ID, self.Name, self.BD_ID, self.No_split, self.BK_Peer,
                      self.Type, self.PW_Class, self.MTU, self.Encap, self.Description, self.VPN_ID,self.IFL,
                      self.mac_limit,self.Meshgroup,self.Admin_status,self.UPE,self.BUM,self.Bk_vc_id,self.PW_class_bk,
                      self.UPE_bk,self.CW,self.Bk_cw)
        cursor.execute(add_l2vpn, data_l2vpn)

    def insert_ifl(self, cursor):
        add_l2vpn = ("INSERT INTO L2VPN "
                        "(Peer,Hostname,VC_ID,IFL ) "
                        "VALUES (%s,%s,%s,%s) "
                        "ON DUPLICATE KEY UPDATE IFL=VALUES(IFL)")
        data_l2vpn = (self.Peer, L2VPN.Hostname, self.VC_ID,self.IFL)
        cursor.execute(add_l2vpn, data_l2vpn)