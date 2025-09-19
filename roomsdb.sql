/*
 Navicat Premium Dump SQL

 Source Server         : 127.0.0.1
 Source Server Type    : MariaDB
 Source Server Version : 50525 (5.5.25-MariaDB)
 Source Host           : 127.0.0.1:3306
 Source Schema         : roomsdb

 Target Server Type    : MariaDB
 Target Server Version : 50525 (5.5.25-MariaDB)
 File Encoding         : 65001

 Date: 12/07/2025 11:04:21
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for room_meters
-- ----------------------------
DROP TABLE IF EXISTS `room_meters`;
CREATE TABLE `room_meters`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `room_id` int(11) NOT NULL,
  `electricity_unit` int(11) NOT NULL,
  `water_unit` int(11) NOT NULL,
  `recorded_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `room_id`(`room_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 24 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Fixed;

-- ----------------------------
-- Records of room_meters
-- ----------------------------
INSERT INTO `room_meters` VALUES (1, 3, 0, 0, '2025-07-12 08:47:43');
INSERT INTO `room_meters` VALUES (2, 3, 5, 5, '2025-07-12 08:47:52');
INSERT INTO `room_meters` VALUES (3, 4, 1, 3, '2025-07-12 08:48:40');
INSERT INTO `room_meters` VALUES (4, 3, 9, 30, '2025-07-12 09:06:15');
INSERT INTO `room_meters` VALUES (5, 4, 11, 3, '2025-07-12 09:07:11');
INSERT INTO `room_meters` VALUES (6, 3, 4, 2, '2025-07-12 09:11:50');
INSERT INTO `room_meters` VALUES (7, 3, 5, 3, '2025-07-12 09:16:05');
INSERT INTO `room_meters` VALUES (8, 4, 50, 30, '2025-07-12 09:20:22');
INSERT INTO `room_meters` VALUES (9, 4, 70, 80, '2025-07-12 09:24:10');
INSERT INTO `room_meters` VALUES (10, 5, 5, 5, '2025-07-12 09:50:03');
INSERT INTO `room_meters` VALUES (11, 6, 1, 1, '2025-07-12 09:50:14');
INSERT INTO `room_meters` VALUES (12, 6, 7, 5, '2025-07-12 09:50:32');
INSERT INTO `room_meters` VALUES (13, 6, 70, 50, '2025-07-12 09:52:10');
INSERT INTO `room_meters` VALUES (14, 5, 60, 40, '2025-07-12 09:52:19');
INSERT INTO `room_meters` VALUES (15, 7, 50, 40, '2025-07-12 09:53:28');
INSERT INTO `room_meters` VALUES (16, 7, 70, 60, '2025-07-12 09:53:58');
INSERT INTO `room_meters` VALUES (17, 7, 112, 89, '2025-07-12 09:57:53');
INSERT INTO `room_meters` VALUES (18, 7, 175, 99, '2025-07-01 00:00:00');
INSERT INTO `room_meters` VALUES (19, 7, 180, 99, '2025-07-01 00:00:00');
INSERT INTO `room_meters` VALUES (20, 7, 150, 150, '2025-08-01 00:00:00');
INSERT INTO `room_meters` VALUES (21, 7, 1, 1, '2025-06-01 00:00:00');
INSERT INTO `room_meters` VALUES (22, 8, 1, 1, '2025-06-01 00:00:00');
INSERT INTO `room_meters` VALUES (23, 8, 7, 8, '2025-07-01 00:00:00');

-- ----------------------------
-- Table structure for rooms
-- ----------------------------
DROP TABLE IF EXISTS `rooms`;
CREATE TABLE `rooms`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `tenant_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `room_price` decimal(10, 2) NULL DEFAULT 0.00,
  `water_rate` decimal(10, 2) NULL DEFAULT 0.00,
  `electricity_rate` decimal(10, 2) NULL DEFAULT 0.00,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of rooms
-- ----------------------------
INSERT INTO `rooms` VALUES (8, 'S002', 'มีผู้เช่า', 'test2', 3000.00, 7.00, 7.00);
INSERT INTO `rooms` VALUES (7, 'S001', 'มีผู้เช่า', 'test', 3000.00, 7.00, 7.00);

-- ----------------------------
-- Table structure for settings
-- ----------------------------
DROP TABLE IF EXISTS `settings`;
CREATE TABLE `settings`  (
  `id` int(11) NOT NULL,
  `site_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `welcome_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `default_rooms` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of settings
-- ----------------------------
INSERT INTO `settings` VALUES (1, 'หอพักศรีรุ้ง', 'ยินดีต้อนรับเข้าสู่ระบบจัดการห้องพัก', '');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'admin', '1234');

SET FOREIGN_KEY_CHECKS = 1;
