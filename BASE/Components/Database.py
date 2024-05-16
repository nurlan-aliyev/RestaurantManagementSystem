
import sqlite3
from sqlite3 import Error


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS gen_config (id INTEGER PRIMARY KEY, conf_name text);")
        self.conn.commit()

        self.insert_genconfig()

    def create_table(self, create_table_query):
        try:
            cursor = self.cur
            cursor.execute(create_table_query)
            self.conn.commit()
        except Error as e:
            print(e)

    def insert_genconfig(self):
        try:
            self.cur.execute("INSERT OR IGNORE INTO gen_config(id, conf_name) VALUES (?, ?)",
                             (1, "fac_config"))
            self.cur.execute("INSERT OR IGNORE INTO gen_config(id, conf_name) VALUES (?, ?)",
                             (2, "menu_config"))
            self.cur.execute("INSERT OR IGNORE INTO gen_config(id, conf_name) VALUES (?, ?)",
                             (3, "orders"))
            self.conn.commit()
        except Error as e:
            print(e)

    def insert_spec_config(self, insert_query, values):
        try:
            con = self.cur
            con.execute(insert_query, values)
            self.conn.commit()
        except Error as e:
            print(e)

    def update(self, update_query, values):
        try:
            con = self.cur
            con.execute(update_query, values)
            self.conn.commit()
        except Error as e:
            print(e)

    def read_val(self, read_query, table_num=''):
        try:
            con = self.cur
            if "WHERE" in read_query:
                con.execute(read_query, table_num)
                rows = con.fetchall()
            else:
                con.execute(read_query)
                rows = con.fetchall()
            return rows
        except Error as e:
            print(e)

    def delete_val(self, delete_query, item_id):
        try:
            con = self.cur
            con.execute(delete_query, item_id)
            self.conn.commit()
        except Error as e:
            print(e)

    def __del__(self):
        self.conn.close()
