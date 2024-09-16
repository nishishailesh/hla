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
-- Table structure for table `SAB`
--

DROP TABLE IF EXISTS `SAB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SAB` (
  `patient_id` varchar(50) NOT NULL,
  `antigen_id` int(11) NOT NULL,
  `mfi_median` int(11) NOT NULL,
  PRIMARY KEY (`patient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `patient` (
  `patient_id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `ABO` varchar(10) NOT NULL,
  `Rh` int(10) NOT NULL,
  `HLA-A allele-1` varchar(10) NOT NULL,
  `HLA-A allele-2` varchar(10) NOT NULL,
  `HLA-B allele-1` varchar(10) NOT NULL,
  `HLA-B allele-2` varchar(10) NOT NULL,
  `HLA-Bw allele-1` varchar(10) NOT NULL,
  `HLA-Bw allele-2` varchar(10) NOT NULL,
  `HLA-Cw allele-1` varchar(10) NOT NULL,
  `HLA-Cw allele-2` varchar(10) NOT NULL,
  `HLA-DRB1 allele-1` varchar(10) NOT NULL,
  `HLA-DRB1 allele-2` varchar(10) NOT NULL,
  `HLA-DRB3 allele-1` varchar(10) NOT NULL,
  `HLA-DRB3 allele-2` varchar(10) NOT NULL,
  `HLA-DRB4 allele-1` varchar(10) NOT NULL,
  `HLA-DRB4 allele-2` varchar(10) NOT NULL,
  `HLA-DRB5 allele-1` varchar(10) NOT NULL,
  `HLA-DRB5 allele-2` varchar(10) NOT NULL,
  `HLA-DQA1 allele-1` varchar(10) NOT NULL,
  `HLA-DQA1 allele-2` varchar(10) NOT NULL,
  `HLA-DQB1 allele-1` varchar(10) NOT NULL,
  `HLA-DQB1 allele-2` varchar(10) NOT NULL,
  PRIMARY KEY (`patient_id`)
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

-- Dump completed on 2024-09-16 13:01:48
