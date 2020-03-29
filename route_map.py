import pymysql
import re

class Route_map:
    Hostname=""

    def __init__(self):
        self.Name = ""
        self.Seq = 0
        self.ACL = ""
        self.Extcomm = ""
        self.Action_1 = ""

    def showdata(self):
        attrs = vars(self)
        print(Route_map.Hostname,',',','.join("%s: %s" % item for item in list(attrs.items())))

    def insert(self, cursor):
        add_route_map =("INSERT INTO Route_map "
                        "(Name,Hostname,Seq,ACL,Extcomm,Action_1) "
                        "VALUES (%s,%s,%s,%s,%s,%s) "
                        "ON DUPLICATE KEY UPDATE "
                        "ACL=VALUES(ACL),Extcomm=VALUES(Extcomm),Action_1=VALUES(Action_1)")
        data_route_map = ( self.Name, Route_map.Hostname, self.Seq, self.ACL, self.Extcomm ,self.Action_1)
        cursor.execute(add_route_map, data_route_map)

    @staticmethod
    def get_route_policy(temp_list,total_line):
        dict_route_policy = {}
        i=0
        while i < total_line:
            if re.match('route-policy ([\S]*) permit node ([\d]*)\n',temp_list[i]):
                temp_search = re.match('route-policy ([\S]*) permit node ([\d]*)\n',temp_list[i]).groups()
                temp_route_map = Route_map()
                temp_route_map.Name = temp_search[0]
                temp_route_map.Seq = int(temp_search[1])
                temp_route_map.Action_1 = 'accept'
                i +=1
                while temp_list[i]!='#\n':
                    if re.match(' if-match ip-prefix ([\S]*)\n',temp_list[i]):
                        temp_route_map.ACL = re.match(' if-match ip-prefix ([\S]*)\n',temp_list[i]).groups()[0]
                    elif re.match(' apply local-preference ([\d]*)\n',temp_list[i]):
                        temp_route_map.Action_1 = 'local-preference ' + \
                                                  re.match(' apply local-preference ([\d]*)\n', temp_list[i]).groups()[0]
                    elif re.match(' apply as-path((?:[\s][\d]*)+) additive',temp_list[i]):
                        temp_route_map.Action_1 = 'as-path-prepend '+\
                                                  re.match(' apply as-path((?:[\s][\d]*)+) additive',temp_list[i]).groups()[0]
                    i += 1
                i -= 1
                dict_route_policy[temp_route_map.Name+'/'+str(temp_route_map.Seq)]=temp_route_map
            i += 1
        return dict_route_policy
