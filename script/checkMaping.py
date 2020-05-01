#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import os
import sys
import time

from jsonschema import validate

sys.path.append('..')
from bin.loggerPro import LoggerPro, logger

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      checkMaping.py
@time:      2020/4/24 4:42 PM

@desc:      对json格式的mapping文件进行校验，判断是否缺失必要属性
'''


class ChcekMapping(object):
    def __init__(self):
        self._schema = {
            "type": "object",
            "required": ["source", "table", "database", "fieldMapping", "rule"],
            "properties": {
                "source": {"type": "string", "minLength": 1},
                "table": {"type": "string", "minLength": 1},
                "database": {"type": "string", "minLength": 1},
                "rule": {"type": "object"},
                "fieldMapping": {
                    "type": "object",
                    "required": ["uuid", "sfzh", "user_name", "email", "phoneno", "password", "explode_time",
                                 "confidence"],
                    "properties": {
                        "uuid": {"type": "string", "minLength": 1},
                        "sfzh": {"type": "string"},
                        "user_name": {"type": "string"},
                        "email": {"type": "string"},
                        "phoneno": {"type": "string"},
                        "password": {"type": "string"},
                        "explode_time": {"type": "string"},
                        "confidence": {"type": "string"}
                    }
                }
            }
        }

    def _checkJsonStr(self, jsonStr):
        """
        校验核心方法
        :param jsonStr: 待校验字符串
        :return: True False
        """
        try:
            validate(instance=jsonStr, schema=self._schema)
        except Exception as e:
            logger.error(e)
            return False
        else:
            return True

    def _checkJsonFile(self, jsonFile):
        """
        对json文件进行json字符串提取
        :param jsonFile:
        :return:
        """
        with open(jsonFile, mode="r", encoding="utf-8") as jf:
            jsonStr_ = json.load(jf)
            jf.flush()
            jf.close()
            return self._checkJsonStr(jsonStr_)

    def checkJson(self, json):
        """
        对文件或者json字符串进行模板匹配
        :param json:
        :return:
        """
        is_json = False
        if isinstance(json, str) and os.path.isfile(json):
            if self._checkJsonFile(json):
                time.sleep(1)
                logger.info(f'Json文件【{json}】验证通过！')
                is_json = True
            else:
                logger.error(f"Json文件【{json}】错误，需要对应模板格式！")
        else:
            if self._checkJsonStr(json):
                logger.info(f'Json格式数据验证通过！')
                is_json = True
            else:
                logger.error("Json格式数据错误，需要对应模板格式！请检查上送数据")
        return is_json


if __name__ == '__main__':
    LoggerPro().config()
    ck = ChcekMapping()
    ck.checkJson('../mappings/tb_ml_dbm_dbsource.json')

    succData = {
        "source": "12306",
        "database": "sgk_source",
        "table": "ssd_12306account_result",
        "fieldMapping": {
            "uuid": "uuid",
            "sfzh": "tag1",
            "user_name": "tag2",
            "email": "tag3",
            "phoneno": "tag4",
            "password": "tag5",
            "explode_time": "explode_time",
            "confidence": "confidence"
        },
        "rule": {
            "sfzh": "not_null",
            "user_name": ["not_null", "convert_empty"],
            "email": "convert_empty",
            "phoneno": "not_null",
            "confidence": "confidence"
        },
        "test": "test"
    }
    logger.info(f'succData：{ck.checkJson(succData)}')

    errData = {
        "err": "12306",
        "database": "sgk_source",
        "table": "ssd_12306account_result",
        "fieldMapping": {
            "uuid": "uuid",
            "sfzh": "tag1",
            "user_name": "tag2",
            "email": "tag3",
            "phoneno": "tag4",
            "password": "tag5",
            "explode_time": "explode_time",
            "confidence": "confidence"
        },
        "rule": {
            "tag1": "not_null",
            "tag2": "not_null",
            "tag3": "convert_empty",
            "tag4": "not_null",
            "tag5": "not_null",
            "confidence": "confidence"
        },
        "test": "test"
    }
    # logger.info(f'errData：{ck.checkJson(errData)}')
