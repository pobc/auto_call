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

 Date: 05/09/2025 11:11:47
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for speech_word
-- ----------------------------
DROP TABLE IF EXISTS `speech_word`;
CREATE TABLE `speech_word`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT ' ',
  `txt` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `txt_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `ok_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `no_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `hesitate_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `insert_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `update_datetime` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `community_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `keys` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 58 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of speech_word
-- ----------------------------
INSERT INTO `speech_word` VALUES (-1, '您好，我这边是海居租房中介的，您万科的房子是自己住还是出租呢？', 'wanke_q1', 'q2', 'q2', 'q6', '2024-07-22 15:58:34', '2024-07-22 15:58:34', '万科', NULL);
INSERT INTO `speech_word` VALUES (1, '您好，我这边是海居租房中介的，您远洋的房子是自己住还是出租呢？', 'yuanyang_q1', 'q2', 'q2', 'q6', '2024-07-22 15:58:34', '2024-07-22 15:58:34', '远洋东方境', NULL);
INSERT INTO `speech_word` VALUES (2, '好的，我记录一下，那您还有没有其他房子要出租呢？', 'q2', 'q5', 'q12', 'q12', '2024-07-22 15:58:34', '2024-07-22 15:58:34', NULL, NULL);
INSERT INTO `speech_word` VALUES (3, '好的，稍后 我们的租房专员联系您，为您登记房子信息，祝您生活愉快，再见', 'q5', 'q8', 'q9', 'q12', '2024-07-22 15:58:34', '2024-07-22 15:58:34', NULL, NULL);
INSERT INTO `speech_word` VALUES (4, '最近要租万科翡翠滨江房子的客户蛮多的，居家、情侣、办公的都有，我稍后加您微信，如果您打算出租的话，随时给我发信息，可以吗？', 'q6', 'q5', 'q12', 'q12', '2024-07-22 15:58:34', '2024-07-22 15:58:34', NULL, NULL);
INSERT INTO `speech_word` VALUES (5, '好的，打扰您了,祝您生活愉快，再见！', 'q7', NULL, NULL, NULL, '2024-07-22 15:58:34', '2024-07-22 15:58:34', NULL, NULL);
INSERT INTO `speech_word` VALUES (6, '您当前手机号可以加到您的微信吗？我稍后加您微信，你把房子里面的照片发我一下，如果没有照片的话，我安排时间过去拍', 'q8', 'q12', 'q9', 'q12', '2024-07-22 15:58:34', '2024-07-22 15:58:34', NULL, NULL);
INSERT INTO `speech_word` VALUES (7, '稍后我把我的联系方式用短信的方式发送给您，您加我，我这边就先不打扰您了，祝您生活愉快，再见！', 'q9', NULL, NULL, NULL, '2024-07-22 15:58:34', '2024-07-22 15:58:34', NULL, NULL);
INSERT INTO `speech_word` VALUES (9, '好的，您贵姓啊', 'q11', 'q12', 'q12', 'q12', '2024-07-22 15:58:34', '2024-07-22 15:58:34', NULL, NULL);
INSERT INTO `speech_word` VALUES (10, '好嘞，那我这边就先不打扰您了，祝您生活愉快，再见！', 'q12', NULL, NULL, NULL, '2024-07-22 15:58:34', '2024-07-22 15:58:34', NULL, NULL);
INSERT INTO `speech_word` VALUES (11, '好嘞，这边先不打扰您了，再见！', 'w1', 'q12', 'q12', 'q12', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '电话助理,语音留言,语音超时,录制留言,智能助理,现在不方便接听电话,正在忙线中,呼叫保持');
INSERT INTO `speech_word` VALUES (12, '骚扰', 'w2', 'q12', 'q12', 'q12', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, NULL);
INSERT INTO `speech_word` VALUES (13, '骂人', 'w3', 'q12', 'q12', 'q12', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, NULL);
INSERT INTO `speech_word` VALUES (16, '好的', 'w9', NULL, NULL, NULL, '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, NULL);
INSERT INTO `speech_word` VALUES (17, '我们在全武汉有一百多家门店，您想去线下了解的话，在地图上搜海居租房，大海的海，居住的居，任何门店都会热情接待您', 'w10', 'q2', 'q2', 'q2', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '怎么过去');
INSERT INTO `speech_word` VALUES (18, '只需要您告知门牌号，发送房子里面的照片给我就行，在没有帮您把房子租出去之前，不涉及任何费用，稍后我把公司的营业执照、我的工牌照片发给您看一下', 'w11', 'q2', 'q2', 'q2', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '骗人的');
INSERT INTO `speech_word` VALUES (19, '我们是在房管局注册的租赁公司，受房管局监管的，网上可以查到，而且我们公司在武汉经营十几年，有100多家门店，业务员近5000人，租房效率特别高', 'w18', 'q2', 'q2', 'q2', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '优势');
INSERT INTO `speech_word` VALUES (20, '我们是电脑随机拨号码段的，看您有没有房屋出租', 'w19', 'q5', 'q12', 'q12', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '号码是哪里来的');
INSERT INTO `speech_word` VALUES (21, '那行，那我先加你微信，如果有需要的话，随时联系我，那我这边先不打扰您了，祝您生活愉快，再见！', 'w21', NULL, NULL, NULL, '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '有空再说');
INSERT INTO `speech_word` VALUES (23, '现在都不用交', 'w26', 'q2', 'q2', 'q2', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '交不交税');
INSERT INTO `speech_word` VALUES (24, '那等您方便的时候我们再联系，祝您生活愉快，再见！', 'w27', NULL, NULL, NULL, '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '客户忙');
INSERT INTO `speech_word` VALUES (25, '您好，暂时无法回答您的问题，随后我会找一个专业的顾问帮你解答。', 'w28', 'q12', 'q12', 'q12', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, 'AI连续3次无法回答的最终处理');
INSERT INTO `speech_word` VALUES (26, '哦，那您小心开车，我就不打扰您了，祝您生活愉快，再见！', 'w29', 'w1', 'w1', 'w1', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '开车');
INSERT INTO `speech_word` VALUES (28, '抱歉，暂时没听清您的问题。您刚刚说什么来着?', 'w31', 'q5', 'q12', 'q12', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '无法应答处理');
INSERT INTO `speech_word` VALUES (29, '我这边可能信号不太好，您能再说一遍吗？', 'w32', 'q5', 'q12', 'q12', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '无法应答处理');
INSERT INTO `speech_word` VALUES (30, '不好意思，我这边听得不是很清楚，您可以再说一遍吗？', 'w33', 'q5', 'q12', 'q12', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '无法应答处理');
INSERT INTO `speech_word` VALUES (31, '我们是免费带看的，成功帮您出租后 ，收取首月租金的一半作为佣金，如果客户只租半年的话，我们的佣金再减一半', 'w34', 'q5', 'q12', 'q12', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '有没有优惠');
INSERT INTO `speech_word` VALUES (32, '非常抱歉呢，跟工作不相关的问题上班时间我们是不允许聊的，咱们还是回归到租赁上来吧', 'w36', 'q2', 'q12', 'q12', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '调戏AI');
INSERT INTO `speech_word` VALUES (33, '一般是押一付三', 'w37', 'q5', 'q12', 'q12', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '付款方式');
INSERT INTO `speech_word` VALUES (34, '我是海居租房的客服，您叫我小蒋就好了', 'w40', 'q5', 'q5', 'q5', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '怎么称呼');
INSERT INTO `speech_word` VALUES (35, '小区不同的户型、不同的装修，价格差异还挺大的，我稍后加您微信，把其他业主的报价截图发您参考一下', 'w44', 'q2', 'q2', 'q12', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '多少,价格,行情,租金');
INSERT INTO `speech_word` VALUES (36, '喂。在吗', 'w45', 'q2', 'q12', 'q6', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '用户不回答');
INSERT INTO `speech_word` VALUES (37, '喂，您能听到我的说话吗？', 'w46', 'q8', 'q2', 'q6', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '用户不回答');
INSERT INTO `speech_word` VALUES (38, '喂，在吗？我这边听不见您的声音，先挂了，再见。', 'w47', 'q2', 'q12', 'q6', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '用户不回答');
INSERT INTO `speech_word` VALUES (39, '这不重要啦，主要是我们有大量客户要租房，想看您介不介意中介带客看房', 'w52', 'q2', 'q12', 'q12', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '机器人');
INSERT INTO `speech_word` VALUES (40, '不好意思，您问的问题我不太了解，我记下来了，稍后我让我们资深客户经理给您回个电话详细介绍一下，我这边就不打扰您了，再见', 'w53', NULL, NULL, NULL, '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '答非所问');
INSERT INTO `speech_word` VALUES (41, '您在地图上搜一下海居租房，大海的海，居住的居，武汉到处都有我们的门店', 'w56', 'q2', 'q12', 'q12', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '公司位置');
INSERT INTO `speech_word` VALUES (42, '好的，我稍后在微信里面搜索您当前手机号加您，如果搜不到的话，我就将我的微信以短信的形式发给您', 'w57', 'q12', 'q12', 'q12', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '加微信');
INSERT INTO `speech_word` VALUES (43, '您好，我这边是海居租房中介的，您远洋的房子是自己还是出租呢？', 'tanyue_q1', 'q2', 'q2', 'q6', '2024-07-22 15:58:34', '2024-07-22 15:58:34', '阳光城檀悦', NULL);
INSERT INTO `speech_word` VALUES (44, '您好，我这边是海居租房中介的，您融创的房子是自己还是出租呢？', 'rongchuang1890_q1', 'q2', 'q2', 'q6', '2024-07-22 15:58:34', '2024-07-22 15:58:34', '融创', NULL);
INSERT INTO `speech_word` VALUES (45, '我们公司是海居租房，专业做租房的中介', 'w30', 'q2', 'q12', 'q16', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '房产公司');
INSERT INTO `speech_word` VALUES (46, '我们公司叫海居租房，大海的海，居住的居，专门做房屋租赁的中介公司  ', 'w24', 'q2', 'q2', 'q2', '2024-07-22 16:03:50', '2024-07-22 16:03:50', NULL, '公司名称,公司,什么,哪里,哪个中介,哪位');
INSERT INTO `speech_word` VALUES (47, '您好，我这边是海居租房中介的，您纽宾凯的房子是自己还是出租呢？', 'niubingkai_q1', 'q2', 'q2', 'q6', '2024-07-22 15:58:34', '2024-07-22 15:58:34', '纽宾凯', NULL);
INSERT INTO `speech_word` VALUES (48, '老板，我是海居租房中介的，您十里新城的房子是自己住还是出租呢？', 'shilixincheng_q1', 'q2', 'q2', 'q6', '2024-07-22 15:58:34', '2024-07-22 15:58:34', '十里新城', NULL);
INSERT INTO `speech_word` VALUES (49, '什么时候到期呢？', 'w58', 'q2', 'q2', 'q2', '2024-12-13 15:38:47', '2024-12-13 15:38:47', NULL, '已经租了,已经出租,已经租,租出去了');
INSERT INTO `speech_word` VALUES (50, '老板，我是海居租房中介的，您保利庭瑞的房子是自己住还是出租呢？', 'baolitingrui_q1', 'q2', 'q2', 'q6', '2024-07-22 15:58:34', '2024-07-22 15:58:34', '保利庭瑞', NULL);
INSERT INTO `speech_word` VALUES (51, '老板，我是海居租房中介的，您翡翠滨江的房子是自己住还是出租呢？', 'feicui_q1', 'q2', 'q2', 'q6', '2024-07-22 15:58:34', '2024-07-22 15:58:34', '翡翠滨江三期', '听清楚');
INSERT INTO `speech_word` VALUES (52, '老板，我是海居租房中介的，您金地天悦的房子是自己住还是出租呢？', 'jinditianyue_q1', 'q2', 'q2', 'q6', '2024-07-22 15:58:34', '2024-07-22 15:58:34', '金地天悦', '听清楚');
INSERT INTO `speech_word` VALUES (53, '老板，我是海居租房中介的，您中建大公馆有没有房子要出租呢？', 'zhongjiandagongguan_q1', 'q2', 'q2', 'q6', '2024-07-22 15:58:34', '2024-07-22 15:58:34', '中建大公馆', '听清楚');
INSERT INTO `speech_word` VALUES (54, '老板，我是海居租房中介的，您金地格林东郡有没有房子要出租呢？', 'jindigelindongjun_q1', 'q2', 'q2', 'q6', '2024-07-22 15:58:34', '2024-07-22 15:58:34', '金地格林东郡', '听清楚');
INSERT INTO `speech_word` VALUES (55, '老板，我是海居租房中介的，您天祥尚府有没有房子要出租呢？', 'tianxiangshangfu_q1', 'q2', 'q2', 'q6', '2024-07-22 15:58:34', '2024-07-22 15:58:34', '天祥尚府', '听清楚,听不清');
INSERT INTO `speech_word` VALUES (56, '老板，我是海居租房中介滴，您茉莉公馆有没有房子要出租呢？', 'moligongguan_q1', 'q2', 'q2', 'q6', '2024-07-22 15:58:34', '2024-07-22 15:58:34', '茉莉公馆', '听清楚,听不清');
INSERT INTO `speech_word` VALUES (57, '老板，我是海居租房中介滴，您关山春晓有没有房子要出租呢？', 'guanshanchunxiao_q1', 'q2', 'q2', 'q6', '2024-07-22 15:58:34', '2024-07-22 15:58:34', '关山春晓', '听清楚,听不清');

SET FOREIGN_KEY_CHECKS = 1;
