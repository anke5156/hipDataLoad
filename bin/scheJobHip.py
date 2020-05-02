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
from script.exploreMappingRealtion import ExploreMappingRealtion
from script.exploreSql import ExploteSql

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
            if line.find('Python scheJobHip.py') != -1:
                numrows = numrows + 1
        if numrows > 1:
            logger.info('当前程序正在运行，不予执行!')
        else:
            return func(**kargs)

    return wrapper


@ScheJobHip
def tick():
    mark = str(time.time())
    logger.info('%s' % mark)

    # 1.先建mapping
    expMapping = ExploreMappingRealtion('dbm_service')
    expMapping.build('../script/table.txt')

    # 2.根据mapping构建sql
    for dirPath, dirNames, fileNames in os.walk('../mappings'):
        for fileName in fileNames:
            if fileName.endswith('json'):
                i = os.path.join(dirPath, fileName)
                with open(i, 'r') as f:
                    c = ExploteSql(f.name)
                    logger.info(f'正在处理【{f.name}】文件')
                    if not os.path.isdir('../sql'):  # 无文件夹时创建
                        os.makedirs('../sql')
                    file = os.path.join('../sql', c.table + '.sql')
                    lis = ['20', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10']

                    with open(file, mode="w+", encoding="utf-8") as fd:
                        for i in lis:
                            fd.write(c.getSql(i))
                            fd.write('\n\n')
                        fd.flush()
                        fd.close()

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
