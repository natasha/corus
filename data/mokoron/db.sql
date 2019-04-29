-- MySQL dump 10.13  Distrib 5.6.12, for osx10.6 (x86_64)
--
-- Host: localhost    Database: neu
-- ------------------------------------------------------
-- Server version	5.6.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `sentiment`
--

DROP TABLE IF EXISTS `sentiment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sentiment` (
  `id` bigint(32) NOT NULL AUTO_INCREMENT,
  `tdate` varchar(128) DEFAULT NULL,
  `tname` varchar(128) DEFAULT NULL,
  `ttext` varchar(256) DEFAULT NULL,
  `ttype` int(10) DEFAULT '0',
  `trep` int(10) DEFAULT '0',
  `trtw` int(10) DEFAULT '0',
  `tfav` int(10) DEFAULT '0',
  `tstcount` int(10) DEFAULT '0',
  `tfoll` int(10) DEFAULT '0',
  `tfrien` int(10) DEFAULT '0',
  `listcount` int(10) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=441644379397451777 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sentiment`
--

LOCK TABLES `sentiment` WRITE;
/*!40000 ALTER TABLE `sentiment` DISABLE KEYS */;
INSERT INTO `sentiment` VALUES (408906695721877504,'1386325928','Va5ilina','Пропавшая в Хабаровске школьница почти сутки провела в яме у коллектор',2,0,0,0,183,95,158,0),(408906695700520960,'1386325928','i_wont_judge_ya','ЛЕНТА, Я СЕГОДНЯ ПОЛГОДА ДИРЕКШИОНЕЕЕЕР! С:\nХОТЯ ВСЕ РАВНО НИКТО НЕ ПОЗДРАВИТ ЛОЛ',2,0,0,0,19809,804,257,11)
INSERT INTO `sentiment` VALUES (410005806927847424,'1386587976','Victorika_nya','Открытые аудиозаписи нужны, чтобы прийти в гости и включить их ^.^',2,0,0,0,426,12,20,0),(408906695663161344,'1386325928','victorypanasenk','Царствие Божие внутрь вас есть.',2,0,0,0,1080,986,412,0)
