#!/usr/bin/python3
# encoding=utf-8


# @Time    : 2018/10/8 下午8:06
# @Author  : 张锐志
# @TODO    : buy a house,live with a dog

# 系统库
import os

# 第三方库
import html2text
from requests_html import HTMLSession
from logbook.more import ColorizedStderrHandler
from logbook import Logger, TimedRotatingFileHandler, set_datetime_format

# 自定义库

# 禁止from xx import *
__all__ = []

# 定义logger
logger = Logger(__name__)
set_datetime_format('local')
# logger.handlers.append(TimedRotatingFileHandler(log_name, level=log_level, bubble=True, date_format='%Y-%m-%d',))
logger.handlers.append(ColorizedStderrHandler(level='DEBUG', bubble=True))


class Html(object):
    def __init__(self, url='naughtyGitCat@github.com'):
        session = HTMLSession()
        self.html = session.get(url).html

    @property
    def title(self):
        """
        获取文章标题
        :return:
        """
        html_title = self.html.find('title', first=True).text
        return html_title

    @property
    def body_md(self):
        """
        返回md格式的文章正文
        :return:字符串
        """
        body = self.html.find('body', first=True)
        md_processer = html2text.HTML2Text()
        return md_processer.handle(body.html)

    @property
    def html_text(self):
        """
        获取网页的html源码
        :return:
        """
        html_context = self.html.html
        return html_context

    @property
    def foreword(self):
        """
        获取文章的第一段作为前言
        :return: 字符串前言
        """
        foreword = self.html.find('p', first=True).text
        return foreword

    def archive_md(self, archive_dir='/tmp'):
        """
        返回
        :param archive_dir:
        :param tmp_dir:暂存文件位置(放在git wiki目录？)
        :return:暂存文件全路径
        """
        md_file = os.path.join(archive_dir, self.title)+'.md'
        md_context = self.body_md.encode('utf-8')
        with open(md_file, 'wb') as file:
            file.write(md_context)
        return md_file

    def archive_html(self, archive_dir='/tmp'):
        html_file = os.path.join(archive_dir, self.title.replace('·', '-').replace(" ", ""))+'.html'  # 删除空格和不易打出的·
        html_context = self.html_text.encode('utf-8')
        with open(html_file, 'wb') as file:
            file.write(html_context)
        return html_file


if __name__ == '__main__':
    web = Html("http://mysql.taobao.org/monthly/2018/09/02/")
    web.archive_html(archive_dir="/tmp")
