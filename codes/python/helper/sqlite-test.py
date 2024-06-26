#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

con = None

try:
    con = lite.connect('test.db')
    cur = con.cursor()
    cur.execute('SELECT SQLITE_VERSION()')
    data = cur.fetchone()
    print("SQLite version: {0}".format(data))
except (lite.Error, e):
    print("Error {0}:".format(e.args[0]))
    sys.exit(1)
finally:
    if con:
        con.close()
