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
-- Table structure for table `donor`
--

DROP TABLE IF EXISTS `donor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donor` (
  `patient_id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `ABO` varchar(10) DEFAULT NULL,
  `Rh` varchar(10) DEFAULT NULL,
  `HLA-A_allele-1` varchar(10) DEFAULT NULL,
  `HLA-A_allele-2` varchar(10) DEFAULT NULL,
  `HLA-B_allele-1` varchar(10) DEFAULT NULL,
  `HLA-B_allele-2` varchar(10) DEFAULT NULL,
  `HLA-Bw_allele-1` varchar(10) DEFAULT NULL,
  `HLA-Bw_allele-2` varchar(10) DEFAULT NULL,
  `HLA-Cw_allele-1` varchar(10) DEFAULT NULL,
  `HLA-Cw_allele-2` varchar(10) DEFAULT NULL,
  `HLA-DRB1_allele-1` varchar(10) DEFAULT NULL,
  `HLA-DRB1_allele-2` varchar(10) DEFAULT NULL,
  `HLA-DRB3_allele-1` varchar(10) DEFAULT NULL,
  `HLA-DRB3_allele-2` varchar(10) DEFAULT NULL,
  `HLA-DRB4_allele-1` varchar(10) DEFAULT NULL,
  `HLA-DRB4_allele-2` varchar(10) DEFAULT NULL,
  `HLA-DRB5_allele-1` varchar(10) DEFAULT NULL,
  `HLA-DRB5_allele-2` varchar(10) DEFAULT NULL,
  `HLA-DQA1_allele-1` varchar(10) DEFAULT NULL,
  `HLA-DQA1_allele-2` varchar(10) DEFAULT NULL,
  `HLA-DQB1_allele-1` varchar(10) DEFAULT NULL,
  `HLA-DQB1_allele-2` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`patient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `recipient`
--

DROP TABLE IF EXISTS `recipient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recipient` (
  `patient_id` bigint(20) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `ABO` varchar(10) DEFAULT NULL,
  `Rh` varchar(10) DEFAULT NULL,
  `HLA-A_allele-1` varchar(10) DEFAULT NULL,
  `HLA-A_allele-2` varchar(10) DEFAULT NULL,
  `HLA-B_allele-1` varchar(10) DEFAULT NULL,
  `HLA-B_allele-2` varchar(10) DEFAULT NULL,
  `HLA-Bw_allele-1` varchar(10) DEFAULT NULL,
  `HLA-Bw_allele-2` varchar(10) DEFAULT NULL,
  `HLA-Cw_allele-1` varchar(10) DEFAULT NULL,
  `HLA-Cw_allele-2` varchar(10) DEFAULT NULL,
  `HLA-DRB1_allele-1` varchar(10) DEFAULT NULL,
  `HLA-DRB1_allele-2` varchar(10) DEFAULT NULL,
  `HLA-DRB3_allele-1` varchar(10) DEFAULT NULL,
  `HLA-DRB3_allele-2` varchar(10) DEFAULT NULL,
  `HLA-DRB4_allele-1` varchar(10) DEFAULT NULL,
  `HLA-DRB4_allele-2` varchar(10) DEFAULT NULL,
  `HLA-DRB5_allele-1` varchar(10) DEFAULT NULL,
  `HLA-DRB5_allele-2` varchar(10) DEFAULT NULL,
  `HLA-DQA1_allele-1` varchar(10) DEFAULT NULL,
  `HLA-DQA1_allele-2` varchar(10) DEFAULT NULL,
  `HLA-DQB1_allele-1` varchar(10) DEFAULT NULL,
  `HLA-DQB1_allele-2` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`patient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `recipient_antibodies`
--

DROP TABLE IF EXISTS `recipient_antibodies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recipient_antibodies` (
  `patient_id` varchar(50) NOT NULL,
  `unique_string` varchar(100) NOT NULL,
  `antigen_id` int(11) NOT NULL,
  `mfi` int(11) NOT NULL,
  `HLA_Type` varchar(100) NOT NULL,
  `HLA_Serology` varchar(100) NOT NULL,
  PRIMARY KEY (`patient_id`,`unique_string`,`antigen_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `password` varchar(1000) NOT NULL,
  `expirydate` date NOT NULL,
  `authorization` varchar(300) NOT NULL,
  `insert_authorization_level` int(11) NOT NULL,
  `update_authorization_level` int(11) NOT NULL,
  `select_authorization_level` int(11) NOT NULL,
  `delete_authorization_level` int(11) NOT NULL,
  PRIMARY KEY (`user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-10 13:36:36
