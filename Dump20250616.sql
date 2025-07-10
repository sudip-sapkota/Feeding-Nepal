-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: feed
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS admin;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  id int NOT NULL AUTO_INCREMENT,
  username varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES admin WRITE;
/*!40000 ALTER TABLE admin DISABLE KEYS */;
/*!40000 ALTER TABLE admin ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `analytics`
--

DROP TABLE IF EXISTS analytics;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE analytics (
  id int NOT NULL AUTO_INCREMENT,
  metric_name varchar(100) NOT NULL,
  metric_value bigint NOT NULL,
  `description` text,
  recorded_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `analytics`
--

LOCK TABLES analytics WRITE;
/*!40000 ALTER TABLE analytics DISABLE KEYS */;
/*!40000 ALTER TABLE analytics ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS auth_group;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_group (
  id int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES auth_group WRITE;
/*!40000 ALTER TABLE auth_group DISABLE KEYS */;
/*!40000 ALTER TABLE auth_group ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS auth_group_permissions;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_group_permissions (
  id bigint NOT NULL AUTO_INCREMENT,
  group_id int NOT NULL,
  permission_id int NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY auth_group_permissions_group_id_permission_id_0cd325b0_uniq (group_id,permission_id),
  KEY auth_group_permissio_permission_id_84c5c92e_fk_auth_perm (permission_id),
  CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES auth_permission (id),
  CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES auth_group_permissions WRITE;
/*!40000 ALTER TABLE auth_group_permissions DISABLE KEYS */;
/*!40000 ALTER TABLE auth_group_permissions ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS auth_permission;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_permission (
  id int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  content_type_id int NOT NULL,
  codename varchar(100) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY auth_permission_content_type_id_codename_01ab375a_uniq (content_type_id,codename),
  CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES django_content_type (id)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES auth_permission WRITE;
/*!40000 ALTER TABLE auth_permission DISABLE KEYS */;
INSERT INTO auth_permission VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add donor',7,'add_donor'),(26,'Can change donor',7,'change_donor'),(27,'Can delete donor',7,'delete_donor'),(28,'Can view donor',7,'view_donor'),(29,'Can add donate',8,'add_donate'),(30,'Can change donate',8,'change_donate'),(31,'Can delete donate',8,'delete_donate'),(32,'Can view donate',8,'view_donate'),(33,'Can add volunteer',9,'add_volunteer'),(34,'Can change volunteer',9,'change_volunteer'),(35,'Can delete volunteer',9,'delete_volunteer'),(36,'Can view volunteer',9,'view_volunteer'),(37,'Can add message',10,'add_message'),(38,'Can change message',10,'change_message'),(39,'Can delete message',10,'delete_message'),(40,'Can view message',10,'view_message'),(41,'Can add inventory',11,'add_inventory'),(42,'Can change inventory',11,'change_inventory'),(43,'Can delete inventory',11,'delete_inventory'),(44,'Can view inventory',11,'view_inventory'),(45,'Can add volunteer',12,'add_volunteer'),(46,'Can change volunteer',12,'change_volunteer'),(47,'Can delete volunteer',12,'delete_volunteer'),(48,'Can view volunteer',12,'view_volunteer'),(49,'Can add donor report',13,'add_donorreport'),(50,'Can change donor report',13,'change_donorreport'),(51,'Can delete donor report',13,'delete_donorreport'),(52,'Can view donor report',13,'view_donorreport');
/*!40000 ALTER TABLE auth_permission ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS auth_user;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_user (
  id int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  last_login datetime(6) DEFAULT NULL,
  is_superuser tinyint(1) NOT NULL,
  username varchar(150) NOT NULL,
  first_name varchar(150) NOT NULL,
  last_name varchar(150) NOT NULL,
  email varchar(254) NOT NULL,
  is_staff tinyint(1) NOT NULL,
  is_active tinyint(1) NOT NULL,
  date_joined datetime(6) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY username (username)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES auth_user WRITE;
/*!40000 ALTER TABLE auth_user DISABLE KEYS */;
INSERT INTO auth_user VALUES (1,'pbkdf2_sha256$870000$M0fj3VwzmcodSELX9UTz8U$euVThehee1SRSWp2FgzIW6iNT9+JXGtKdam5Kkh8ats=','2025-06-01 06:25:25.678065',1,'rameshpradhan','','','ramesh@gmail.com',1,1,'2025-06-01 06:25:11.945520'),(2,'pbkdf2_sha256$870000$3IAIUYNsdsKsVvJQjrfnXs$wwZsLKZrTPtWR063F6F5ctDajQC7kjnh87TRuLNnaPQ=','2025-06-03 06:14:16.699514',1,'sudip','','','sudip@gmail.com',1,1,'2025-06-02 03:52:35.338335');
/*!40000 ALTER TABLE auth_user ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS auth_user_groups;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_user_groups (
  id bigint NOT NULL AUTO_INCREMENT,
  user_id int NOT NULL,
  group_id int NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY auth_user_groups_user_id_group_id_94350c0c_uniq (user_id,group_id),
  KEY auth_user_groups_group_id_97559544_fk_auth_group_id (group_id),
  CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group (id),
  CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES auth_user_groups WRITE;
/*!40000 ALTER TABLE auth_user_groups DISABLE KEYS */;
/*!40000 ALTER TABLE auth_user_groups ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS auth_user_user_permissions;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_user_user_permissions (
  id bigint NOT NULL AUTO_INCREMENT,
  user_id int NOT NULL,
  permission_id int NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY auth_user_user_permissions_user_id_permission_id_14a6b632_uniq (user_id,permission_id),
  KEY auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm (permission_id),
  CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES auth_permission (id),
  CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES auth_user_user_permissions WRITE;
/*!40000 ALTER TABLE auth_user_user_permissions DISABLE KEYS */;
/*!40000 ALTER TABLE auth_user_user_permissions ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS django_admin_log;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_admin_log (
  id int NOT NULL AUTO_INCREMENT,
  action_time datetime(6) NOT NULL,
  object_id longtext,
  object_repr varchar(200) NOT NULL,
  action_flag smallint unsigned NOT NULL,
  change_message longtext NOT NULL,
  content_type_id int DEFAULT NULL,
  user_id int NOT NULL,
  PRIMARY KEY (id),
  KEY django_admin_log_content_type_id_c4bce8eb_fk_django_co (content_type_id),
  KEY django_admin_log_user_id_c564eba6_fk_auth_user_id (user_id),
  CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES django_content_type (id),
  CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user (id),
  CONSTRAINT django_admin_log_chk_1 CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES django_admin_log WRITE;
/*!40000 ALTER TABLE django_admin_log DISABLE KEYS */;
/*!40000 ALTER TABLE django_admin_log ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS django_content_type;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_content_type (
  id int NOT NULL AUTO_INCREMENT,
  app_label varchar(100) NOT NULL,
  model varchar(100) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY django_content_type_app_label_model_76bd3d3b_uniq (app_label,model)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES django_content_type WRITE;
/*!40000 ALTER TABLE django_content_type DISABLE KEYS */;
INSERT INTO django_content_type VALUES (1,'admin','logentry'),(11,'adminpanel','inventory'),(12,'adminpanel','volunteer'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(8,'donor','donate'),(7,'donor','donor'),(6,'sessions','session'),(13,'volunteer','donorreport'),(10,'volunteer','message'),(9,'volunteer','volunteer');
/*!40000 ALTER TABLE django_content_type ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS django_migrations;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_migrations (
  id bigint NOT NULL AUTO_INCREMENT,
  app varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  applied datetime(6) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES django_migrations WRITE;
/*!40000 ALTER TABLE django_migrations DISABLE KEYS */;
INSERT INTO django_migrations VALUES (1,'contenttypes','0001_initial','2025-05-03 08:09:39.175841'),(2,'auth','0001_initial','2025-05-03 08:09:41.355932'),(3,'admin','0001_initial','2025-05-03 08:09:41.916963'),(4,'admin','0002_logentry_remove_auto_add','2025-05-03 08:09:41.933855'),(5,'admin','0003_logentry_add_action_flag_choices','2025-05-03 08:09:41.948299'),(6,'contenttypes','0002_remove_content_type_name','2025-05-03 08:09:42.302866'),(7,'auth','0002_alter_permission_name_max_length','2025-05-03 08:09:42.536605'),(8,'auth','0003_alter_user_email_max_length','2025-05-03 08:09:42.593654'),(9,'auth','0004_alter_user_username_opts','2025-05-03 08:09:42.609963'),(10,'auth','0005_alter_user_last_login_null','2025-05-03 08:09:42.786789'),(11,'auth','0006_require_contenttypes_0002','2025-05-03 08:09:42.800810'),(12,'auth','0007_alter_validators_add_error_messages','2025-05-03 08:09:42.822692'),(13,'auth','0008_alter_user_username_max_length','2025-05-03 08:09:43.065981'),(14,'auth','0009_alter_user_last_name_max_length','2025-05-03 08:09:43.334585'),(15,'auth','0010_alter_group_name_max_length','2025-05-03 08:09:43.374976'),(16,'auth','0011_update_proxy_permissions','2025-05-03 08:09:43.388673'),(17,'auth','0012_alter_user_first_name_max_length','2025-05-03 08:09:43.586867'),(18,'donor','0001_initial','2025-05-03 08:09:43.684656'),(19,'sessions','0001_initial','2025-05-03 08:09:43.798145'),(20,'donor','0002_donor_created_at_alter_donor_table','2025-05-03 08:26:36.758462'),(21,'donor','0003_alter_donor_created_at_alter_donor_table','2025-05-03 15:06:19.962131'),(22,'donor','0004_donate','2025-05-07 18:30:27.514774'),(23,'volunteer','0001_initial','2025-05-07 18:30:27.643887'),(24,'donor','0005_alter_donate_donor','2025-05-26 02:50:45.847557'),(25,'adminpanel','0001_initial','2025-06-12 03:04:15.954474'),(26,'volunteer','0002_message','2025-06-12 03:04:34.335318'),(27,'donor','0006_donate_accepted_donate_volunteer','2025-06-12 03:07:41.758524'),(28,'adminpanel','0002_inventory_collect','2025-06-16 03:18:19.828941'),(29,'volunteer','0003_donorreport','2025-06-16 03:29:12.640850');
/*!40000 ALTER TABLE django_migrations ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS django_session;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_session (
  session_key varchar(40) NOT NULL,
  session_data longtext NOT NULL,
  expire_date datetime(6) NOT NULL,
  PRIMARY KEY (session_key),
  KEY django_session_expire_date_a5c62663 (expire_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES django_session WRITE;
/*!40000 ALTER TABLE django_session DISABLE KEYS */;
INSERT INTO django_session VALUES ('0es768757dxiuhuhuxfmjssy2u614dkv','eyJ2b2x1bnRlZXJfZW1haWwiOiJrYXJ1bmthcmtpMTExQGdtYWlsLmNvbSIsImFkbWluX2xvZ2dlZF9pbiI6dHJ1ZX0:1uGzor:d3EC1EEqAVysoM9hKVL3i3_jkcQK4B6B9oxsq6AYAIU','2025-05-19 13:42:13.045222'),('1ag37d6m3bixvhkd6jwybaiyxlrggnbj','.eJyrVorPTS0uTkxPLVayUoqOjlGKj88qzs-DicYo6SgY6CiYAHGMkmdecn5RUWpyiUJBYnFxeX5RiiJIPkYpRilWR4EWeo1MQUp88tMz8xSKS5OTgZJppTkInbFKOkop-Xn5RfGZKUpWJrUAE6BBqQ:1uMIzI:XXd3VUuS0MSTdZjYYc1o8ZAk2-X415-lE_eoPNeocsE','2025-06-03 05:10:56.458623'),('1p0s8raysuls143m37t28p673lebcazx','eyJhZG1pbl9sb2dnZWRfaW4iOnRydWV9:1uFCSd:_rG7PpxB1AZi32wwW7UaSeCmsKT2G2AypIAWlZ-sTTk','2025-05-14 14:47:51.012717'),('2c0kt5iwxwqui521v6xu0o1mq53u3w1o','.eJxVjDkOwjAUBe_iGlnfW4gp6XOG6C8ODiBbipMKcXeIlALaNzPvpUbc1jxuLS3jLOqirDr9boT8SGUHcsdyq5prWZeZ9K7ogzY9VEnP6-H-HWRs-VsngQ4NnpnIQuSeObLvXAIfAkVwbCx69NALMbAhB-Ama8Aji50oqPcH80I4JQ:1uLwLj:XlZ-U-8lJYoQyPah4wu_Q2rGqdSLDmk6ey_RyquQlHo','2025-06-02 05:00:35.138638'),('2grr2ww4qv0ej7e8m6d1gtuztp42a8ta','eyJhZG1pbl9sb2dnZWRfaW4iOnRydWV9:1uLaXM:tLLdmGbusDY4Tq3vTGg7PjWEtioEHnsOdYToBadZZco','2025-06-01 05:43:08.628414'),('2v83f4j3uo2kurflce3w4d57uviivzmz','eyJhZG1pbl9sb2dnZWRfaW4iOnRydWV9:1uOZHQ:244JqL0xKjZtK4zt0--tbsJRiR9nPu5ecN9rDPMqnbs','2025-06-09 10:59:00.227900'),('3ou9xhb5xgxdwzixk4deqckl7hw5mtpx','.eJy1kM1OwzAQhF8l-BxFG8cpDUdulcoT1JW1Xjs_pdjIm4gD4t2xRRHwABz2Mt_MSDvvwuC2zmZjn8zixIOQov6tWaRnHwpwFwxTbCiGNS22KZbmRrl5is5fH2_ePwUz8pzT3sEOW7wnayUMtCcaSO06D6rv7QAdtRIVKtg7S0Ct7QC6UbagkJwcbV9KXzwzTp5z3emkhTEXjuFb1aKuoK5UPi0OgWJKntbqFZnfYnJ3hWuhxbmu_iMr-2I5xmkJFW9EGY7b9Sd5zg-4GOLXyurjE5GIeQE:1uLy7d:h5lyuGH3p_bYYyZa8DDn3Jn9Armh_exGOph7AvYdQzc','2025-06-02 06:54:09.433539'),('444968jwtei3i1ahl3bnw8yt34bveh0w','.eJzdizEOwjAQBL9irrYQioAiFS0SP4ijk2UflsH2Rb4YCsTfSQrEHyi2mdl5gefCFaOH_qjhwamVmagiZRsT9CBNfJzETnfuTmGFW8cZNFifY8HEIZDHWKCfayMNmEnEBpKlHQYDiDfh8qUGtNpptV9m4Fwc10puVpMVeXL1m9UbMDBq9U9td1gvFw6xKGnOLfLa0q8c4f0BKkl_pw:1uPloe:Nz_juq6BAzXrkakBxJb24iNzlQZg7q4ayC1JAYDTnzg','2025-06-12 18:34:16.122659'),('4l2kvmv1k1lqo4gid8re2sn1l72brrte','eyJ2b2x1bnRlZXJfZW1haWwiOiJzdXNkaXBzYXBrbzU1QGdtYWlsLmNvbSIsImFkbWluX2xvZ2dlZF9pbiI6dHJ1ZX0:1uIIu0:iCN5m8eUN8oybOlLspBLLrQ5XJuS98Zfi33sYzEaSsg','2025-05-23 04:16:56.723057'),('4oc974jiv8n0k7960ds695jt7w6uimzp','.eJzdkDEOwyAUQ69C_4yqJFI7ZOoBOnUNEULkFxEBv-JDlyp3Dxm69gAdbT978AfeFGoqiFljND7ACK-6mr7rb-7QZ0sRJOiIzMYht3yaFGi9MqWvq0CKTorhIoWCBzrPJZviKQmu1jbmWcPpgBQomKX4PXAn5_-hObffFkqUtV9gvG47gol0CQ:1uF6ml:_ZnMJ47rCzDASvN7JZvjpH_AzJukflJ5cEv5o5HO4YM','2025-05-14 08:44:15.663777'),('5c7604bpkbfly3ovi2v23mr9eyll1ze2','.eJztkkEKwjAURK8SZ_2RVuimKw_gDZoSQhpD2uRHEuNGvLsp4iXEzcDMY3bviSVxysovGAfCI4XKd2uzslH7gBG3uuq-689u70eTIggq2lK0s6XxaZJQai2Jv6sEiY7EaSAhcUnOsyjVmAavNRx2KiExk_g_f-k5NzE-LrGOtpmx6VxZtNw8Xm_XqcI9:1uDFQI:fnWQBIczfdqMXNkmIQywX_Jc4RBy289FHqh7a6oLdBk','2025-05-09 05:33:22.364544'),('5qvqdi5g4k2n2bcveku2ske1703dw0oi','eyJhZG1pbl9sb2dnZWRfaW4iOnRydWV9:1uGVzv:mZy0u5EKTtIoLngbahx0WBN4Q6eOib9mmJaharZjX7I','2025-05-18 05:51:39.785600'),('6cwfaeu16cvyhr8wa340k4yjal5ncjyo','.eJyrVorPTS0uTkxPLVayUoqOjlGKj88qzs-DicYo6SgY6CiYAHGMkmtuYmaOQl5-iUJafmleiiJIMkYpRilWRwGXRiNTkBKf_PTMPIXi0uRkoGRaac7A6oxV0lFKyc_LL4rPTFGyMqwFAKmhURQ:1uFT0K:CzUp5pWfHSOpSihDEtLfUHH7wtDP48LUrhQ2N3JDQ3E','2025-05-15 08:27:44.494949'),('a00kcmu9srw9k0ocxgeitt4atbi3n6yo','eyJhZG1pbl9sb2dnZWRfaW4iOnRydWV9:1uPDOZ:z2NbsYnRb3AGz4PS6EvSRXGY6ltQ834wszZr8NjX_og','2025-06-11 05:49:03.593714'),('ajgx8tqqbk95ztv4ksd1wy0bu5mbkhat','eyJ2b2x1bnRlZXJfZW1haWwiOiJwdWphMTAxQGdtYWlsLmNvbSIsImFkbWluX2xvZ2dlZF9pbiI6dHJ1ZX0:1uQ2D9:BN_WEhtwHZc49eVqLULNyTnB8yMtf4FEmUZZtLhOV8s','2025-06-13 12:04:39.859781'),('bc04o5vt8w7a3jt3r85bhvjhmoxafhio','eyJhZG1pbl9sb2dnZWRfaW4iOnRydWV9:1uPKIJ:A52VpAvYGUOyLyYZRUabMTHq6ZGiAi8dM_MMe5zJ16M','2025-06-11 13:11:03.705865'),('bicm3tvga0zxaunuz3bemlaluf8kt13w','.eJyljksKAjEQBa8S3jqIiqtZufUMkyEEuwnRJD2k57MQ7-6M4AlcvE1RFO8FkirNJ0J3sghUUvVZYmTyqaKb2swWvrBqiKzo0PcO3j9U6o86WHO05rLN4VaXkBMZLiFlI82MQXWVRrvl4DBY829hgMUiea4Tc_Nfbzums1IaNYxPOV_jDg93KXh_ANjxTE8:1uPZ40:38RWFE7aIVQzb65j1GGQwZGifSZ6NShZEFWeOU1nplQ','2025-06-12 04:57:16.990042'),('bsdglhm1cyt0j6amf8salva8tfv7f4x9','eyJ2b2x1bnRlZXJfZW1haWwiOiJrYXJ1bmthcmtpMTExQGdtYWlsLmNvbSIsImFkbWluX2xvZ2dlZF9pbiI6dHJ1ZX0:1uJ1qZ:no-VrYrNcujN2YP24Yi774JiTHHtVnPcYbDiVDksyGQ','2025-05-25 04:16:23.751676'),('c6922exkdu0k1zs5vn6zykvax03r4ijn','.eJw1ys0KAiEYheFbsbOWyKDNrFp0F-MgpjbY6PeBP0FE956zaHM4vDwfeCYuJnpMSuLFqVMLoZiQbUyYsNnSacwWlVLXda9HxxkSJoda7RrqUPOsYcyzMv2rhhQnKc4XKTRuTLZFJlH7PcfWgh_PuSEfPaX3YccaGsuC7w-KpzHL:1uJOay:_5546QL2iNa4rmuiPljB9SchKTnXFS7jsaDUs0jHEFg','2025-05-26 04:33:48.568753'),('c7m8t7umv1l348rkyfo8uq3n8n20vrol','eyJkb25vcl9pZCI6MSwidm9sdW50ZWVyX2VtYWlsIjoic3VzZGlwc2Fwa281QGdtYWlsLmNvbSJ9:1uFotk:xOUU-w10lXiknXn5ELxZekO0_oiyFmzzx7SM4OgpXoM','2025-05-16 07:50:24.043803'),('c8ay6nfig2rlx6yl3wvulmf96a6aw8ee','eyJhZG1pbl9sb2dnZWRfaW4iOnRydWV9:1uPzti:gsbXy8E1oPOI6QlUZa3aB-lvP1VHaEcZL5iISZgFDfQ','2025-06-13 09:36:26.364294'),('cg4lgpdkx9bbkjf61z23cr9i9h30kazr','eyJhZG1pbl9sb2dnZWRfaW4iOnRydWV9:1uPwN0:QA0B9fbnffP4MbGeQwIplNPgm5-9cZvUdkZOPvk-Mls','2025-06-13 05:50:26.293429'),('ec4qseythkp9cj7ahv2zk30scpmqhb06','eyJ2b2x1bnRlZXJfZW1haWwiOiJzdXNkaXBzYXBrbzU1QGdtYWlsLmNvbSJ9:1uOJB3:unf8PrITgUwghhw5Pe1Aku8dQOD1m6S_io07UmeprYc','2025-06-08 17:47:21.582879'),('gbtxqld5wnme4ljf3280hibltwm2wr8i','eyJhZG1pbl9sb2dnZWRfaW4iOnRydWUsInZvbHVudGVlcl9lbWFpbCI6InN1c2RpcHNhcGtvNTVAZ21haWwuY29tIn0:1uOpo7:iiq-X0yNrTvItUYCnqCnhSSPSa2BSx6mB2zQfmunr5A','2025-06-10 04:37:51.941064'),('gcz0jvvj10m28otki0hl1lalizshmphf','.eJyrVorPTS0uTkxPLVayUoqOjlGKj88qzs-DicYo6SgY6CiYAHGMkmdecn5RUWpyiUJBYnFxeX5RiiJIPkYpRilWR4F8vbFKOkpl-TmleSWpqUXxqbmJmTlAx2QnFpXmAYnsTENDQ4d0kKhecn6uUi0AwZQ7Pg:1uQdeb:fXVaTl2ZUZV3uIl3fpBVdX5aCjnhOwtRB-3IWiBFj7o','2025-06-15 04:03:29.665391'),('izpb8vrn3f94evfv9adg0om2gt034496','eyJhZG1pbl9sb2dnZWRfaW4iOnRydWV9:1uHGy2:X90z_lLuvelXuU6gM0Gpdpk0Ou90MYFKuKFgDSioIZI','2025-05-20 08:00:50.502185'),('ls0zuzi7g1g8g10qwt5dl9hm8c0z15s4','eyJhZG1pbl9sb2dnZWRfaW4iOnRydWV9:1uKS4f:CEQgULAhWGoeuGEmcAwNuaoRpkfsJLgdYdNfEAPuhhk','2025-05-29 02:28:49.702833'),('mo7z5bru989m3oao6d4767h0fh0oehtm','eyJhZG1pbl9sb2dnZWRfaW4iOnRydWV9:1uKrjM:Afhv1qPLWfMwVfgNRKtD6YlEWTy4Iavtk9kxJR5_NVs','2025-05-30 05:52:32.450909'),('o510uhpbaaz5gliji0xod87c5ejau0fk','.eJyrVorPTS0uTkxPLVayUoqOjlGKj88qzs-DicYo6SgY6CiYAHGMkmdecn5RUWpyiUJBYnFxeX5RiiJIPkYpRilWRwGXXiNTkBKf_PTMPIXi0uRkoGRaaQ5CZ6ySjlJKfl5-UXxmipKVSS0AzNQu1A:1uJPnR:grDfXhs-Sbm0b26xUhNnNK2r_NIpriAY_2wObKVI_hw','2025-05-26 05:50:45.170031'),('o9sy6wiva6kcupcmconbhk6qi6hx22kj','.eJxVjDkOwjAUBe_iGlnfW4gp6XOG6C8ODiBbipMKcXeIlALaNzPvpUbc1jxuLS3jLOqirDr9boT8SGUHcsdyq5prWZeZ9K7ogzY9VEnP6-H-HWRs-VsngQ4NnpnIQuSeObLvXAIfAkVwbCx69NALMbAhB-Ama8Aji50oqPcH80I4JQ:1uMKux:Qe-c8UM_oaLtWyNPARW2FR-isaRcAbTSCTdAzF-yaGc','2025-06-03 07:14:35.798123'),('ouimjvfw9dbzeuogba570w406ccwe3ti','eyJ2b2x1bnRlZXJfZW1haWwiOiJrYXJ1bmthcmtpMTExQGdtYWlsLmNvbSJ9:1uQL7v:p7cnm8dh0u5oC_MfnzfSL9fLH7jK7cDQvPILNwAR9-M','2025-06-14 08:16:31.206249'),('q5dxqwlzmth44ylxlyg69xxss73asvav','.eJyrVorPTS0uTkxPLVayUoqOjlGKj88qzs-DicYo6SgY6CiYAHGMkmdecn5RUWpyiUJBYnFxeX5RiiJIPkYpRilWR2Fw6nXNTczMUUjMKUpNTKlUKEpNzywuSS1KpZLtsUq1AO3JZgM:1uO6im:nqNBqe1uzZOKAS-mumU8MU4UB7DaiTG2bIY00M9RDiQ','2025-06-08 04:29:20.142361'),('s18m87aw0r3f1xctgs43rbjwqgk3j66f','eyJhZG1pbl9sb2dnZWRfaW4iOnRydWV9:1uHEd1:_XHUlcDQ_dnwy4qv8g3-7hJlRVe3ZCspGIkgFShHrVI','2025-05-20 05:30:59.122981'),('sogp58nvn98p7kv0gyiazu1iwnxyt7vl','.eJxVjDsOgzAQBe_iOrJsTMxCmZ4zWOvdBZwQW-JTRbl7gkRD-2bmfRTyO-Uwl3EUDimrblt2uamA-zaFfZUlJFadsuqyRaSX5APwE_NYNJW8LSnqQ9EnXXVfWObH6V4OJlynf10BmpaG-m6qgZkbdhFrhCjGWBBHDgnA-ogwRPRcM1F0YqVtSLwHUd8fHWVBxQ:1uLc8M:iyxMc_kaZ-keuiv97Z12vBHv0azawXy16ETummGpfaE','2025-06-01 07:25:26.159732'),('v66jenafeg3b79zs4ff0sq6ztz8jo9uh','.eJy1jzEOAiEURK-CvyZGjDZb2Zp4g2VDCHwJLvxvYNHCeHfZwngCi5li3kwxL7A-RzKJQ0BvIsGwlIYSTMZabcAKA4yjBmNulembapBiJ8WhS8OZHJeCbhF3W-uTi9-sXIOGSYp_bPfHtXLhEEnU5lyH15Z-ywkkeCYuJnoYlIQHp0YLYjGYbUz902xLo25zVEqdwppuHWd4fwB46VnW:1uR0id:_J4UVZZT8EAnRCWzuQaRNgaKY6xFgL1xkIZTFicwtes','2025-06-16 04:41:11.466582'),('wlh2uhii4c6vrwqzdb9g5rx3nq4265au','eyJ2b2x1bnRlZXJfZW1haWwiOiJzdXNkaXBzYXBrbzU1QGdtYWlsLmNvbSJ9:1uOWQ2:waK0ykM6zANZQBa3OpAYYpAQtumhordCW9rDshqxXS4','2025-06-09 07:55:42.806221'),('wmf41jkjp5k6t8dgl32fo0h4c8rp82bm','.eJyrVkrJz8svis9MUbIy0VGKz00tLk5MTy1WslKKjo5Rio_PKs7Pg4nGKOkoGOgoGJnqKMQo-eSnZ-YpFJcmJwMl00pzFEGyMUoxSrGxSrUA9X0b_w:1uPase:FLWsvEWY_r_Ny_KXfNH9QCVE3Mam8lzbBAIinXpvxMU','2025-06-12 06:53:40.926958'),('zusouo86mvr5nnczketm1i2cyjg6v4a4','.eJw1jDEKwzAQBL9ybC1MBKlc5RVpfEaI-BCKpTuw7DQhf49cuNgphmG_-Fg5dBfZgtSYC0ascTu0Y83e-0c67fCyCodQpbWYpPVqmhghvJvpZRmObo7ufYzndUtqOxVLSRbKOpwRgzHP-P0ByIsp-A:1uQN36:7JR7uubZCbFBQyEY938Esbn4ffI6Vjdgs6NUibF2l9s','2025-06-14 10:19:40.507440');
/*!40000 ALTER TABLE django_session ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donate`
--

DROP TABLE IF EXISTS donate;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE donate (
  id bigint NOT NULL AUTO_INCREMENT,
  donor_id bigint NOT NULL,
  quantity varchar(100) NOT NULL,
  food_type varchar(100) NOT NULL,
  `description` longtext,
  pickup_date date NOT NULL,
  pickup_time time NOT NULL,
  storage_type varchar(100) DEFAULT NULL,
  packaging_type varchar(100) DEFAULT NULL,
  expiry_date date DEFAULT NULL,
  created_at datetime(6) DEFAULT CURRENT_TIMESTAMP(6),
  volunteer_id int DEFAULT NULL,
  accepted enum('yes','no') NOT NULL DEFAULT 'no',
  PRIMARY KEY (id),
  KEY fk_donor_id (donor_id),
  KEY fk_donate_volunteer (volunteer_id),
  CONSTRAINT fk_donate_volunteer FOREIGN KEY (volunteer_id) REFERENCES volunteer (id) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_donor_id FOREIGN KEY (donor_id) REFERENCES donor_donor (id) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donate`
--

LOCK TABLES donate WRITE;
/*!40000 ALTER TABLE donate DISABLE KEYS */;
INSERT INTO donate VALUES (1,4,'10','Homemade Food','ASDFGHJ','2025-05-08','02:00:00','Refrigerated','Plastic Container','2025-05-08','2025-05-07 00:11:41.106221',NULL,'no'),(2,4,'10','Homemade Food','ASDFGHJ','2025-05-08','02:00:00','Refrigerated','Plastic Container','2025-05-08','2025-05-07 00:13:59.574848',NULL,'no');
/*!40000 ALTER TABLE donate ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donor`
--

DROP TABLE IF EXISTS donor;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE donor (
  id int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  email varchar(255) NOT NULL,
  phone varchar(20) NOT NULL,
  city varchar(100) NOT NULL,
  address text NOT NULL,
  `comment` text,
  `password` varchar(255) NOT NULL,
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY email (email)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donor`
--

LOCK TABLES donor WRITE;
/*!40000 ALTER TABLE donor DISABLE KEYS */;
INSERT INTO donor VALUES (1,'sudip sapkota','susdipsapko2@gmail.com','9843996625','kathmandu','kathmandu buspark lotsemall','hello lpease','pbkdf2_sha256$870000$uXwEEXJyZ2Fx6GLS7COmhE$1pp2JVImQpMzCWVdqUKxgyGrA6Q0Fffiombu5UbDCbc=','2025-05-03 02:42:22');
/*!40000 ALTER TABLE donor ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donor_donate`
--

DROP TABLE IF EXISTS donor_donate;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE donor_donate (
  id bigint NOT NULL AUTO_INCREMENT,
  quantity varchar(100) NOT NULL,
  food_type varchar(100) NOT NULL,
  `description` longtext,
  pickup_date date NOT NULL,
  pickup_time time(6) NOT NULL,
  storage_type varchar(100) DEFAULT NULL,
  packaging_type varchar(100) DEFAULT NULL,
  expiry_date date DEFAULT NULL,
  created_at datetime(6) NOT NULL,
  donor_id bigint NOT NULL,
  volunteer_id int DEFAULT NULL,
  accepted enum('yes','no') NOT NULL DEFAULT 'no',
  PRIMARY KEY (id),
  KEY donor_donate_donor_id_6aa41ebf_fk_donor_donor_id (donor_id),
  CONSTRAINT donor_donate_donor_id_6aa41ebf_fk_donor_donor_id FOREIGN KEY (donor_id) REFERENCES donor_donor (id)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donor_donate`
--

LOCK TABLES donor_donate WRITE;
/*!40000 ALTER TABLE donor_donate DISABLE KEYS */;
INSERT INTO donor_donate VALUES (1,'10','Junk Food','vbnm,.','2025-05-15','20:31:00.000000','Refrigerated','Plastic Container','2025-06-02','2025-05-26 02:50:53.259243',1,NULL,'no'),(2,'10','Junk Food','vbnm,.','2025-05-15','20:31:00.000000','Refrigerated','Plastic Container','2025-06-02','2025-05-26 02:52:56.154110',1,NULL,'no'),(3,'10','Canned Food','fgffff','2025-05-22','01:38:00.000000','Cool & Dark','Glass Jar','2025-11-26','2025-05-26 02:53:15.456782',1,NULL,'no'),(4,'10','Homemade Food','xhhhh','2025-06-07','08:52:00.000000','Cool & Dark','Plastic Container','2025-05-28','2025-05-26 03:17:49.097865',1,NULL,'no');
/*!40000 ALTER TABLE donor_donate ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donor_donor`
--

DROP TABLE IF EXISTS donor_donor;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE donor_donor (
  id bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  email varchar(254) NOT NULL,
  phone varchar(20) NOT NULL,
  city varchar(100) NOT NULL,
  address longtext NOT NULL,
  `comment` longtext,
  `password` varchar(255) NOT NULL,
  created_at datetime(6) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY email (email)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donor_donor`
--

LOCK TABLES donor_donor WRITE;
/*!40000 ALTER TABLE donor_donor DISABLE KEYS */;
INSERT INTO donor_donor VALUES (1,'sudip sapkota','sudip@gmail.com','9843996625','kathmandu','kathmandu buspark lotsemall','hello lpease','pbkdf2_sha256$870000$Vdl4Zjr4QKmC5qYeGWz1kx$+6/vKP+lEjWLC0R5bXTjqTZiCX5imzBoT84W7n35M3w=','2025-05-03 08:25:55.040169'),(2,'puja gurung','puja101@gmail.com','9843996625','kathmandu','kathmandu buspark lotsemall','hello lpease','111111','2025-05-03 14:22:54.538520'),(3,'sudip sapkota','susdipsapko23@gmail.com','9843996625','kathmandu','kathmandu buspark lotsemall','hello i wanna help to needy people','pbkdf2_sha256$870000$wNIz5DtyLCPimhj4sB3AnA$EvGURJztOTY6upCW0DXLwydg6qoKqY4Ib0Gd6a2dLCM=','2025-05-03 15:07:36.375570'),(4,'sudip sapkota','susdipsapko2@gmail.com','9843996625','kathmandu','kathmandu buspark lotsemall','hello i wanna help to needy people','pbkdf2_sha256$870000$CFrXyPZdozgnWLyyeERYmS$Mskc2p/UBpxFei5/0Cd+xAlOz+o4Pv0g6bSAnfkGb2w=','2025-05-03 15:19:50.694057'),(5,'karun karki','karunkarki111@gmail.com','9843996625','kathmandu','kathmandu buspark lotsemall','hello i wanna help to needy people','pbkdf2_sha256$870000$FGzMdVkuNaShHwyPjWJ0iH$DJLmx3ZvlIJOyxPoA5+kB8eo786hFosw1lV5RZAa9n4=','2025-05-07 18:34:55.655996'),(6,'sudip sapkota','susdipsapko3@gmail.com','9843996625','kathmandu','kathmandu buspark lotsemall','hello lpease','pbkdf2_sha256$870000$dT4uggLVOEKDnCvGEgZfP1$0EwcOQ870/JTCSkPeCoIjmdbBdT5pPbGcy+6s2NVeW8=','2025-05-14 07:17:29.890337');
/*!40000 ALTER TABLE donor_donor ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donorreport`
--

DROP TABLE IF EXISTS donorreport;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE donorreport (
  id int NOT NULL AUTO_INCREMENT,
  donor_id bigint NOT NULL,
  message longtext NOT NULL,
  created_at datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (id),
  KEY fk_donor (donor_id),
  CONSTRAINT fk_donor FOREIGN KEY (donor_id) REFERENCES donor_donor (id) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donorreport`
--

LOCK TABLES donorreport WRITE;
/*!40000 ALTER TABLE donorreport DISABLE KEYS */;
INSERT INTO donorreport VALUES (1,1,'zsxcvbhjk','2025-06-16 09:26:15.199144');
/*!40000 ALTER TABLE donorreport ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `food_management`
--

DROP TABLE IF EXISTS food_management;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE food_management (
  id int NOT NULL AUTO_INCREMENT,
  donate_id bigint NOT NULL,
  `status` varchar(50) NOT NULL,
  distribution_date date DEFAULT NULL,
  remarks text,
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY fk_foodmanagement_donate (donate_id),
  CONSTRAINT fk_foodmanagement_donate FOREIGN KEY (donate_id) REFERENCES donate (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `food_management`
--

LOCK TABLES food_management WRITE;
/*!40000 ALTER TABLE food_management DISABLE KEYS */;
/*!40000 ALTER TABLE food_management ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS inventory;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE inventory (
  id int NOT NULL AUTO_INCREMENT,
  food_type varchar(100) NOT NULL,
  quantity varchar(100) NOT NULL,
  storage_type varchar(100) DEFAULT NULL,
  packaging_type varchar(100) DEFAULT NULL,
  expiry_date date DEFAULT NULL,
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  collect varchar(10) NOT NULL DEFAULT 'no',
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory`
--

LOCK TABLES inventory WRITE;
/*!40000 ALTER TABLE inventory DISABLE KEYS */;
INSERT INTO inventory VALUES (1,'Fresh Produce','10','room temp','bottle','2025-06-17','2025-06-11 21:24:47','2025-06-13 04:45:54','yes'),(2,'Fresh Produce','10','room temp','bottle','2025-06-17','2025-06-11 21:26:42','2025-06-14 21:18:02','yes');
/*!40000 ALTER TABLE inventory ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS messages;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE messages (
  id bigint NOT NULL AUTO_INCREMENT,
  donor_id bigint NOT NULL,
  phone varchar(20) DEFAULT NULL,
  email varchar(255) DEFAULT NULL,
  message text,
  created_at datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY donor_id (donor_id),
  CONSTRAINT messages_ibfk_1 FOREIGN KEY (donor_id) REFERENCES donor_donor (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES messages WRITE;
/*!40000 ALTER TABLE messages DISABLE KEYS */;
/*!40000 ALTER TABLE messages ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS notification;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE notification (
  id int NOT NULL AUTO_INCREMENT,
  donor_id bigint DEFAULT NULL,
  volunteer_id int DEFAULT NULL,
  contact varchar(100) NOT NULL,
  message text NOT NULL,
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY fk_donor_notification (donor_id),
  KEY fk_volunteer_notification (volunteer_id),
  CONSTRAINT fk_donor_notification FOREIGN KEY (donor_id) REFERENCES donor_donor (id) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_volunteer_notification FOREIGN KEY (volunteer_id) REFERENCES volunteer (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification`
--

LOCK TABLES notification WRITE;
/*!40000 ALTER TABLE notification DISABLE KEYS */;
/*!40000 ALTER TABLE notification ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `volunteer`
--

DROP TABLE IF EXISTS volunteer;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE volunteer (
  id int NOT NULL AUTO_INCREMENT,
  full_name varchar(100) NOT NULL,
  email varchar(100) NOT NULL,
  mobile varchar(20) NOT NULL,
  dob date NOT NULL,
  gender varchar(20) DEFAULT NULL,
  address text NOT NULL,
  city varchar(50) NOT NULL,
  district varchar(50) NOT NULL,
  `password` varchar(128) NOT NULL,
  emergency_contact varchar(20) NOT NULL,
  emergency_name varchar(100) NOT NULL,
  availability varchar(50) NOT NULL,
  skills text,
  terms_accepted tinyint(1) NOT NULL DEFAULT '0',
  created_at datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY email (email)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `volunteer`
--

LOCK TABLES volunteer WRITE;
/*!40000 ALTER TABLE volunteer DISABLE KEYS */;
INSERT INTO volunteer VALUES (1,'sudip sapkota','susdipsapko2@gmail.com','+977','2025-05-15','male','kathmandu buspark lotsemall','kathmandu','kathmandu','pbkdf2_sha256$870000$h3LU8MEcGcTyU5EGXm6x6t$uacj0BuRo6Nnw2DK5E/lJKmLJac/YJo35HrXJeVwph4=','9843996625','sudip sapkota','weekdays','zxcvbnm,.',1,'2025-05-04 05:55:41'),(2,'puja gurung','puja101@gmail.com','+9779843996625','2025-05-30','female','kathmandu buspark lotsemall','kathmandu','kathmandu','pbkdf2_sha256$870000$dVNadZa66Rb7b2LXZ1LXhV$3OACP8TutfiKSf7gD19zqfOAKWrWBVkuE7DGZF9zuNE=','9843996625','puja gurung','full-time','hhhehhhe',1,'2025-05-04 06:26:26'),(3,'sudip sapkota','susdipsapko5@gmail.com','+977','2025-05-09','male','kathmandu buspark lotsemall','kathmandu','kathmandu','pbkdf2_sha256$870000$SWH6VPg6YcPZ3avMmoiMY2$pIiGk9OEF/H5hK7yK1qg9v/awflcdOwE1tMAy2gMfW8=','9843996625','puja gurung','weekdays','asdfghjkl;\'',1,'2025-05-16 06:50:16'),(4,'karun karki','karunkarki111@gmail.com','+9779843996625','2011-02-02','male','kathmandu buspark lotsemall','kathmandu','kathmandu','pbkdf2_sha256$870000$mQEUFPtzOj5ywBj8vL6Jin$j0Xr2VhADqsbVhcdFYIu9iCjQUnWs2+83eEyjLvuWYo=','9843996625','sudip sapkota','part-time','sadfghnm',1,'2025-05-19 11:07:16'),(6,'sudip sapkota','susdipsapko55@gmail.com','+977','2006-07-21','female','kathmandu buspark lotsemall','kathmandu','kathmandu','pbkdf2_sha256$870000$dgkzCQEZ4ynkkSVfKSYmir$GH5aJUmMj2fBwwcwhZEhnB9vXx/vbbJE61Bt4SL2Tic=','9843996625','karun karki','evenings','xcvbnm',1,'2025-05-23 03:15:44');
/*!40000 ALTER TABLE volunteer ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `volunteer_donorreport`
--

DROP TABLE IF EXISTS volunteer_donorreport;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE volunteer_donorreport (
  id bigint NOT NULL AUTO_INCREMENT,
  message longtext NOT NULL,
  created_at datetime(6) NOT NULL,
  donor_id bigint NOT NULL,
  PRIMARY KEY (id),
  KEY volunteer_donorreport_donor_id_5c76c9f5_fk_donor_donor_id (donor_id),
  CONSTRAINT volunteer_donorreport_donor_id_5c76c9f5_fk_donor_donor_id FOREIGN KEY (donor_id) REFERENCES donor_donor (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `volunteer_donorreport`
--

LOCK TABLES volunteer_donorreport WRITE;
/*!40000 ALTER TABLE volunteer_donorreport DISABLE KEYS */;
INSERT INTO volunteer_donorreport VALUES (1,'xcfghj','2025-06-16 03:35:00.685072',1);
/*!40000 ALTER TABLE volunteer_donorreport ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `volunteer_message`
--

DROP TABLE IF EXISTS volunteer_message;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE volunteer_message (
  id bigint NOT NULL AUTO_INCREMENT,
  `subject` varchar(200) NOT NULL,
  message longtext NOT NULL,
  sent_at datetime(6) NOT NULL,
  volunteer_id bigint NOT NULL,
  PRIMARY KEY (id),
  KEY volunteer_message_volunteer_id_46772592_fk_volunteer (volunteer_id),
  CONSTRAINT volunteer_message_volunteer_id_46772592_fk_volunteer FOREIGN KEY (volunteer_id) REFERENCES volunteer_volunteer (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `volunteer_message`
--

LOCK TABLES volunteer_message WRITE;
/*!40000 ALTER TABLE volunteer_message DISABLE KEYS */;
/*!40000 ALTER TABLE volunteer_message ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `volunteer_volunteer`
--

DROP TABLE IF EXISTS volunteer_volunteer;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE volunteer_volunteer (
  id bigint NOT NULL AUTO_INCREMENT,
  full_name varchar(100) NOT NULL,
  email varchar(254) NOT NULL,
  mobile varchar(20) NOT NULL,
  dob date NOT NULL,
  gender varchar(20) DEFAULT NULL,
  address longtext NOT NULL,
  city varchar(50) NOT NULL,
  district varchar(50) NOT NULL,
  `password` varchar(128) NOT NULL,
  emergency_contact varchar(20) NOT NULL,
  emergency_name varchar(100) NOT NULL,
  availability varchar(50) NOT NULL,
  skills longtext,
  terms_accepted tinyint(1) NOT NULL,
  created_at datetime(6) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `volunteer_volunteer`
--

LOCK TABLES volunteer_volunteer WRITE;
/*!40000 ALTER TABLE volunteer_volunteer DISABLE KEYS */;
/*!40000 ALTER TABLE volunteer_volunteer ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-16 22:27:24
