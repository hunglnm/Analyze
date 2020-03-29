from mysql.connector import MySQLConnection,Error
import mysql.connector

class CLI_Router:
    Hostname = ""

    def __init__(self):
        self.Line = 0
        self.CLI = ""
        self.Note=""

    def insert(self,cursor):
        add_cli_router = ("INSERT INTO CLI_Router "
                          "(Hostname,Line,CLI) "
                          "VALUES (%s,%s,%s) "
                          "ON DUPLICATE KEY UPDATE CLI=VALUES(CLI)")
        data_cli_router = (CLI_Router.Hostname, self.Line, self.CLI)
        cursor.execute(add_cli_router, data_cli_router)

    @staticmethod
    def query(self,cursor):
        query_cli_router = ("SELECT * FROM CLI_Router "
                            "WHERE Hostname='%s' AND Line='%d'")
        data_cli_router = (CLI_Router.Hostname,self.Line)
        cursor.execute(query_cli_router,data_cli_router)
        return cursor.fetchall()

    @staticmethod
    def delete(self,cursor):
        delete_cli_router = ("DELETE * FROM CLI_Router "
                             "WHERE Hostname='%s'")
        data_cli_router = (CLI_Router.Hostname)

        cursor.execute(delete_cli_router, data_cli_router)

    def getdata(self,result_query):
        for row in result_query:
            print row #Xu ly truoc khi print


