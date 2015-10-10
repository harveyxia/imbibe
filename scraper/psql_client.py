import psycopg2

class PsqlClient(object):
    def __init__(self, host='lab.zoo.cs.yale.edu', user='hx52', password='whispering'):
        self.conn = psycopg2.connect("host=%s user=%s password=%s" % (host, user, password))
        self.cur = self.conn.cursor()