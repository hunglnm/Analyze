import MySQLdb


class POLICYMAP:
    def __init__(self, name=''):
        self.name = name
        self.mf_list = []
        self.acl_list = []
        self.df_action = ''
        self.df_fc = ''
        self.df_lp = ''
        self.family_type = ''

    @staticmethod
    def query_policy_name(hostname, cursor):
        try:
            sql = "select Name from policy_map " \
                  "where Hostname = '%s' and CIR= 0 group by Name" % hostname
            cursor.execute(sql)
            list_rows = cursor.fetchall()
            #print list_rows
            list_policy_map = {x[0]: POLICYMAP.insert_item(x[0], hostname, cursor) for x in list_rows}
            return list_policy_map
        except MySQLdb.Error, e:
            print (e)

    @staticmethod
    def insert_item(info, hostname, cursor):
        #print info
        temp_policy_name = POLICYMAP(info)
        temp_policy_name.mf_list = temp_policy_name.get_mf_list(temp_policy_name.name, hostname, cursor)
        #print 'Gia tri MF:',temp_policy_name.mf_list
        temp_policy_name.acl_list = temp_policy_name.get_acl_list(temp_policy_name.name,hostname,cursor)
        #print 'Gia tri ACL:', temp_policy_name.acl_list
        return temp_policy_name

    @staticmethod
    def get_mf_list(info,hostname,cursor):
        try:
            sql = "select Name, Class, 8021p,DSCP,Set_1p,Set_dscp,Set_prec_transmit,Set_EXP,FC,LP from policy_map " \
                  "where Hostname = '%s' and CIR= 0 and Name = '%s' and ACL=''" % (hostname, info)
            cursor.execute(sql)
            list_rows = cursor.fetchall()
            list_mf = []
            if len(list_rows) > 0:
                #print 'MF:',list_rows
                list_mf = list(map(lambda x: MF.insert_mf(x), list_rows))

            return list_mf
        except MySQLdb.Error, e:
            print (e)

    @staticmethod
    def get_acl_list(info, hostname, cursor):
        try:
            sql = "select Name, Class, ACL from policy_map " \
                  "where Hostname = '%s' and CIR= 0 and Name = '%s' and ACL!=''" % (hostname, info)
            cursor.execute(sql)
            list_rows = cursor.fetchall()
            list_acl = []
            if len(list_rows)>0:
                #print 'Gia tri Policy:', info, 'ACL:', list_rows
                list_acl = FF.insert_acl_list(list_rows[0][2], hostname, cursor)

            return list_acl
        except MySQLdb.Error, e:
            print (e)

class FF:
    def __init__(self, name='', Index_1=0,Action_1='',Protocol_1='',Prefix_Source=''
                 , S_Port='',Prefix_Dest='',D_Port=''):
        self.name = name
        self.Index_1 = Index_1
        self.Action_1 = Action_1
        self.Protocol_1 = Protocol_1
        self.Prefix_Source = Prefix_Source
        self.S_Port = S_Port
        self.Prefix_Dest = Prefix_Dest
        self.D_Port = D_Port

    @staticmethod
    def insert_acl(info):
        tmp_acl = FF(name=info[0],Index_1=info[1],Action_1=info[2],Protocol_1=info[3],Prefix_Source=info[4],
                     S_Port=info[5],Prefix_Dest=info[6],D_Port=info[7])
        return tmp_acl

    @staticmethod
    def insert_acl_list(info,hostname,cursor):
        sql = "select Name,Index_1,Action_1,Protocol_1,Prefix_Source,S_Port,Prefix_Dest,D_Port " \
              "from acl_detail where hostname = '%s' and Name = '%s' " % ( hostname,info)
        cursor.execute(sql)
        list_rows = cursor.fetchall()
        tmp_acl_list = list(map(lambda x: FF.insert_acl(x),list_rows))
        return tmp_acl_list

class MF:
    #"Name, Class, ACL, 8021p, DSCP, Set_1p, Set_dscp, Set_prec_transmit, Set_EXP,FC, LP"
    def __init__(self, name, classname='',p1=0,dscp=0,set_1p=0,set_dscp='',set_ip_pre=0,set_exp=0,fc='',
                 lp=''):
        self.name = name
        self.classname = classname
        self.p1 = p1
        self.dscp = dscp
        self.set_1p = set_1p
        self.set_dscp = set_dscp
        self.set_ip_pre = set_ip_pre
        self.set_exp = set_exp
        self.fc = fc
        self.lp = lp

    def showdata(self):
        attrs = vars(self)
        print ','.join("%s: %s" % item for item in attrs.items())

    @staticmethod
    def insert_mf(info):
        tmp_mf = MF(name=info[0], classname=info[1], p1=info[2], dscp=info[3], set_1p=info[4],
                    set_dscp=info[5], set_ip_pre=info[6], set_exp=info[7], fc=info[8], lp=info[9])

        return tmp_mf

