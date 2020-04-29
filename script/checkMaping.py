#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import logging
import sys

from jsonschema import validate

sys.path.append('..')
from bin.propertiesUtiil import Properties

'''
@author:    anke
@contact:   anke.wang@foxmail.com
@file:      checkMaping.py
@time:      2020/4/24 4:42 PM

@desc:      对json格式的mapping文件进行校验，判断是否缺失必要属性
'''


class ChcekMapping(object):
    '''
    schema = {
        "type": "object",
        "required": ["systemId", "password", "operator", "ApplicationID", "EnviType", "Params"],
        "properties": {
            "systemId": { "type": "string", "minLength": 1},
            "password": { "type": "string"},
            "operator": { "type": "string", "minLength": 1},
            "ApplicationID": { "type": "int"},
            "EnviType": { "type": "int", "enum": [1, 2, 3]},
            "Params": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["Scope", "KeyName", "ValName"],
                    "properties": {
                        "Scope": {
                            "type": "string",
                            "pattern": "^(\w+|\*|\[[,\d]+\]){3}(\w+|\*|\[[,\d]+\])$"
                        },
                        "KeyName": {"type": "string", "minLength": 1},
                        "ValName": {"type": "string"},
                    }
                }
            },
        }
    }
    '''

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
            logging.error("Json文件格式错误，需要对应模板格式！%s" % jsonStr)
            logging.error(validate.exceptions.ValidationError)
            return False
        else:
            logging.info("Json文件格式验证通过！")
            return True


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a,%d %b %Y %H:%M:%S',
                        filename=Properties().get("logFile"),
                        filemode='a'
                        )
    ck = ChcekMapping()
    with open("../mappings/tb_ml_dbm_dbsource.json", 'r', encoding='utf-8') as f:
        # 将类文件对象中的JSON字符串直接转换成Python字典
        jsonStr_ = json.load(f)
        print(ck.check(jsonStr_))

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
    print(ck.check(succData))

    errData = {
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
        "ruless": {
            "sfzh": "not_null",
            "user_name": ["not_null", "convert_empty"],
            "email": "convert_empty",
            "phoneno": "not_null",
            "confidence": "confidence"
        },
        "test": "test"
    }
    print(ck.check(errData))
