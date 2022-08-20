/*
 Navicat Premium Data Transfer

 Source Server         : server-db
 Source Server Type    : MySQL
 Source Server Version : 50737 (5.7.37-log)
 Source Host           : 204.15.72.120:3306
 Source Schema         : final

 Target Server Type    : MySQL
 Target Server Version : 50737 (5.7.37-log)
 File Encoding         : 65001

 Date: 19/08/2022 23:17:59
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for log_table
-- ----------------------------
DROP TABLE IF EXISTS `log_table`;
CREATE TABLE `log_table`  (
  `logId` varchar(22) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `userId` int(11) NOT NULL,
  `level_` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `requestUrl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `code_` int(11) NOT NULL,
  `response` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `logTime` datetime NOT NULL,
  `processTime` double NOT NULL,
  PRIMARY KEY (`logId`) USING BTREE,
  INDEX `log_table_user_table_FK`(`userId`) USING BTREE,
  CONSTRAINT `log_table_user_fk` FOREIGN KEY (`userId`) REFERENCES `user_table` (`userId`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
