#!/usr/bin/env python
# coding: utf-8

# EXPERIMENTAL

# https://pypi.python.org/pypi/mysql-connector-python
#now mariadb.org download and copy to /usr/lib/python2.7/site-packages/mysql/
import mysql 
from mysql import connector

class Request:
    def mysql():
        # https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
        config = {
          'user': 'asolar_entropy',
          'password': '',
          'host': 'johnny.heliohost.org', # make sure remote host are allowed
          'database': 'asolar_entropy',
          'port': 3306 # default is 3306
        }

        db = mysql.connector.connect(**config)

        # you must create a Cursor object. It will let
        #  you execute all the queries you need
        cur = db.cursor()

        # Use all the SQL you like
        cur.execute("SELECT * FROM proximity")

        # print all the first cell of all the rows
        for row in cur.fetchall() :
            print row[0]

r = Request()
r.mysql
