'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017/5/9
# @Author  : foodish
# @File    : mysqlite3.py
'''
import sqlite3

conn = sqlite3.connect('xq_init.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS User
            (id INT PRIMARY KEY, uid INT UNIQUE ,screen_name TEXT, gender TEXT, province TEXT, city TEXT, 
            verified TEXT, verified_type TEXT, cube_count INTEGER, stocks_count INTEGER, friends_count INTEGER, 
            followers_count INTEGER, status_count INTEGER, last_status_id INTEGER, is_visited INTEGER)''')
#主键类型为int时其为自增加类型
# cur.execute('''CREATE TABLE IF NOT EXISTS Follows
#             (from_id INTEGER, to_id INTEGER, UNIQUE(from_id, to_id))''')
# CREATE TABLE user(
#    id INTEGER  PRIMARY KEY,
#    screen_name　TEXT,
#    gender TEXT,
#    province TEXT,
#    city　TEXT,
#    verified　BOOL,
#    verified_type TEXT,
#    cube_count INTEGER,
#    stocks_count INTEGER,
#    followers_count INTEGER,
#    friends_count INTEGER,
#    status_count INTEGER,
#    last_status_id INTEGER,
#    is_visited INTEGER
# );
# [(1, 1955602780, '不明真相的群众', 'm', '北京', 13229, 201403, 1)]
cur.close()