#!/usr/bin/python
# -*- coding: UTF-8 -*-

from threading import Thread
import subprocess
import logging

from propertiesUtiil import Properties

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
                logging.info('[****命令【%s】执行成功，退出进程!****]' % self.cmd)
                logging.info('[EXCUTE_DONE]%s' % self.cmd)
                logging.info('[****执行结果【%s】****]' % result)
                self.isSuccess = True
            else:
                logging.error('[****命令【%s】执行失败! status=【%d】 result=【%s】进程退出!****]'
                              % (self.cmd, status, result))
                logging.error('[EXCUTE_DONE]%s' % self.cmd)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a,%d %b %Y %H:%M:%S',
                        filename=Properties().get("logFile"),
                        filemode='a'
                        )
    cm = CmdThread(1, "pwd", )
    cm.run()
