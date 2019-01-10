/*
Navicat MySQL Data Transfer

Source Server         : 云服务器
Source Server Version : 50724
Source Host           : 121.196.214.60:3306
Source Database       : article_spider

Target Server Type    : MYSQL
Target Server Version : 50724
File Encoding         : 65001

Date: 2019-01-10 09:31:23
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for jobbole_article
-- ----------------------------
DROP TABLE IF EXISTS `jobbole_article`;
CREATE TABLE `jobbole_article` (
  `title` varchar(200) NOT NULL,
  `create_date` date DEFAULT NULL,
  `url` varchar(300) NOT NULL,
  `url_object_id` varchar(50) NOT NULL,
  `front_image_url` varchar(300) NOT NULL,
  `front_image_path` varchar(200) DEFAULT NULL,
  `comment_nums` int(11) NOT NULL DEFAULT '0',
  `fav_nums` int(11) NOT NULL DEFAULT '0',
  `praise_nums` int(11) NOT NULL DEFAULT '0',
  `tags` varchar(200) DEFAULT NULL,
  `content` longtext NOT NULL,
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
