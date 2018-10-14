/*

 Source Server Type    : MySQL
 Source Schema         : library
 Target Server Type    : MySQL
 File Encoding         : 65001

 Date: 14/10/2018 19:59:43
*/

create database library;

USE library;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for taobao_monthly_report
-- ----------------------------
DROP TABLE IF EXISTS `taobao_monthly_report`;
CREATE TABLE `taobao_monthly_report` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `db_type` varchar(255) DEFAULT NULL COMMENT '数据库类型',
  `sub_type` varchar(255) DEFAULT NULL COMMENT '次级分类',
  `title` varchar(255) DEFAULT NULL COMMENT '文章标题',
  `sequence` int(11) DEFAULT NULL COMMENT '文章序号',
  `year` int(11) DEFAULT NULL COMMENT '年份',
  `month` int(11) DEFAULT NULL COMMENT '月份',
  `link` varchar(255) DEFAULT NULL COMMENT '标题',
  `foreword` text COMMENT '前言',
  `archive_dir` varchar(500) DEFAULT NULL COMMENT '存放位置',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
