#!/usr/bin/python3
# encoding=utf-8


# @Time    : 2018/10/14 下午3:23
# @Author  : 张锐志
# @TODO    : buy a house,live with a dog

# 系统库
import os
import sys
import datetime
# 第三方库
from logbook.more import ColorizedStderrHandler
from logbook import Logger, TimedRotatingFileHandler, set_datetime_format

# 自定义库
from common.MySQL import MySQLClass
from config import MetaMisc
# 禁止from xx import *
__all__ = []

# 追加路径依赖
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 定义logger
logger = Logger(__name__)
set_datetime_format('local')
# logger.handlers.append(TimedRotatingFileHandler(log_name, level=log_level, bubble=True, date_format='%Y-%m-%d',))
logger.handlers.append(ColorizedStderrHandler(level='DEBUG', bubble=True))


def int2str(num):
    """
    将1，2，3..9补成两位字符01,02....09
    :param num:数字类型
    :return:字符串类型
    """
    if num < 10:
        str_num = '0'+str(num)
    else:
        str_num = str(num)
    return str_num


def generate_link():
    """
    生成上个月的所有文章列表地址
    :return:生成器列表
    """
    base_link = 'http://mysql.taobao.org/monthly'
    month = int2str(datetime.datetime.today().month-1)
    year = datetime.datetime.today().year
    if month == '0':
        month = 12
        year = datetime.datetime.today().year-1
    for i in range(1, 11):  # 月报每个月总共10篇，下个月一次性放出
        yield base_link + '/' + str(year) + '/' + month + '/' + int2str(i) + '/'


def register_to_db(meta_dict):
    """
    写入到元数据库中备查
    :param meta_dict:字典形式
    :return:无返回
    """
    client = MySQLClass(host=MetaMisc.host, port=MetaMisc.port,
                        user=MetaMisc.user, password=MetaMisc.pwd,
                        database=MetaMisc.db)
    client.insert_one_meta(meta_dict, MetaMisc.tb)
    logger.info("push to {}.{} success".format(MetaMisc.db, MetaMisc.tb))


if __name__ == '__main__':
    for i in generate_link():
        print(i)
