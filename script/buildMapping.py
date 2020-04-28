#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pydbclib import connect as con
import os
import json

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      buildMapping.py
@time:      2020/4/28 11:12 下午

@desc:      构建json映射工具
'''

defatMapping = {
    "uuid": "uuid",
    "身份证号": "sfzh",
    "身份证号码": "sfzh",
    "用户名": "user_name",
    "邮箱": "email",
    "手机号": "phoneno",
    "密码": "password",
    "密码-密文": "password",
    "明文密码": "password"
}

db = con("mysql+pymysql://***:***@127.0.0.1:3306/dbm_service")
sql = "SELECT a.table_schema,a.table_name,a.table_comment,b.column_name,b.ordinal_position,b.column_comment " \
      "FROM information_schema.TABLES a " \
      "LEFT JOIN information_schema.COLUMNS b ON a.table_schema=b.table_schema AND a.table_name=b.table_name " \
      "WHERE 1=1 " \
      "AND a.table_schema='dbm_service' " \
      "AND a.table_name='tb_ml_dbm_users' " \
      "ORDER BY a.table_schema,a.table_name,b.ordinal_position"
lines = db.read(sql)

Jm = {}
JfieldM = {"uuid": "uuid",
           "sfzh": "",
           "user_name": "",
           "email": "",
           "phoneno": "",
           "password": "",
           "explode_time": "",
           "confidence": "confidence",
           "source": "",
           "source_table": ""}
Jrule = {"confidence": "confidence"}
for l in lines:
    if l['column_comment'] in defatMapping:
        print(l['column_comment'])
        JfieldM[defatMapping[l['column_comment']]] = l['column_name']
        Jrule[l['column_name']] = 'not_null'
    Jm['source'] = l['table_schema']
    Jm['table'] = l['table_name']
    Jm['database'] = l['table_schema']
    Jm['fieldMapping'] = JfieldM
    Jm['rule'] = Jrule
loads = json.dumps(Jm)
print(loads)
