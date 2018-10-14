## 设计用途
* 定期抓取淘宝数据库月报
* 发送邮件，保存到本地，最好是git中
* 发送元数据到mysql中，后期可以做成接口集成到运维平台中，便于查询

## 使用方式
```bash
# 修改配置
vim config.py

# 安装crontab
"0 10 8 * * source ~/.bashrc && python3 ~/spider_taobao_mysql/main.py" 

# 安装依赖
pip3 install logbook
pip3 install html2text
pip3 install pymysql
pip3 install requests_html

# 创建元信息库表
mysql -d mysql -u root -p < taobao_monthly_report.sql 

# 执行程序
python3 main.py
```

## 完成情况:
* 定期抓取用crontab来做，不放到本脚本中
* 发送邮件，保存到本地(html)皆完成
* 保存元数据

## 问题
* 为什么邮件正文只有前言部分？因为邮件有反垃圾措施，全文容易被屏蔽
* 为什么收件人只有一个？因为邮件有反垃圾措施，多人容易被屏蔽，可以发送到同一个邮箱中，然后自动转发
* 可以也可以保存md格式到本地，但是我的md编辑器好像加载不了图片，就是用了html的格式本地保存
* 本地保存以及发送html时都损失了样式，不太美观，但我在邮件正文中增加了原文链接。
* 文章中的图片没有本地化，理论上是有图片失效的问题的。但考虑到各位都有阅读后及时总结整理的好习惯，也就无所谓了。

## 注意
* 一个月运行一次就够了，可以放到crontab中每月执行一次，自动抓取上个月的文章内容
* 阿里的页面是到下个月后一次性放出上个月所有的文章，总数目前看基本是10篇，
* 如果发现其一次放出了>10篇的文章，请联系我进行更改

## 依赖包
* logbook 日志
* html2text 格式转换为md
* pymysql 上传元数据
* requests_html 抓取网页的正文

## TODO:
* 缓存本地图片
* 把insert into 改成replace into
