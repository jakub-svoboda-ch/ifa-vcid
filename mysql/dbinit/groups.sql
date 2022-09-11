--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `groups` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groups`
--

LOCK TABLES `groups` WRITE;
/*!40000 ALTER TABLE `groups` DISABLE KEYS */;
INSERT INTO `groups` VALUES (1,'Administratoren','Dürfen alle Funktionen der App verwenden.'),(2,'Editoren','Dürfen alles was Benutzer dürfen, und alle Stammdaten (Genres, Artists) bearbeiten.'),(3,'Benutzer','Dürfen neue Daten erfassen und eigene Daten (Alben & Songs) aktualisieren, aber nicht löschen.');
/*!40000 ALTER TABLE `groups` ENABLE KEYS */;
UNLOCK TABLES;
