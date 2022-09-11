--
-- Table structure for table `users2groups`
--

DROP TABLE IF EXISTS `users2groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users2groups` (
  `users_id` int unsigned NOT NULL,
  `groups_id` int unsigned NOT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified` datetime NOT NULL DEFAULT '1000-01-01 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`users_id`,`groups_id`),
  KEY `fk_users2groups_groups_idx` (`groups_id`),
  KEY `fk_users2groups_users_idx` (`users_id`),
  CONSTRAINT `fk_users2groups_groups` FOREIGN KEY (`groups_id`) REFERENCES `groups` (`id`),
  CONSTRAINT `fk_users2groups_users` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users2groups`
--

LOCK TABLES `users2groups` WRITE;
/*!40000 ALTER TABLE `users2groups` DISABLE KEYS */;
INSERT INTO `users2groups` VALUES (1,1,'2022-07-30 15:26:54','1000-01-01 00:00:00'),(2,2,'2022-07-30 15:26:54','1000-01-01 00:00:00'),(3,3,'2022-07-30 15:26:54','1000-01-01 00:00:00'),(4,3,'2022-07-30 15:26:54','1000-01-01 00:00:00');
/*!40000 ALTER TABLE `users2groups` ENABLE KEYS */;
UNLOCK TABLES;
