--
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS `genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genres` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `genre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `genre_UNIQUE` (`genre`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genres`
--

LOCK TABLES `genres` WRITE;
/*!40000 ALTER TABLE `genres` DISABLE KEYS */;
INSERT INTO `genres` VALUES (1,'Alternative Rock'),(2,'Blues'),(3,'Blues Rock'),(4,'Classical'),(5,'Country'),(6,'Dancehall'),(7,'Death Metal'),(8,'Electronic'),(9,'Folk'),(10,'Free Jazz'),(11,'Funk'),(12,'Funk Rock'),(13,'Grunge'),(14,'Hard Rock'),(15,'Heavy Metal'),(16,'Hip-Hop'),(17,'Industrial'),(18,'Instrumental Rock'),(19,'Jazz'),(20,'Jazz Fusion'),(21,'Metal'),(22,'Mundart Rock'),(23,'New Wave'),(24,'Pop'),(25,'Progressive Rock'),(26,'Punk'),(27,'Punk Rock'),(28,'Rap'),(29,'Reggae'),(30,'Rhythm & Blues'),(31,'Riot Jazz'),(32,'Rock'),(33,'Symphonic Metal'),(34,'Symphonic Rock'),(35,'World Music');
/*!40000 ALTER TABLE `genres` ENABLE KEYS */;
UNLOCK TABLES;
