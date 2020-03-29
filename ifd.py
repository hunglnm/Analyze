class IFD:
    Hostname = ""

    def __init__(self):
        self.Name = ""
        self.Type = ""
        self.Parent_link = ""
        self.MTU = 0
        self.Dampening = False
        self.Description = ""
        self.AE_type = ""
        self.AE_mode = ""
        self.Service_pol_out=""
        self.Media_type=""
        self.Admin_status = True
        self.Speed =""
        self.MX_IFD=""
        self.Flex_vlan_tag = False
        self.Vlan_tag = False
        self.Flex_service = False
        self.Wanphy=False
        self.weight = 0
        self.native_vlan = ''

    def showdata(self):
        attrs = vars(self)
        print(IFD.Hostname,',',','.join("%s: %s" % item for item in list(attrs.items())))

    def insert(self, cursor):
        add_ifd = ("INSERT INTO IFD "
                   "(Name,Hostname,Type,Parent_link,MTU,Dampening,Description,AE_type,AE_mode,Service_pol_out, "
                   "Media_type,Admin_status,Speed,Flex_vlan_tag,Vlan_tag,Flex_service,Wanphy,Weight,Native_vlan) "
                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                   "ON DUPLICATE KEY UPDATE Type=VALUES(Type),Parent_link=VALUES(Parent_link),MTU=VALUES(MTU), "
                   "Dampening=VALUES(Dampening),Description=VALUES(Description),AE_Type=VALUES(AE_Type), "
                   "AE_mode=VALUES(AE_mode),Service_pol_out=VALUES(Service_pol_out),Media_type=VALUES(Media_type), "
                   "Admin_status=VALUES(Admin_status),Speed=VALUES(Speed),Flex_vlan_tag=VALUES(Flex_vlan_tag), "
                   "Vlan_tag=VALUES(Vlan_tag),Flex_service=VALUES(Flex_service),Wanphy=VALUES(Wanphy),Weight=VALUES"
                   "(Weight),Native_vlan=VALUES(Native_vlan) ")
        data_ifd = (self.Name,IFD.Hostname,self.Type,self.Parent_link,self.MTU,self.Dampening,self.Description,
                    self.AE_type,self.AE_mode,self.Service_pol_out,self.Media_type,self.Admin_status,self.Speed,
                    self.Flex_vlan_tag,self.Vlan_tag,self.Flex_service,self.Wanphy,self.weight,self.native_vlan)
        cursor.execute(add_ifd, data_ifd)

