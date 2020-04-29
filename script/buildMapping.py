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


class ExploreMappingRealtion(object):
    def __init__(self, database='dbm_service', filePath='./mappings'):
        self.database = database
        self.db = con(f"mysql+pymysql://root:123456@127.0.0.1:3306/{self.database}")
        self.filePath = filePath
        self.table = ''
        self.defatMapping = {
            "uuid": "uuid",
            "身份证": "sfzh",
            "身份证号": "sfzh",
            "用户名": "user_name",
            "微信": "user_name",
            "QQ": "user_name",
            "邮箱": "email",
            "手机号": "phoneno",
            "手机号码": "phoneno",
            "密码": "password",
            "密码-加密": "password",
            "明文密码": "password"
        }

    def _buildSql(self, table_name, table_schema):
        return "SELECT d.sjly,a.table_schema,a.table_name,a.table_comment,b.column_name,b.ordinal_position,b.column_comment " \
               "FROM information_schema.TABLES a " \
               "LEFT JOIN information_schema.COLUMNS b ON a.table_schema=b.table_schema AND a.table_name=b.table_name " \
               "LEFT JOIN dangan.s_ssd_table_completed c ON a.table_name=c.table_name_after " \
               "LEFT JOIN dangan.s_analyse_data d ON d.sjpc=c.batch_id " \
               "WHERE 1=1 " \
               f"AND a.table_schema='{table_schema}' " \
               f"AND a.table_name='{table_name}' " \
               "ORDER BY a.table_schema,a.table_name,b.ordinal_position"

    def build(self):
        with open('./table.txt') as ts:
            for t in ts.readlines():
                t = t.replace('\n', '')
                if (t.strip(' ') == ''):
                    exit(-1)
                print(t)
                sql = self._buildSql(t, self.database)
                print(sql)
                lines = self.db.read(sql)
                Jm = {}
                JfieldM = {"uuid": "uuid",
                           "sfzh": "",
                           "user_name": "",
                           "email": "",
                           "phoneno": "",
                           "password": "",
                           "explode_time": "explode_time",
                           "confidence": "confidence",
                           "source": "",
                           "source_table": ""}
                Jrule = {"confidence": "confidence"}
                for l in lines:
                    if l['column_comment'] in self.defatMapping:
                        JfieldM[self.defatMapping[l['column_comment']]] = l['column_name']
                        Jrule[l['column_name']] = 'not_null'
                    Jm['source'] = l['sjly']
                    Jm['table'] = l['table_name']
                    Jm['database'] = l['table_schema']
                    JfieldM['source'] = l['sjly']
                    JfieldM['source_table'] = l['table_name']
                    self.table = l['table_name'] + '.json'
                    Jm['fieldMapping'] = JfieldM
                    Jm['rule'] = Jrule
                loads = json.dumps(Jm, ensure_ascii=False, indent=4)
                # print(loads)
                if not os.path.isdir(self.filePath):  # 无文件夹时创建
                    os.makedirs(self.filePath)
                file = os.path.join(self.filePath, self.table)
                with open(file, mode="w+", encoding="utf-8") as fd:
                    fd.write(loads)
                    fd.flush()
                    fd.close()
        ts.close()


if __name__ == '__main__':
    exp = ExploreMappingRealtion()
    exp.build()
