import os
import sqlite3
import datetime

class SqliteHandler(object):
    def __init__(self, db_name:str='instance/site.sqlite'):
        self.db_name = db_name

        if not os.path.exists(self.db_name):
            self.conn = sqlite3.connect(self.db_name)
            c = self.conn.cursor()
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_name TEXT PRIMARY KEY,
                    email TEXT NOT NULL,
                    user_depot TEXT NOT NULL,
                    auth_granted BOOLEAN NOT NULL,
                    date_grant TIMESTAMP NOT NULL,
                    authed_by TEXT
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS roles (
                    role_name TEXT PRIMARY KEY,
                    role_dsc TEXT NOT NULL,
                    auth_granted BOOLEAN NOT NULL,
                    date_grant TIMESTAMP NOT NULL,
                    authed_by TEXT
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS menus (
                    menu_id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    set_grp TEXT NO NULL,
                    set_lvl INTEGER NO NULL,
                    set_order INTEGER NO NULL,
                    parent TEXT
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS user_role (
                    user_name TEXT,
                    role_name TEXT,
                    date_grant TIMESTAMP NOT NULL,
                    authed_by TEXT,
                    PRIMARY KEY (user_name, role_name),
                    FOREIGN KEY (user_name) REFERENCES users(user_name)
                    FOREIGN KEY (role_name) REFERENCES roles(role_name)
                )
                """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS role_menu (
                    role_name TEXT NOT NULL,
                    menu_id INTEGER NOT NULL,
                    date_grant TIMESTAMP NOT NULL,
                    authed_by TEXT,
                    PRIMARY KEY (role_name, menu_id),
                    FOREIGN KEY (role_name) REFERENCES roles(role_name),
                    FOREIGN KEY (menu_id) REFERENCES menus(menu_id)
                )
                """
            )
            c.executemany(
                'INSERT INTO menus VALUES (?,?,?,?,?,?,?)', 
                ([
                    (1, 'Toolbox', '/', 'top_menu', 1, 1, None),
                    (2, 'News', '/news/list', 'top_menu', 1, 2, None),
                    (3, 'Profile', '/user/profile', 'top_menu', 1, 3, None),
                    (4, 'Broken', '/broken', 'top_menu', 1, 4, None),
                    (5, 'Logout', '/logout', 'top_menu', 1, 5, None)
                ])
            )
            c.executemany(
                'INSERT INTO roles VALUES (?,?,?)',
                ([
                    ('system', 'system role', True, datetime.datetime.now(),'sys'),
                    ('certificate', 'certificate role', True, datetime.datetime.now(),'sys'),
                    ('classified', 'classified role', True, datetime.datetime.now(),'sys'),
                    ('student', 'student role', True, datetime.datetime.now(),'sys'),
                    ('guest', 'guest role', True, datetime.datetime.now(),'sys')
                ])
            )
            c.executemany(
                'INSERT INTO role_menu VALUES (?,?,?,?)',
                ([
                    ('system',1,datetime.datetime.now(),'sys'),
                    ('system',2,datetime.datetime.now(),'sys'),
                    ('system',3,datetime.datetime.now(),'sys'),
                    ('system',4,datetime.datetime.now(),'sys'),
                    ('system',5,datetime.datetime.now(),'sys'),
                    ('certificate',1,datetime.datetime.now(),'sys'),
                    ('certificate',2,datetime.datetime.now(),'sys'),
                    ('certificate',3,datetime.datetime.now(),'sys'),
                    ('certificate',5,datetime.datetime.now(),'sys'),
                    ('classified',1,datetime.datetime.now(),'sys'),
                    ('classified',2,datetime.datetime.now(),'sys'),
                    ('classified',3,datetime.datetime.now(),'sys'),
                    ('classified',5,datetime.datetime.now(),'sys'),
                    ('student',1,datetime.datetime.now(),'sys'),
                    ('student',3,datetime.datetime.now(),'sys'),
                    ('student',5,datetime.datetime.now(),'sys'),
                    ('guest',1,datetime.datetime.now(),'sys'),
                    ('guest',2,datetime.datetime.now(),'sys'),
                ])
            )
            self.conn.commit()
            self.conn.close()