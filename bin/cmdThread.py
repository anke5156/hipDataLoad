#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from threading import Thread
import subprocess
sys.path.append('..')
import bin.logger as log

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      cmdThread.py
@time:      2020/4/25 11:25 AM

@desc:      为任务创建线程
'''


class CmdThread(Thread):
    def __init__(self, id, cmd):
        Thread.__init__(self)
        self.id = id
        self.cmd = cmd
        self.isSuccess = False

    def run(self):
        isComeon = True
        if isComeon:
            status = 0
            result = '假装我就是执行结果'
            # status, result = subprocess.getstatusoutput(self.cmd)
            if status == 0:
                log.info('[****命令【%s】执行成功，退出进程!****]' % self.cmd)
                log.info('[EXCUTE_DONE]%s' % self.cmd)
                log.info('[****执行结果【%s】****]' % result)
                self.isSuccess = True
            else:
                log.error('[****命令【%s】执行失败! status=【%d】 result=【%s】进程退出!****]'
                          % (self.cmd, status, result))
                log.error('[EXCUTE_DONE]%s' % self.cmd)


if __name__ == '__main__':
    cm = CmdThread(1, "pwd", )
    cm.run()
