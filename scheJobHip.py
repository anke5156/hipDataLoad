#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from transforData import Mapping
from command import Command
from logSplit import splitlog
from utils.propertiesUtiil import Properties
from assemblyTask import AssemblyTask as ak
import logging
import time
import subprocess
import json

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

    for dirpath, dirnames, filenames in os.walk('mappings'):
        for filename in filenames:
            if filename.endswith('json'):
                i = os.path.join(dirpath, filename)
                with open(i, 'r') as f:
                    logging.info('正在处理【%s】文件' % f.name)

                    aks = ak().assemb(f.name)
                    strJson = json.loads(aks)

                    cmd = Command()
                    cmd.execute_layer_command(strJson, strJson)

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
