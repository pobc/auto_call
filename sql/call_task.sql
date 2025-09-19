/*
 Navicat Premium Data Transfer

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 80400 (8.4.0)
 Source Host           : localhost:3306
 Source Schema         : xianyu

 Target Server Type    : MySQL
 Target Server Version : 80400 (8.4.0)
 File Encoding         : 65001

 Date: 05/09/2025 11:11:58
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for call_task
-- ----------------------------
DROP TABLE IF EXISTS `call_task`;
CREATE TABLE `call_task`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `area_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `insert_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `update_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `task_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `default_choose` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 24 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of call_task
-- ----------------------------
INSERT INTO `call_task` VALUES (1, 'wanke', '万科', '2024-08-29 11:14:21', '2025-03-13 15:54:07', 'stop', 'no');
INSERT INTO `call_task` VALUES (2, 'yuanyang', '远洋', '2024-09-03 23:21:25', '2025-03-24 12:56:27', 'stop', NULL);
INSERT INTO `call_task` VALUES (3, 'tanyue', '檀悦', '2024-10-31 14:53:07', '2024-11-11 16:48:50', 'stop', NULL);
INSERT INTO `call_task` VALUES (4, 'rongchuang1890', '融创1890', '2024-11-11 16:49:46', '2025-04-29 10:38:04', 'stop', NULL);
INSERT INTO `call_task` VALUES (5, 'niubingkai', '纽宾凯', '2024-11-28 12:08:35', '2024-12-09 19:05:41', 'stop', NULL);
INSERT INTO `call_task` VALUES (6, 'shilixincheng', '十里新城', '2024-11-28 12:08:57', '2024-12-29 17:06:36', 'stop', NULL);
INSERT INTO `call_task` VALUES (7, 'baolitingrui', '保利庭瑞', '2024-12-25 09:58:24', '2024-12-31 12:23:21', 'stop', NULL);
INSERT INTO `call_task` VALUES (8, 'feicui', '翡翠滨江', '2025-01-05 10:03:13', '2025-05-27 10:45:06', 'stop', NULL);
INSERT INTO `call_task` VALUES (9, 'jinditianyue', '金地天悦', '2025-06-19 17:27:56', '2025-08-19 22:10:13', 'stop', 'no');
INSERT INTO `call_task` VALUES (10, 'ttt', '测试', '2025-07-06 18:53:58', '2025-07-06 18:53:58', 'stop', 'no');
INSERT INTO `call_task` VALUES (19, 'zhongjiandagongguan', '中建大公馆', '2025-07-26 14:38:04', '2025-08-13 11:46:55', 'stop', 'no');
INSERT INTO `call_task` VALUES (20, 'jindigelindongjun', '金地格林东郡', '2025-08-11 19:25:50', '2025-08-25 14:51:49', 'stop', 'no');
INSERT INTO `call_task` VALUES (21, 'tianxiangshangfu', '天祥尚府', '2025-08-25 19:21:09', '2025-08-28 17:12:47', 'stop', 'no');
INSERT INTO `call_task` VALUES (22, 'moligongguan', '茉莉公馆', '2025-08-29 14:52:57', '2025-09-02 16:16:59', 'stop', 'ok');
INSERT INTO `call_task` VALUES (23, 'guanshanchunxiao', '关山春晓', '2025-09-02 16:04:38', '2025-09-04 20:49:44', 'stop', 'no');

SET FOREIGN_KEY_CHECKS = 1;
