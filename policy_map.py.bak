class Policy_map:
    Hostname = ""

    def __init__(self):
        self.Name = ""
        self.Class = ""
        self.Police = 0
        self.Shape = 0
        self.CIR = 0
        self.BC = 0
        self.PIR = 0
        self.BE = ''
        self.Set_prec_transmit = ""
        self.Set_EXP=""
        self.Conform_action = ""
        self.Exceed_action = ""
        self.Violate_action = ""
        self.BW = 0
        self.Priority=""
        self.Queue_limit = 0
        self.Service_policy = ""
        self.RED_Agg = False
        self.RED_Pre = ""
        self.RED_Min = ""
        self.RED_Max = ""
        self.RED_Mark = ""
        self.p1 = ''
        self.FC= ''
        self.LP = ''
        self.set_p1 = ''
        self.dscp = ''
        self.set_dscp = ''
        self.acl = ''

    def showdata(self):
        attrs = vars(self)
        print Policy_map.Hostname, ',', ','.join("%s: %s" % item for item in attrs.items())

    def insert(self, cursor):
        add_policy_map = ("INSERT INTO Policy_map "
                          "(Name,Hostname,Class,Police,Shape,CIR,BC,PIR,BE,Set_prec_transmit,Set_EXP, "
                          "Conform_action,Exceed_action,Violate_action,BW,Priority,Queue_limit, "
                          "Service_policy,RED_Agg,RED_Pre,RED_Min,RED_Max,RED_Mark,8021p,FC,LP,Set_1p,DSCP,Set_dscp,"
                          "ACL) "
                          "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                          "%s,%s,%s,%s) "
                          "ON DUPLICATE KEY UPDATE Police=VALUES(Police),Shape=VALUES(Shape),CIR=VALUES(CIR), "
                          "BC=VALUES(BC),PIR=VALUES(PIR),BE=VALUES(BE),Set_prec_transmit=VALUES(Set_prec_transmit), "
                          "Set_EXP=VALUES(Set_EXP),Conform_action=VALUES(Conform_action), "
                          "Exceed_action=VALUES(Exceed_action),Violate_action=VALUES(Violate_action), "
                          "BW=VALUES(BW),Priority=VALUES(Priority),Queue_limit=VALUES(Queue_limit), "
                          "Service_policy=VALUES(Service_policy),RED_Agg=VALUES(RED_Agg),RED_Pre=VALUES(RED_Pre), "
                          "RED_Min=VALUES(RED_Min),RED_Max=VALUES(RED_Max),RED_Mark=VALUES(RED_Mark),"
                          "8021p=VALUES(8021p),FC=VALUES(FC),LP=VALUES(LP),Set_1p=VALUES(Set_1p),DSCP=VALUES(DSCP),"
                          "Set_dscp=VALUES(Set_dscp),ACL=VALUES(ACL)")
        data_policy_map = (self.Name,Policy_map.Hostname,self.Class,self.Police,self.Shape,self.CIR, \
                           self.BC,self.PIR,self.BE,self.Set_prec_transmit,self.Set_EXP,self.Conform_action,self.Exceed_action, \
                           self.Violate_action,self.BW,self.Priority,self.Queue_limit,self.Service_policy, \
                           self.RED_Agg,self.RED_Pre,self.RED_Min,self.RED_Max,self.RED_Mark,self.p1,self.FC,self.LP,
                           self.set_p1,self.dscp,self.set_dscp,self.acl)
        cursor.execute(add_policy_map, data_policy_map)