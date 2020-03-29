import pymysql

class VRF_IE:
    Hostname = ""

    def __init__(self):
        self.Name = ""
        self.Seq=0
        self.VRF_Name=""
        self.ACL=""
        self.Extcomm=""
        self.IE = ""
        self.Action=""
        self.protocol = ''
        self.route_filter=''

    def showdata(self):
        attrs = vars(self)
        print(VRF_IE.Hostname,',',','.join("%s: %s" % item for item in list(attrs.items())))

    def insert(self, cursor):
        add_l3vpn_ie = ("INSERT INTO VRF_IE "
                        "(Name,Hostname,Seq,VRF_Name,ACL,Extcomm,IE,Action,Protocol,Route_filter) "
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                        "ON DUPLICATE KEY UPDATE ACL=VALUES(ACL),Extcomm=VALUES(Extcomm),IE=VALUES(IE), "
                        "Action=VALUES(Action),Protocol=VALUES(Protocol),Route_filter=VALUES(Route_filter)")
        data_l3vpn_ie = (self.Name,VRF_IE.Hostname,self.Seq,self.VRF_Name,self.ACL,self.Extcomm,self.IE,
                         self.Action,self.protocol,self.route_filter)
        cursor.execute(add_l3vpn_ie, data_l3vpn_ie)
'''
    @staticmethod
    def extract_data(hostname, cursor):
        temp_sql = "SELECT Name,Seq,VRF_Name,ACL,Extcomm,IE,Action,Protocol FROM VRF_IE WHERE Hostname = '%s' " \
                   "and IE='exp' ;" % hostname
        cursor.execute(temp_sql)
        temp_list = cursor.fetchall()
        temp_dict = {}
        for item in temp_list:
            temp_vrf_ie = VRF_IE()
            temp_vrf_ie.Name = item[0]
            temp_vrf_ie.Seq = item[1]
            temp_vrf_ie.VRF_Name = item[2]
            temp_vrf_ie.ACL = item[3]
            temp_vrf_ie.Extcomm = item[4]
            temp_vrf_ie.IE = item[5]
            temp_vrf_ie.Action = item[6]
            temp_vrf_ie.protocol = item[7]
            temp_dict[temp_vrf_ie.VRF_Name+'_'+temp_vrf_ie.Name+'_'+str(temp_vrf_ie.Seq)] = temp_vrf_ie
        return temp_dict
'''