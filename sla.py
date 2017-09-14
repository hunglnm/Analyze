class SLA:
    Hostname = ""

    def __init__(self):
        self.SLA_ID = 0
        self.VRF_Name = ""
        self.Dest = ""
        self.Src = ""
        self.Track = 0
        self.Data_size=0
        self.Timeout = 0
        self.Freq=0
        self.Start = ""
        self.local_pw_id = 0
        self.test_type = ''
        self.test_name = ''
        self.role = ''
        self.s_port = 0
        self.d_port = 0
        self.probe = ''
        self.fail_percent = 0

    def showdata(self):
        attrs = vars(self)
        print SLA.Hostname,',',','.join("%s: %s" % item for item in attrs.items())

    def insert(self, cursor):
        add_sla = ("INSERT INTO SLA "
                   "(SLA_ID,Hostname,VRF_Name,Dest,Src,Track,Data_size,Timeout,Freq,Start,Local_pw_id,"
                   "Test_type,Test_name,Role,S_port,Probe,D_Port,Fail_percent) "
                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                   "ON DUPLICATE KEY UPDATE VRF_Name=VALUES(VRF_Name),Dest=VALUES(Dest), "
                   "Src=VALUES(Src),Track=VALUES(Track),Data_size=VALUES(Data_size), "
                   "Timeout=VALUES(Timeout),Freq=VALUES(Freq),Start=VALUES(Start), "
                   "Local_pw_id=VALUES(Local_pw_id),Test_type=VALUES(Test_type),Test_name=VALUES(Test_name), "
                   "Role=VALUES(Role),S_port=VALUES(S_port),Probe=VALUES(Probe),D_port=VALUES(D_port), "
                   "Fail_percent=VALUES(Fail_percent)")
        data_sla = (self.SLA_ID,SLA.Hostname,self.VRF_Name,self.Dest,self.Src,self.Track,self.Data_size,self.Timeout,
                    self.Freq,self.Start,self.local_pw_id,self.test_type,self.test_name,self.role,self.s_port,
                    self.probe,self.d_port,self.fail_percent)
        cursor.execute(add_sla, data_sla)
