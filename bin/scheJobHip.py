#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import subprocess
import sys
import time

sys.path.append('..')
from bin.logSplit import splitlog
from bin.cmdThread import CmdThread
from bin.loggerPro import LoggerPro, logger

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
            logger.info('不予执行!')
        else:
            return func(**kargs)

    return wrapper


def tick():
    # 日志开始切割的标识
    mark = str(time.time())
    logger.info('%s' % mark)

    threadList = []
    cnt = 1
    for dirpath, dirnames, filenames in os.walk('../sql'):
        for filename in filenames:
            if filename.endswith('sql'):
                i = os.path.join(dirpath, filename)
                with open(i, 'r') as f:
                    logger.info('正在处理【%s】文件' % f.name)
                    thr = CmdThread(cnt, f'hive -f "{f.name}"')
                    threadList.append(thr)
    for t in threadList:
        t.start()
    for t in threadList:
        t.join()
        if t.isSuccess:
            pass
    splitlog('../logs/hipdataload.log', mark)


if __name__ == '__main__':
    LoggerPro().config(when='D', backCount=3)
    tick()
    # sched = BlockingScheduler()
    # sched.daemonic = False
    # sched.add_job(tick, trigger='cron', hour='16', minute='27')
    # sched.start()
