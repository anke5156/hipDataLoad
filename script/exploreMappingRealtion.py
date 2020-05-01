#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys

from pydbclib import connect as con
import os
import json

sys.path.append('..')
from bin.loggerPro import LoggerPro, logger

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      exploreMappingRealtion.py
@time:      2020/4/28 11:12 下午

@desc:      构建json映射工具
'''


class ExploreMappingRealtion(object):
    def __init__(self, database, outPutPath='../mappings'):
        self.database = database
        # self.db = con(f"mysql+pymysql://root:123456@172.20.1.11:3306/{self.database}")
        self.db = con(f"mysql+pymysql://root:123456@127.0.0.1:3306/{self.database}")
        self.filePath = outPutPath
        self.table = ''
        self.fieldTransMapping = {
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
        self.sourceTransMapping = {"12306": "12306",
                                   "126": "126",
                                   "163": "163",
                                   "7k7k": "7k7k",
                                   "acfun": "acfun",
                                   "csdn": "csdn",
                                   "renren": "renren",
                                   "tianya": "tianya",
                                   "xiaomi": "xiaomi",
                                   "珍爱网": "zhenaiwang",
                                   "52房地产": "52fangdichan",
                                   "92hacker": "92hacker",
                                   "118faka": "118faka",
                                   "open": "open",
                                   "zp": "zp",
                                   "曹长青": "caochangqing",
                                   "汉庭": "hanting",
                                   "鲸鱼": "jingyu",
                                   "缅华": "mianhua",
                                   "台湾海外网": "taiwanhaiwaiwang",
                                   "一亿": "yiyi",
                                   "web": "web"}

    def _buildSql(self, table, database):
        sql = f'''
        SELECT d.sjly,a.table_schema,a.table_name,a.table_comment,b.column_name,b.ordinal_position,b.column_comment
        FROM information_schema.TABLES a
        LEFT JOIN information_schema.COLUMNS b ON a.table_schema=b.table_schema AND a.table_name=b.table_name
        LEFT JOIN dangan.s_ssd_table_completed c ON a.table_name=c.table_name_after
        LEFT JOIN dangan.s_analyse_data d ON d.sjpc=c.batch_id
        WHERE 1=1
        AND d.sjly is not null
        AND a.table_schema='{database}'
        AND a.table_name='{table}'
        ORDER BY a.table_schema,a.table_name,b.ordinal_position
        '''
        # sql = f"select * from dangan.t_ml_tempdddddddd where 1=1 and table_name='{table}'"
        return sql

    def build(self, tableFile):
        with open(tableFile) as ts:
            for t in ts.readlines():
                t = t.replace('\n', '')
                if (t.strip(' ') == ''):
                    exit(-1)
                elif t.startswith('#'):
                    continue
                sql = self._buildSql(t, self.database)
                lines = self.db.read(sql)
                jBase = {}
                jField = {"uuid": "uuid",
                          "sfzh": "",
                          "user_name": "",
                          "email": "",
                          "phoneno": "",
                          "password": "",
                          "explode_time": "explode_time",
                          "confidence": "confidence",
                          "source_table": "",
                          "source": ""}
                jRule = {"confidence": "confidence"}

                for l in lines:
                    if l['column_comment'] in self.fieldTransMapping:
                        jField[self.fieldTransMapping[l['column_comment']]] = l['column_name']
                        jRule[l['column_name']] = 'not_null'

                    if l['sjly'] in self.sourceTransMapping:
                        l['sjly'] = self.sourceTransMapping[l['sjly']]
                    jField['source'] = l['sjly']
                    jField['source_table'] = l['table_name']

                    self.table = l['table_name'] + '.json'

                    jBase['source'] = l['sjly']
                    jBase['table'] = l['table_name']
                    jBase['database'] = l['table_schema']
                    jBase['fieldMapping'] = jField
                    jBase['rule'] = jRule
                if not bool(jBase):
                    logger.warning(f'【{t}】表没有找到需要构建的mapping，请检查table.txt文件和数据库')
                    continue
                logger.info(jBase['database'] + '.' + jBase['table'])
                loads = json.dumps(jBase, ensure_ascii=False, indent=4)
                if not os.path.isdir(self.filePath):
                    os.makedirs(self.filePath)
                file = os.path.join(self.filePath, self.table)
                with open(file, mode="w+", encoding="utf-8") as fd:
                    fd.write(loads)
                    fd.flush()
                    fd.close()
        ts.close()


if __name__ == '__main__':
    LoggerPro().config()

    exp = ExploreMappingRealtion('dbm_service')
    exp.build('./table.txt')
