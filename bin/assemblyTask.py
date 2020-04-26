#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      assemblyTask.py
@time:      2020/4/26 12:02 PM

@desc:      构建任务
'''
import json
import logging

from propertiesUtiil import Properties
from transforData import Mapping


class AssemblyTask(object):
    def assemb(self, fileName):
        mp = Mapping(fileName)
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
        sql20 = mp.getSql('20')
        sql01 = mp.getSql('01')
        sql02 = mp.getSql('02')
        sql03 = mp.getSql('03')
        sql04 = mp.getSql('04')
        sql05 = mp.getSql('05')
        sql06 = mp.getSql('06')
        sql07 = mp.getSql('07')
        sql08 = mp.getSql('08')
        sql09 = mp.getSql('09')
        sql10 = mp.getSql('10')
        # sql20 = ('20')
        # sql01 = ('01')
        # sql02 = ('02')
        # sql03 = ('03')
        # sql04 = ('04')
        # sql05 = ('05')
        # sql06 = ('06')
        # sql07 = ('07')
        # sql08 = ('08')
        # sql09 = ('09')
        # sql10 = ('10')

        {"20": [], "01": ["20"], "02": ["20"]}

        taskDic = dict()

        # sqls = []
        # # sqls.append(sql20)
        # sqls.append(sql01)
        # sqls.append(sql02)
        # sqls.append(sql03)
        # sqls.append(sql04)
        # sqls.append(sql05)
        # sqls.append(sql06)
        # sqls.append(sql07)
        # sqls.append(sql08)
        # sqls.append(sql09)
        # sqls.append(sql10)

        taskDic[sql20] = []
        taskDic[sql01] = [sql20]
        taskDic[sql02] = [sql20]
        taskDic[sql03] = [sql20]
        taskDic[sql04] = [sql20]
        taskDic[sql05] = [sql20]
        taskDic[sql06] = [sql20]
        taskDic[sql07] = [sql20]
        taskDic[sql08] = [sql20]
        taskDic[sql09] = [sql20]
        taskDic[sql10] = [sql20]
        jsStr = json.dumps(taskDic)
        logging.info(jsStr)
        return jsStr


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a,%d %b %Y %H:%M:%S',
                        filename=Properties('../config/config.conf').get("logFile"),
                        filemode='a'
                        )
    AssemblyTask().assemb('../mappings/tb_ml_test.json')
