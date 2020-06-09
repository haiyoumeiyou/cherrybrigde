import pyodbc

class HrdbHandler(object):

    def __init__(self, hrdb_conf):
        self.hrdb_conf = hrdb_conf