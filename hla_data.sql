-- MariaDB dump 10.19  Distrib 10.11.6-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: hla
-- ------------------------------------------------------
-- Server version	10.11.6-MariaDB-0+deb12u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `antigen`
--

DROP TABLE IF EXISTS `antigen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `antigen` (
  `antigen_id` int(11) NOT NULL,
  `HLA_Type` varchar(100) NOT NULL,
  `HLA_Serology` varchar(100) NOT NULL,
  PRIMARY KEY (`antigen_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `antigen`
--

LOCK TABLES `antigen` WRITE;
/*!40000 ALTER TABLE `antigen` DISABLE KEYS */;
INSERT INTO `antigen` VALUES
(103,'A*01:01///','A1//'),
(104,'A*02:01///','A2//'),
(106,'A*02:02///','A2//'),
(107,'A*02:03///','A203//'),
(108,'A*02:05///','A2//'),
(109,'A*03:01///','A3//'),
(110,'A*11:01///','A11//'),
(111,'A*11:02///','A11//'),
(112,'A*23:01///Bw4','A23(9)//'),
(113,'A*24:02///Bw4','A24(9)//'),
(114,'A*24:03///Bw4','A2403//'),
(115,'A*25:01///Bw4','A25(10)//'),
(116,'A*26:01///','A26(10)//'),
(117,'A*29:01///','A29(19)//'),
(118,'A*29:02///','A29(19)//'),
(119,'A*30:01///','A30(19)//'),
(120,'A*31:01///','A31(19)//'),
(121,'A*32:01///Bw4','A32(19)//'),
(122,'A*33:01///','A33(19)//'),
(123,'A*33:03///','A33(19)//'),
(124,'A*34:02///','A34(10)//'),
(125,'A*36:01///','A36//'),
(126,'A*43:01///','A43//'),
(127,'A*66:01///','A66(10)//'),
(128,'A*66:02///','A66(10)//'),
(129,'A*68:01///','A68(28)//'),
(130,'A*68:02///','A68(28)//'),
(131,'A*69:01///','A69(28)//'),
(132,'A*74:01///','A74(19)//'),
(133,'A*80:01///','A80//'),
(134,'/B*07:02//Bw6','/B7/'),
(135,'/B*07:03//Bw6','/B703/'),
(136,'/B*08:01//Bw6','/B8/'),
(137,'/B*13:02//Bw4','/B13/'),
(138,'/B*14:01//Bw6','/B64(14)/'),
(139,'/B*14:02//Bw6','/B65(14)/'),
(140,'/B*15:01//Bw6','/B62(15)/'),
(141,'/B*15:02//Bw6','/B75(15)/'),
(142,'/B*15:03//Bw6','/B72(70)/'),
(143,'/B*15:12//Bw6','/B76(15)/'),
(144,'/B*15:13//Bw4','/B77(15)/'),
(145,'/B*15:16//Bw4','/B63(15)/'),
(146,'/B*15:18//Bw6','/B71(70)/'),
(147,'/B*18:01//Bw6','/B18/'),
(148,'/B*27:03//Bw4','/B27/'),
(149,'/B*27:05//Bw4','/B27/'),
(150,'/B*27:08//Bw6','/B2708/'),
(151,'/B*35:01//Bw6','/B35/'),
(152,'/B*35:08//Bw6','/B35/'),
(153,'/B*37:01//Bw4','/B37/'),
(154,'/B*38:01//Bw4','/B38(16)/'),
(155,'/B*39:01//Bw6','/B3901/'),
(156,'/B*40:01//Bw6','/B60(40)/'),
(157,'/B*40:02//Bw6','/B61(40)/'),
(158,'/B*41:01//Bw6','/B41/'),
(159,'/B*42:01//Bw6','/B42/'),
(160,'/B*44:02//Bw4','/B44(12)/'),
(161,'/B*44:03//Bw4','/B44(12)/'),
(162,'/B*45:01//Bw6','/B45(12)/'),
(163,'/B*46:01//','/B46/'),
(164,'/B*47:01//Bw4','/B47/'),
(165,'/B*48:01//Bw6','/B48/'),
(166,'/B*49:01//Bw4','/B49(21)/'),
(167,'/B*50:01//Bw6','/B50(21)/'),
(168,'/B*51:01//Bw4','/B51(5)/'),
(169,'/B*52:01//Bw4','/B52(5)/'),
(170,'/B*53:01//Bw4','/B53/'),
(171,'/B*54:01//Bw6','/B54(22)/'),
(172,'/B*55:01//Bw6','/B55(22)/'),
(173,'/B*56:01//Bw6','/B56(22)/'),
(174,'/B*57:01//Bw4','/B57(17)/'),
(175,'/B*58:01//Bw4','/B58(17)/'),
(176,'/B*59:01//Bw4','/B59/'),
(177,'/B*67:01//Bw6','/B67/'),
(178,'/B*73:01//','/B73/'),
(179,'/B*78:01//Bw6','/B78/'),
(180,'/B*81:01//Bw6','/B81/'),
(181,'/B*82:02//Bw6','//'),
(182,'//C*01:02/','//Cw1'),
(183,'//C*02:02/','//Cw2'),
(184,'//C*03:03/','//Cw9(w3)'),
(185,'//C*03:04/','//Cw10(w3)'),
(186,'//C*04:01/','//Cw4'),
(187,'//C*04:03/','//'),
(188,'//C*05:01/','//Cw5'),
(189,'//C*06:02/','//Cw6'),
(190,'//C*07:01/','//Cw7'),
(191,'//C*07:02/','//Cw7'),
(192,'//C*08:01/','//Cw8'),
(193,'//C*08:02/','//Cw8'),
(194,'//C*12:02/','//'),
(195,'//C*14:02/','//'),
(196,'//C*15:02/','//'),
(197,'//C*16:01/','//'),
(198,'//C*17:01/','//'),
(199,'//C*18:01/','//'),
(203,'DRB1*01:01////','DR1//'),
(204,'DRB1*01:02////','DR1//'),
(206,'DRB1*01:03////','DR103//'),
(207,'DRB1*03:01////','DR17(3)//'),
(208,'DRB1*03:02////','DR18(3)//'),
(209,'DRB1*03:03////','DR18(3)//'),
(210,'DRB1*04:01////','DR4//'),
(211,'DRB1*04:02////','DR4//'),
(212,'DRB1*04:03////','DR4//'),
(213,'DRB1*04:04////','DR4//'),
(214,'DRB1*04:05////','DR4//'),
(215,'DRB1*07:01////','DR7//'),
(216,'DRB1*08:01////','DR8//'),
(217,'DRB1*08:02////','DR8//'),
(218,'DRB1*09:01////','DR9//'),
(219,'DRB1*10:01////','DR10//'),
(220,'DRB1*11:01////','DR11(5)//'),
(221,'DRB1*11:03////','DR11(5)//'),
(222,'DRB1*11:04////','DR11(5)//'),
(223,'DRB1*12:01////','DR12(5)//'),
(224,'DRB1*12:02////','DR12(5)//'),
(225,'DRB1*13:01////','DR13(6)//'),
(226,'DRB1*13:03////','DR13(6)//'),
(227,'DRB1*13:05////','DR13(6)//'),
(228,'DRB1*14:01////','DR14(6)//'),
(229,'DRB1*14:03////','DR1403//'),
(230,'DRB1*14:04////','DR1404//'),
(231,'DRB1*15:01////','DR15(2)//'),
(232,'DRB1*15:02////','DR15(2)//'),
(233,'DRB1*15:03////','DR15(2)//'),
(234,'DRB1*16:01////','DR16(2)//'),
(235,'DRB1*16:02////','DR16(2)//'),
(236,'DRB3*01:01////','DR52//'),
(237,'DRB3*02:02////','DR52//'),
(238,'DRB3*03:01////','DR52//'),
(239,'DRB4*01:01////','DR53//'),
(240,'DRB5*01:01////','DR51//'),
(241,'DRB5*02:02////','DR51//'),
(242,'/DQA1*02:01/DQB1*02:01//','/DQ2/'),
(243,'/DQA1*05:01/DQB1*02:01//','/DQ2/'),
(244,'/DQA1*02:01/DQB1*02:02//','/DQ2/'),
(245,'/DQA1*03:02/DQB1*02:02//','/DQ2/'),
(246,'/DQA1*05:01/DQB1*02:02//','/DQ2/'),
(247,'/DQA1*03:01/DQB1*03:01//','/DQ7(3)/'),
(248,'/DQA1*03:02/DQB1*03:01//','/DQ7(3)/'),
(249,'/DQA1*05:01/DQB1*03:01//','/DQ7(3)/'),
(250,'/DQA1*06:01/DQB1*03:01//','/DQ7(3)/'),
(251,'/DQA1*02:01/DQB1*03:02//','/DQ8(3)/'),
(252,'/DQA1*03:01/DQB1*03:02//','/DQ8(3)/'),
(253,'/DQA1*03:02/DQB1*03:02//','/DQ8(3)/'),
(254,'/DQA1*03:02/DQB1*03:03//','/DQ9(3)/'),
(255,'/DQA1*04:01/DQB1*03:03//','/DQ9(3)/'),
(256,'/DQA1*06:01/DQB1*03:03//','/DQ9(3)/'),
(257,'/DQA1*02:01/DQB1*04:01//','/DQ4/'),
(258,'/DQA1*04:01/DQB1*04:01//','/DQ4/'),
(259,'/DQA1*05:01/DQB1*04:01//','/DQ4/'),
(260,'/DQA1*03:01/DQB1*04:02//','/DQ4/'),
(261,'/DQA1*04:01/DQB1*04:02//','/DQ4/'),
(262,'/DQA1*06:01/DQB1*04:02//','/DQ4/'),
(263,'/DQA1*01:01/DQB1*05:01//','/DQ5(1)/'),
(264,'/DQA1*01:02/DQB1*05:01//','/DQ5(1)/'),
(265,'/DQA1*01:02/DQB1*05:02//','/DQ5(1)/'),
(266,'/DQA1*01:04/DQB1*05:03//','/DQ5(1)/'),
(267,'/DQA1*01:03/DQB1*06:01//','/DQ6(1)/'),
(268,'/DQA1*01:04/DQB1*06:01//','/DQ6(1)/'),
(269,'/DQA1*02:01/DQB1*06:01//','/DQ6(1)/'),
(270,'/DQA1*01:02/DQB1*06:02//','/DQ6(1)/'),
(271,'/DQA1*01:03/DQB1*06:03//','/DQ6(1)/'),
(272,'/DQA1*01:02/DQB1*06:04//','/DQ6(1)/'),
(273,'///DPA1*01:03/DPB1*01:01','//DPw1'),
(274,'///DPA1*02:01/DPB1*01:01','//DPw1'),
(275,'///DPA1*02:02/DPB1*01:01','//DPw1'),
(276,'///DPA1*03:01/DPB1*01:01','//DPw1'),
(277,'///DPA1*01:03/DPB1*02:01','//DPw2'),
(278,'///DPA1*01:03/DPB1*03:01','//DPw3'),
(279,'///DPA1*01:03/DPB1*04:01','//DPw4'),
(280,'///DPA1*02:01/DPB1*04:01','//DPw4'),
(281,'///DPA1*02:02/DPB1*04:01','//DPw4'),
(282,'///DPA1*03:01/DPB1*04:01','//DPw4'),
(283,'///DPA1*04:01/DPB1*04:01','//DPw4'),
(284,'///DPA1*01:03/DPB1*04:02','//DPw4'),
(285,'///DPA1*03:01/DPB1*04:02','//DPw4'),
(286,'///DPA1*02:01/DPB1*05:01','//DPw5'),
(287,'///DPA1*02:02/DPB1*05:01','//DPw5'),
(288,'///DPA1*03:01/DPB1*05:01','//DPw5'),
(289,'///DPA1*01:03/DPB1*06:01','//DPw6'),
(290,'///DPA1*02:01/DPB1*09:01','//'),
(291,'///DPA1*02:01/DPB1*11:01','//'),
(292,'///DPA1*02:01/DPB1*13:01','//'),
(293,'///DPA1*04:01/DPB1*13:01','//'),
(294,'///DPA1*02:01/DPB1*14:01','//'),
(295,'///DPA1*02:01/DPB1*15:01','//'),
(296,'///DPA1*02:01/DPB1*17:01','//'),
(297,'///DPA1*01:03/DPB1*18:01','//'),
(298,'///DPA1*02:01/DPB1*19:01','//'),
(299,'///DPA1*02:02/DPB1*28:01','//');
/*!40000 ALTER TABLE `antigen` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-17 14:56:34
