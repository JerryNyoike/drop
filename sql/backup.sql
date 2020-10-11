-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: dropbeats
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `beat`
--

DROP TABLE IF EXISTS `beat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `beat` (
  `beat_id` binary(16) NOT NULL,
  `producer_id` binary(16) NOT NULL,
  `name` varchar(36) NOT NULL,
  `genre` varchar(36) NOT NULL,
  `address` varchar(100) NOT NULL,
  `prev_address` varchar(100) NOT NULL,
  `lease_price` int NOT NULL,
  `selling_price` int NOT NULL,
  `upload_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `beat_hash` varchar(100) NOT NULL,
  PRIMARY KEY (`beat_id`),
  UNIQUE KEY `beat_id` (`beat_id`),
  KEY `producer_id` (`producer_id`),
  CONSTRAINT `beat_ibfk_1` FOREIGN KEY (`producer_id`) REFERENCES `producer` (`producer_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beat`
--

LOCK TABLES `beat` WRITE;
/*!40000 ALTER TABLE `beat` DISABLE KEYS */;
INSERT INTO `beat` VALUES (_binary '(ùeèî¡Ω╗╕\0G\█;,',_binary '\┬\Ω╡▄ç\├\Ω⌐\0G\█;,','Friend of Mine feat. Vargas  La','House','.instanceeats\01_Friend_of_Mine_feat._Vargas__La.m4a','.instancepreviews\01_Friend_of_Mine_feat._Vargas__La.m4a',4560,12580,'2020-05-02 22:43:12','97deb4653ac2ea8ea2261f4e74a17c64'),(_binary '(¿çJî¡Ω╗╕\0G\█;,',_binary '\┬\Ω╡▄ç\├\Ω⌐\0G\█;,','Rules','Pop','.instanceeats\03_Rules.m4a','.instancepreviews\03_Rules.m4a',3450,10890,'2020-05-02 22:43:12','76bd8d62b7533d16d6da70a443919449'),(_binary 'YxvîxΩ╗╕\0G\█;,',_binary '\┬\Ω╡▄ç\├\Ω⌐\0G\█;,','02 Revenge feat. Eminem','Pop','.instanceeats\02_Revenge_feat._Eminem.m4a','.instancepreviews\02_Revenge_feat._Eminem.m4a',4560,11200,'2020-05-02 16:25:11','ce8e447fd2b8afa9cac11411019d53a9'),(_binary 'Y£\≡áîxΩ╗╕\0G\█;,',_binary '\┬\Ω╡▄ç\├\Ω⌐\0G\█;,','Apparently','Hip Hop','.instanceeats11_Apparently.mp3','.instancepreviews11_Apparently.mp3',5680,13450,'2020-05-02 16:25:11','1fc971af66a0b9087e357e8ef5c13fba'),(_binary 'i\r\╟\\îvΩ╗╕\0G\█;,',_binary '\┬\Ω╡▄ç\├\Ω⌐\0G\█;,','January 28th','Hip Hop','.instanceeats\02_January_28th.mp3','.instancepreviews\02_January_28th.mp3',5690,14580,'2020-05-02 16:11:18','4279a8e5fadbd7817396c3e3f793f18f'),(_binary 'iIc\÷îvΩ╗╕\0G\█;,',_binary '\┬\Ω╡▄ç\├\Ω⌐\0G\█;,','06. Daddy Lessons','Pop','.instanceeats\06._Daddy_Lessons.mp3','.instancepreviews\06._Daddy_Lessons.mp3',4590,13590,'2020-05-02 16:11:18','de52f4942be5c29d644855b89a24237f'),(_binary 'â\╔aVîxΩ╗╕\0G\█;,',_binary '\┬\Ω╡▄ç\├\Ω⌐\0G\█;,','LOYALTY','Hip Hop','.instanceeats\06._LOYALTY._Ft._Rihanna.mp3','.instancepreviews\06._LOYALTY._Ft._Rihanna.mp3',3400,10890,'2020-05-02 16:26:22','af642eb0ce0238e1c98f40a73d3a57e0'),(_binary 'Å(√^îíΩ╗╕\0G\█;,',_binary '\┬\Ω╡▄ç\├\Ω⌐\0G\█;,','Tribe','Hip Hop','.instanceeats\03._Tribe.mp3','.instancepreviews\03._Tribe.mp3',3450,15360,'2020-05-02 21:20:10','606de09ee008e512c97212dffe548e23'),(_binary 'Éî\∩╫îrΩ╗╕\0G\█;,',_binary '\┬\Ω╡▄ç\├\Ω⌐\0G\█;,','Water Under the Bridge','Pop','.instanceeats\06_Water_Under_the_Bridge.mp3','.instancepreviews\06_Water_Under_the_Bridge.mp3',4340,13590,'2020-05-02 15:43:46','ad651688207a45e2dca913cc20e9bea5'),(_binary 'òª\╥▌îqΩ╗╕\0G\█;,',_binary '\┬\Ω╡▄ç\├\Ω⌐\0G\█;,','Non Believers','Hip Hop','.instanceeats14._Non_Believers.mp3','.instancepreviews14._Non_Believers.mp3',2890,11340,'2020-05-02 15:36:45','2ca85cf8922cf2a245ed340a1339c946'),(_binary 'òª\╙0îqΩ╗╕\0G\█;,',_binary '\┬\Ω╡▄ç\├\Ω⌐\0G\█;,','Khalid - American Teen','Pop','.instanceeatsKhalid_-_American_Teen.mp3','.instancepreviewsKhalid_-_American_Teen.mp3',4590,13580,'2020-05-02 15:36:45','bf1f25f4f3a5ba9153464921ca3b4831'),(_binary 'ó{\≤îqΩ╗╕\0G\█;,',_binary '\┬\Ω╡▄ç\├\Ω⌐\0G\█;,','Khalid - American Teen','Pop','.instanceeatsKhalid_-_American_Teen.mp3','.instancepreviewsKhalid_-_American_Teen.mp3',4590,13580,'2020-05-02 15:37:07','bf1f25f4f3a5ba9153464921ca3b4831'),(_binary '\∩\\Y(ç\╔\Ω⌐\0G\█;,',_binary '\┬\Ω╡▄ç\├\Ω⌐\0G\█;,','Im a mess','Pop','.instanceeats\02_Im_a_Mess.m4a','.instancepreviews\02_Im_a_Mess.m4a',4560,13700,'2020-04-26 17:26:36','d6ff1a054dd0b2719048aee5323fa963');
/*!40000 ALTER TABLE `beat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `client` (
  `c_id` binary(16) NOT NULL,
  `profile_image_url` varchar(100) NOT NULL UNIQUE,
  `email` varchar(36) NOT NULL,
  `phone_number` int NOT NULL,
  `name` varchar(36) NOT NULL,
  `pwd` varchar(1024) NOT NULL,
  PRIMARY KEY (`c_id`),
  UNIQUE KEY `profile_image_url` (`profile_image_url`),
  UNIQUE KEY `c_id` (`c_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone_number` (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `payment_id` binary(16) NOT NULL,
  `beat_id` binary(16) NOT NULL,
  `amount` int NOT NULL,
  `client_id` binary(16) NOT NULL,
  PRIMARY KEY (`payment_id`),
  UNIQUE KEY `payment_id` (`payment_id`),
  KEY `beat_id` (`beat_id`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`beat_id`) REFERENCES `beat` (`beat_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `producer`
--

DROP TABLE IF EXISTS `producer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producer` (
  `producer_id` binary(16) NOT NULL,
  `profile_image_url` varchar(100) NOT NULL UNIQUE,
  `email` varchar(36) NOT NULL,
  `name` varchar(36) NOT NULL,
  `phone_number` varchar(36) NOT NULL,
  `pwd` varchar(1024) NOT NULL,
  PRIMARY KEY (`producer_id`),
  UNIQUE KEY `profile_image_url` (`profile_image_url`),
  UNIQUE KEY `producer_id` (`producer_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone_number` (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-06-10 17:19:10
