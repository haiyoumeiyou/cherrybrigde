import pyodbc

class ODBCHandler(object):

    def __init__(self, odbc_conf):
        self.odbc_conf = odbc_conf

    def _create_conn(self):
        return pyodbc.connect(self.odbc_conf)

    def _close_conn(self, conn):
        conn.close()

    def _get_many(self, query:str, params:tuple):
        conn = self._create_conn()
        c = conn.cursor()

        try:
            c.execute(query, params)
            rows = c.fetchall()
            columns = [column[0] for column in c.description]
            rs = []
            for row in rows:
                result = dict(zip(columns, row))
                rs.append(result)
            self._close_conn(conn)
            return rs
        except pyodbc.Error as err:
            self._close_conn(conn)
            return err

    def _get_self(self, query:str, params:tuple):
        conn = self._create_conn()
        c = conn.cursor()

        try:
            c.execute(query, params)
            row = c.fetchone()
            columns = [column[0] for column in c.description]
            result = dict(zip(columns, row))
            self._close_conn(conn)
            return result
        except pyodbc.Error as err:
            self._close_conn(conn)
            return err

    def _insert_many(self, query:str, dataset:list):
        conn = self._create_conn()
        c = conn.cursor()

        try:
            c.execute(query, dataset)
            conn.commit()
            self._close_conn(conn)
            return True
        except pyodbc.Error as err:
            self._close_conn(conn)
            return err

    def _insert_self(self, query:str, data:tuple):
        conn = self._create_conn()
        c = conn.cursor()

        try:
            c.execute(query, data)
            conn.commit()
            self._close_conn(conn)
            return True
        except pyodbc.Error as err:
            self._close_conn(conn)
            return err

    def _update(self, query:str, params:tuple):
        conn = self._create_conn()
        c = conn.cursor()

        try:
            c.execute(query, parems)
            conn.commit()
            self._close_conn(conn)
            return True
        except pyodbc.Error as err:
            self._close_conn(conn)
            return err

    
class HrdbHandler(ODBCHandler):

    def __init__(self, hrdb_conf):
        super().__init__(hrdb_conf)
        # print(self.odbc_conf)

    