#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      assemblyTask.py
@time:      2020/4/26 12:02 PM

@desc:      构建任务
'''
import bin.logger as log
import json
import sys

sys.path.append('..')
from script.exploreSql import ExploteSql


class AssemblyTask(object):
    def assemb(self, fileName):
        mp = ExploteSql(fileName)
        """
        按照依赖关系，需要先构建宽表，再构建关系表
宽表: 20,
关系表: 
01:身份证手机号关系；
02: 身份证邮箱关系；
03: 身份证用户名关系；
04: 身份证密码关系；
05: 手机号用户名关系；
06: 手机号邮箱关系；
07: 手机号密码关系；
08: 邮箱用户名关系；
09: 邮箱密码关系；
10: 用户名密码关系
"""
        sql20 = f"hive -e \"{mp.getSql('20')}\""
        sql01 = f"hive -e \"{mp.getSql('01')}\""
        sql02 = f"hive -e \"{mp.getSql('02')}\""
        sql03 = f"hive -e \"{mp.getSql('03')}\""
        sql04 = f"hive -e \"{mp.getSql('04')}\""
        sql05 = f"hive -e \"{mp.getSql('05')}\""
        sql06 = f"hive -e \"{mp.getSql('06')}\""
        sql07 = f"hive -e \"{mp.getSql('07')}\""
        sql08 = f"hive -e \"{mp.getSql('08')}\""
        sql09 = f"hive -e \"{mp.getSql('09')}\""
        sql10 = f"hive -e \"{mp.getSql('10')}\""

        taskDic = dict()
        taskDic[sql20] = []
        # taskDic[sql01] = [sql20]
        # taskDic[sql02] = [sql20]
        # taskDic[sql03] = [sql20]
        # taskDic[sql04] = [sql20]
        # taskDic[sql05] = [sql20]
        # taskDic[sql06] = [sql20]
        # taskDic[sql07] = [sql20]
        # taskDic[sql08] = [sql20]
        # taskDic[sql09] = [sql20]
        # taskDic[sql10] = [sql20]
        jsStr = json.dumps(taskDic)
        log.info(jsStr)
        return jsStr


if __name__ == '__main__':
    AssemblyTask().assemb('../mappings/tb_ml_dbm_users.json')
