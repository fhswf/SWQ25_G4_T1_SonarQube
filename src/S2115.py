from mysql.connector import connection
import os
password = os.getenv('DB_PASSWORD')
connection.MySQLConnection(host='localhost', user='sonarsource', password=password)  # Noncompliant


class MyClass(object):
    def __init__(self):
        self.message = 'Hello'



def myfunc(param):
    if param is None:
        print(param.test())   



#adding something for commit