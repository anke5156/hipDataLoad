#!/usr/bin/python
# -*- coding: UTF-8 -*-


import sys

sys.path.append('..')
from config.configTask import ConfigTask
from bin.loggerPro import LoggerPro,logger
from bin.cmdThread import CmdThread

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      command.py
@time:      2020/4/25 4:36 PM

@desc:      execute the command which 
            configure in configTask.py
'''


class Command(object):
    def __init__(self, config=ConfigTask(), completeList=[]):
        # 配置文件
        self.cfg = config.cfg
        # 已经执行完成的命令
        self.complete = completeList
        self.index = 101

    def execute_layer_command(self, cmdsList, layerCmdsDic):
        """
        执行层命令
        :param cmdsList: 任务列表，list
        :param layerCmdsDic: 依赖任务列表，dic
        :return: 
        """
        threadList = []
        isFinalSucc = True
        for cmd in cmdsList:
            relies = layerCmdsDic[cmd]
            is_ready = True
            for rely in relies:
                if rely not in self.complete:
                    logger.warning('[****命令【%s】依赖命令【%s】，但是依赖命令没有完成****]' % (cmd, rely))
                    is_ready = False
            if not is_ready:
                logger.warning('[****暂时跳过【%s】命令! ****]' % cmd)
                continue
            logger.info('[****即将开始执行【%s】命令!****]' % cmd)

            thr = CmdThread(self.index, cmd)
            self.index = self.index + 1
            threadList.append(thr)
        for thr in threadList:
            thr.start()
        for thr in threadList:
            thr.join()
            if thr.isSuccess:
                self.complete.append(thr.cmd)
            else:
                isFinalSucc = False
        return isFinalSucc

    def execute_cmds(self):
        """
        批量执行任务，任务列表见config.py
        :return: 
        """
        cmdLayers = self.cfg.keys()
        is_success = True
        for cmdLayer in cmdLayers:
            layerCmds = self.cfg[cmdLayer]
            logger.info('[****即将开始执行第【%d】层****]' % cmdLayer)
            cmds = layerCmds.keys()
            isSucc = self.execute_layer_command(cmds, layerCmds)
            if not isSucc:
                logger.error('[****任务失败在第【%d】层 ****]' % cmdLayer)
                is_success = False
                break
        if is_success:
            logger.info('[****任务执行成功!****]')
        else:
            logger.error('[****任务执行失败!****]')
        return is_success, self.complete


if __name__ == '__main__':
    LoggerPro().config()
    cmd = Command(ConfigTask(), [])
    cmd.execute_cmds()

    cmd = Command()
    cmd.execute_layer_command(['pwd'], {"pwd": []})
