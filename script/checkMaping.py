#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import sys

from jsonschema import validate

sys.path.append('..')
import bin.logger as log

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      checkMaping.py
@time:      2020/4/24 4:42 PM

@desc:      对json格式的mapping文件进行校验，判断是否缺失必要属性
'''


class ChcekMapping(object):
    _schema = {
        "type": "object",
        "required": ["source", "table", "database", "fieldMapping", "rule"],
        "properties": {
            "source": {"type": "string", "minLength": 1},
            "table": {"type": "string", "minLength": 1},
            "database": {"type": "string", "minLength": 1},
            "rule": {"type": "object"},
            "fieldMapping": {
                "type": "object",
                "required": ["uuid", "sfzh", "user_name", "email", "phoneno", "password", "explode_time", "confidence"],
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

    def check(self, jsonStr):
        try:
            validate(instance=jsonStr, schema=self._schema)
        except Exception:
            log.error(f"Json文件格式错误，需要对应模板格式！请检查json文件【{jsonStr}】")
            log.error(validate.exceptions.ValidationError)
            return False
        else:
            log.info('Json文件格式验证通过！')
            return True


if __name__ == '__main__':
    ck = ChcekMapping()
    with open("../mappings/tb_ml_dbm_dbsource.json", 'r', encoding='utf-8') as f:
        # 将类文件对象中的JSON字符串直接转换成Python字典
        jsonStr_ = json.load(f)
        log.info(ck.check(jsonStr_))

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
    log.info(ck.check(succData))

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
    log.info(ck.check(errData))
