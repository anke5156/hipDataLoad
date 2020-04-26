#!/usr/bin/python
# -*- coding: UTF-8 -*-


from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import json
from transforData import Mapping
from command import Command
from logSplit import splitlog
from utils.propertiesUtiil import Properties

# from threadpool import Master
# from command import Command
# from config import Config
# from sqoopconfig import Sqoopconfig
# import checktask
# import logsplit
import time
import subprocess
from cmdThread import CmdThread

# import utils
# import sys
# sys.path.append("..")
# from src.predictauto import *

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      scheJobHip.py
@time:      2020/4/23 3:11 PM

@desc:      
'''


def ScheJobHip(func):
    def wrapper(*args, **kargs):
        sta, res = subprocess.getstatusoutput('ps -ef|grep scheJobHip.py')
        print(res)
        numrows = 0
        for line in res.split('\n'):
            if line.find('python scheJobHip.py') != -1:
                numrows = numrows + 1
        if numrows > 1:
            logging.info('不予执行!')
        else:
            return func(**kargs)

    return wrapper


def tick():
    # 日志开始切割的标识
    mark = str(time.time())
    logging.info('%s' % mark)

    mp = Mapping('mappings/tb_ml_test.json')
    sql1 = mp.getSql('20')

    {'ls': ['pwd'], 'whoami': []}
    sql1 = 'date'
    sql2 = 'll'
    sql3 = 'whoami'
    sql4 = 'ps -ef'

    dic1 = dict()
    dic2 = dict()

    sqls = []
    sqls.append(sql1)
    sqls.append(sql2)
    sqls.append(sql3)
    sqls.append(sql4)

    dic2[sql1] = []
    dic2[sql2] = [sql1]
    dic2[sql3] = [sql1]
    dic2[sql4] = [sql1]

    jsStr = json.dumps(dic2)
    print(dic1)
    print(dic2)
    print(jsStr)

    cmd = Command()
    strJson = json.loads(jsStr)
    cmd.execute_layer_command(sqls, strJson)

    logFile = Properties('config.perporties').get("logFile")

    splitlog(logFile, mark)
    res = True
    if res:
        pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a,%d %b %Y %H:%M:%S',
                        filename=Properties('config.perporties').get("logFile"),
                        filemode='a'
                        )
    tick()
    # sched = BlockingScheduler()
    # sched.daemonic = False
    # sched.add_job(tick, trigger='cron', hour='16', minute='27')
    # sched.start()
