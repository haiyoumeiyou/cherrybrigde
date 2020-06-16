import pyodbc

from typing import Dict, List


class DatabaseHandler(object):
    def __init__(self, db_name:str):
        self.db_name = db_name

    def _create_conn(self):
        return pyodbc.connect(self.db_name)

    def _close_conn(self, conn):
        conn.close()

    def get_selve(self, query, params=None):
        with self._create_conn() as conn:
            c = conn.cursor()
            if params is None:
                c.execute(query)
            else:
                c.execute(query, params)
            q_rst = c.fetchall()
            if isinstance(q_rst, List):
                columns = [column[0] for column in c.description]
                we = [dict(zip(columns, me)) for me in q_rst]
                return we
            return None

    def get_self(self, query, params=None):
        with self._create_conn() as conn:
            c = conn.cursor()
            if params is None:
                c.execute(query)
            else:
                c.execute(query, params)
            q_rst = c.fetchone()
            if isinstance(q_rst, tuple):
                columns = [column[0] for column in c.description]
                me = dict(zip(columns, q_rst))
                return me
            return None

    def update_self(self, query, params=None):
        with self._create_conn() as conn:
            c = conn.cursor()
            if params is None:
                c.execute(query)
            else:
                c.execute(query, params)
            conn.commit()
            q_rst = c.fetchone()
            if isinstance(q_rst, tuple):
                columns = [column[0] for column in c.description]
                me = dict(zip(columns, q_rst))
                return me
            return None



