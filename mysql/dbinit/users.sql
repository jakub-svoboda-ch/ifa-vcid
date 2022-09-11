--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `email` varchar(255) NOT NULL,
  `email_confirmed_at` datetime DEFAULT NULL,
  `password` varchar(128) NOT NULL,
  `active` tinyint DEFAULT '0',
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified` datetime NOT NULL DEFAULT '1000-01-01 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `last_seen` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','admin@example.com','2022-07-30 15:13:42','pbkdf2:sha256:260000$RlgpwdKOuxMOpfY3$f3d24b43508b001250cb85161475120314977fce4c369cd459f07d56b751cfc2',1,'2022-07-30 15:11:28','2022-07-30 15:14:03','2022-07-30 15:11:28'),(2,'editor','editor@example.com','2022-07-30 15:13:42','pbkdf2:sha256:260000$INA1Kh1dMLhefDSM$1cc6af327e9fb19516775b71dfa94ab1267982470cacf20ae619a86c3ed0bb6d',1,'2022-07-30 15:11:58','2022-07-30 15:14:03','2022-07-30 15:11:58'),(3,'user1','user1@example.com','2022-07-30 15:13:42','pbkdf2:sha256:260000$Rn1yD8KXH4f6SILC$dfd08e09ae377a93bf04c2d0bc08816e36fec54d420e0548e0ae350abbb6b310',1,'2022-07-30 15:12:45','2022-07-30 15:14:03','2022-07-30 15:12:46'),(4,'user2','user2@example.com','2022-07-30 15:13:42','pbkdf2:sha256:260000$Rn1yD8KXH4f6SILC$dfd08e09ae377a93bf04c2d0bc08816e36fec54d420e0548e0ae350abbb6b310',0,'2022-07-30 15:12:45','2022-07-30 15:21:28','2022-07-30 15:12:46');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
