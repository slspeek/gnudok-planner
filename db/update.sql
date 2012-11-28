-- MySQL dump 10.13  Distrib 5.1.63, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: djangoplanner
-- ------------------------------------------------------
-- Server version	5.1.63-0+squeeze1

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
LOCK TABLES `main_region` WRITE;
/*!40000 ALTER TABLE `main_region` DISABLE KEYS */;
INSERT INTO `main_region` VALUES (1,'Centrum','Centrum, de Pijp, Rivierenbuurt'),(2,'Groot-Oost','Diemen, Duivendrecht, Ijburg, Indische buurt, Oost, Watergraafsmeer, Zeeburg'),(3,'Groot-Zuid  ','Amstelveen, Buitenveldert, Oud-Zuid, Zuid, Zuideramstel'),(4,'Kennemerland  ','Bennebroek, Bloemendaal, Cruquis, Haarlem, Heemstede, Hoofddrop, IJmuiden, Nieuw-Vennep, Vijfhuizen'),(5,'Nieuw-West','Badhoevedorp, Geuzenveld, Halfweg, Nieuw-Sloten, Osdorp, Slotervaart, Westpoort, Zwanenburg'),(6,'Noord  ','Noord\r\n'),(7,'Oud-West  ','Baarsjes, Bos em Lommer, Oud-West, Spaarndammerbuurt, West, Westerpark'),(8,'Zuid-Oost','Zuid-Oost ');
/*!40000 ALTER TABLE `main_region` ENABLE KEYS */;
UNLOCK TABLES;


LOCK TABLES `main_region_timeslots` WRITE;
/*!40000 ALTER TABLE `main_region_timeslots` DISABLE KEYS */;
INSERT INTO `main_region_timeslots` VALUES (8,1,7),(7,1,5),(6,1,3),(5,1,1),(9,2,8),(10,2,2),(11,2,4),(12,2,10),(13,2,6),(14,3,7),(15,3,1),(16,3,3),(17,3,5),(18,3,9),(19,4,3),(20,4,7),(21,5,8),(22,5,4),(23,6,1),(24,6,2),(25,6,10),(26,6,9),(27,7,8),(28,7,2),(29,7,4),(30,7,10),(31,7,6),(32,8,9);
/*!40000 ALTER TABLE `main_region_timeslots` ENABLE KEYS */;
UNLOCK TABLES;
LOCK TABLES `main_timeslot` WRITE;
/*!40000 ALTER TABLE `main_timeslot` DISABLE KEYS */;
INSERT INTO `main_timeslot` VALUES (1,1,9,12.5),(2,1,13,16.5),(3,2,9,12.5),(4,2,13,16.5),(5,3,9,12.5),(6,3,13,16.5),(7,4,9,12.5),(8,4,13,16.5),(9,5,9,12.5),(10,5,13,16.5);
/*!40000 ALTER TABLE `main_timeslot` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-11-05 16:05:26
