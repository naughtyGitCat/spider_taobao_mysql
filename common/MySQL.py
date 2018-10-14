#!/home/dba/python3/bin/python
# encoding=utf-8


# @Time    : 2018/10/14 下午3:05
# @Author  : 张锐志
# @TODO    : buy a house,live with a dog

# 系统库
import os
import sys
import traceback
# 第三方库
import pymysql
from pymysql import MySQLError
from logbook.more import ColorizedStderrHandler
from logbook import Logger, TimedRotatingFileHandler, set_datetime_format

# 自定义库

# 禁止from xx import *
__all__ = []

# 追加路径依赖
depend_path = os.path.abspath(os.path.join('./common'))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 定义logger
logger = Logger(__name__)
set_datetime_format('local')
# logger.handlers.append(TimedRotatingFileHandler(log_name, level=log_level, bubble=True, date_format='%Y-%m-%d',))
logger.handlers.append(ColorizedStderrHandler(level='INFO', bubble=True))


class MySQLClass(object):
    """a wrapped MySQL client"""

    def __init__(self, host=None, user=None, password=None
                 , port=None, database=None, charset='utf8'):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database
        self.cursor = None

        try:
            logger.debug('Class init begin')
            if self.database is None:
                self.client = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password,
                                              charset='utf8',cursorclass=pymysql.cursors.DictCursor)
            else:
                self.client = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password,
                                              database=self.database, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
            logger.debug('Class init sucess')
        except Exception:
            traceback.print_exc()
            logger.error('Init Connect  failed')
            raise MySQLError

    def use_db(self, database):
        """Simulate mysql client`s use database
        :parameter database"""
        self.client.select_db(database)

    def run_dql(self, sql_str):
        try:
            with self.client.cursor() as self.cursor:
                logger.debug('Now execute')
                self.cursor.execute(sql_str)
                dict_list = self.cursor.fetchall()
                return dict_list
        except Exception:
            logger.error(traceback.format_exc())
            logger.error("Get Data failed")

    def run_dml(self, sql_str):
        """
        run i,u,d sql,with transaction
        :param sql_str:
        """
        try:
            # p.debug('Now in run_dml first try')
            with self.client.cursor() as self.cursor:
                logger.debug('Now execute')
                self.cursor.execute(sql_str)
                self.client.commit()
                logger.debug('Execute oK')
        except MySQLError:
            traceback.print_exc()
            self.client.rollback()

    def insert_one_meta(self, meta_dict, table='mongodb_bak_meta'):
        """
        insert one dict into mysql table
        :param meta_dict:
        :param table:
        :return:
        """
        sql_columns = ''
        sql_values = ''
        prepare_sql_str = """insert into {}({}) values {}"""
        prepare_placeholder = ','.join('{}' * len(meta_dict))
        for key in meta_dict.keys():
            value = meta_dict[key]
            sql_columns = sql_columns + key + ','
            # 对列值进行判断，isdigit()是str类型的属性，判断时可以使用repr()加上""进行欺骗
            if repr(value).isdigit():
                # 如果纯数字类型的值，直接连接
                sql_values = sql_values + str(value) + ','
            else:
                # 如果不是纯数字类型的，需要加上""，不然无法插入
                sql_values = sql_values + repr(value) + ','
        sql_str = 'insert into {}({}) values ({})'.format(table, sql_columns[0:-1], sql_values[0:-1])
        logger.debug(sql_str)
        logger.debug('go to rundml')
        self.run_dml(sql_str=sql_str)




if __name__ == '__main__':
    pass
