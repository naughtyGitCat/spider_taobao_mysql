#! /usr/bin/python3
# encoding=utf-8

# @Time    : 2018/10/12 下午3:59
# @Author  : 张锐志
# @TODO    : buy a house,live with a dog

# 系统库
import os
import sys
import traceback
# 第三方库
from logbook.more import ColorizedStderrHandler
from logbook import Logger, TimedRotatingFileHandler, set_datetime_format

# 自定义库
from config import OtherMisc
from common.HTML import Html
from common.SendMail import MailClient
from utils import generate_link
from utils import register_to_db
# 禁止from xx import *
__all__ = []

# 追加路径依赖
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 定义logger
logger = Logger(os.path.split(__file__)[-1].split('.')[0])
set_datetime_format('local')
# logger.handlers.append(TimedRotatingFileHandler(log_name, level=log_level, bubble=True, date_format='%Y-%m-%d',))
logger.handlers.append(ColorizedStderrHandler(level='INFO', bubble=True))

meta_dict_list = []


def main():
    try:
        for link in generate_link():
            logger.info(link)
            web = Html(link)                  # 实例化网页抓取器
            article_title = web.title         # 文章标题
            html_file = web.archive_html(archive_dir=OtherMisc.archive_dir)
            mail_client = MailClient()
            mail_client.subject_body(subject=article_title, body=web.foreword+'\n'*2+link)
            mail_client.attach_file(file_type='string', target=web.body_md)
            mail_client.attach_file(file_type='file', target=html_file)
            mail_client.send_mail()           # 发送邮件

            # 构造元数据字典
            meta_dict = {'db_type': article_title.split('·')[0], 'sub_type': article_title.split('·')[1],
                         'title': article_title.split('·')[2],
                         'sequence': int(link.split('/')[-4] + link.split('/')[-3] + link.split('/')[-2]),
                         'year': int(link.split('/')[-4]), 'month': int(link.split('/')[-3]), 'link': link,
                         'foreword': web.foreword, 'archive_dir': html_file}
            meta_dict_list.append(meta_dict)
        # 写入数据库
        for meta_dict in meta_dict_list:
            register_to_db(meta_dict)
    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error(e)


if __name__ == '__main__':
    main()
