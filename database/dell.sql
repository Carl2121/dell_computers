-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: dell_computers
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_fname` varchar(45) DEFAULT NULL,
  `customer_lname` varchar(45) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phone_number` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Robert','Gonzalez','197 Emily Curve Suite 810\nMoniquefurt, TN 96599','788.896.7541x64859'),(2,'Samantha','Stuart','292 Anderson Plaza Suite 152\nFrederickhaven, GU 35695','528-575-9203x59479'),(3,'Kevin','Woodward','497 Holder Ranch Suite 516\nSullivanhaven, MN 55384','(667)425-7071'),(4,'Kathleen','Doyle','9514 Gilbert Shoals Apt. 694\nSouth Elizabethchester, MH 76451','+1-271-297-8485x38892'),(5,'Cody','Wilkinson','57565 Smith Dam\nEast Rogerbury, LA 77328','+1-228-729-1748x77977'),(6,'David','Sandoval','54351 Wilson Mountains Suite 323\nGarciabury, NM 95521','485.624.2169'),(7,'Francisco','Montoya','48385 Klein Mount Apt. 559\nPatrickchester, NE 69612','001-259-471-7799x32039'),(8,'James','Mack','8436 Jennifer Island Apt. 085\nCarrietown, PW 88741','833.388.2888x769'),(9,'Joseph','Johnson','5563 Cooper Path Apt. 212\nBryantstad, CO 17910','597.749.4352x612'),(10,'Abigail','Riddle','5121 Ashley Hollow\nLake Mary, PR 64723','+1-621-721-1127x155'),(11,'Eric','Page','270 Andrea Centers\nSouth Lisaberg, FL 48120','509.893.6831'),(12,'Chloe','Stewart','32896 Davis Stream Apt. 806\nJosephborough, MH 92841','602-567-0845x8169'),(13,'Kathy','Davis','7070 Wilson Meadow Apt. 388\nNorth Donna, MI 39310','(706)523-2992'),(14,'Vanessa','Hayes','816 Brown Land\nNew Javier, IA 42651','(202)567-0278x3607'),(15,'Tina','Warren','95117 Aaron Mill Apt. 274\nMckinneybury, NY 92898','+1-737-315-3389'),(16,'Kenneth','Parker','07807 Joanna Ferry\nNorth Tannerland, MT 58319','478-869-1832x13948'),(17,'Samuel','Williams','2575 Richard Plaza Apt. 341\nNew Kayla, NV 18359','3163927885'),(18,'Susan','Baker','7826 Jessica Creek\nJerrystad, MO 46911','800-662-6437'),(19,'Alexandra','Holloway','4902 Mullins Mountains\nCooperfurt, NM 57087','(435)394-3562'),(20,'Christopher','Sparks','45238 Yoder Glen Suite 309\nEast Pamelaport, NC 68956','001-367-594-0827x0218'),(21,'Alex','English','742 Bruce Circle Apt. 658\nLake Michele, PA 47382','001-691-977-8234x0394'),(22,'Edward','Smith','USS Lopez\nFPO AP 22673','524.429.5708x9915'),(23,'Christina','King','273 Hernandez Trail Suite 821\nWest Sandra, MO 16849','455-539-3535x862'),(24,'Rachel','Jenkins','60404 Weaver Summit\nNew Amybury, CO 57335','683-344-0889'),(25,'Anne','Hall','1979 Ramirez Ridges\nHayneschester, NV 44557','474-493-8848x67749'),(26,'Uzziel Kyles','Ynciong','Barangay Santa Monica, PPC Palawan','09134523423');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_sales`
--

DROP TABLE IF EXISTS `product_sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_sales` (
  `sales_id` int NOT NULL,
  `products_id` int NOT NULL,
  KEY `fk_product_sales_products1_idx` (`products_id`),
  KEY `fk_product_sales_sales1` (`sales_id`),
  CONSTRAINT `fk_product_sales_products1` FOREIGN KEY (`products_id`) REFERENCES `products` (`id`),
  CONSTRAINT `fk_product_sales_sales1` FOREIGN KEY (`sales_id`) REFERENCES `sales` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_sales`
--

LOCK TABLES `product_sales` WRITE;
/*!40000 ALTER TABLE `product_sales` DISABLE KEYS */;
INSERT INTO `product_sales` VALUES (1,4),(1,3),(2,3),(3,21),(4,6),(4,22),(5,20),(5,3),(5,12),(6,13),(6,13),(6,8),(7,6),(8,15),(8,15),(9,25),(10,23),(10,3),(10,2),(11,24),(12,24),(12,18),(12,12),(13,19),(13,4),(13,21),(14,14),(14,20),(15,12),(16,23),(17,2),(18,15),(18,4),(19,22),(19,3),(20,5),(21,12),(21,22),(22,14),(23,25),(24,12),(24,8),(24,24),(25,8),(25,25),(25,11);
/*!40000 ALTER TABLE `product_sales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_name` varchar(255) DEFAULT NULL,
  `product_price` decimal(10,0) DEFAULT NULL,
  `product_description` varchar(255) DEFAULT NULL,
  `product_stock` int DEFAULT NULL,
  `product_category` varchar(45) DEFAULT NULL,
  `is_dell` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Dell XPS 13',1894,'Capital unit budget it campaign response sea window site new father arrive.',72,'Desktop',1),(2,'Dell XPS 15',589,'May theory let occur during note article customer.',55,'Monitor',1),(3,'Dell Inspiron 14',759,'Yard defense region window experience of.',42,'Laptop',1),(4,'Dell Latitude 7420',1024,'When attorney suggest upon finally year professional within across control.',38,'Laptop',1),(5,'Dell Precision 5550',1705,'Sometimes space finish mother himself today to change we send quite.',36,'Desktop',1),(6,'Dell G15 Gaming',139,'Foreign son almost magazine better decade three son beautiful.',51,'Laptop',1),(7,'Dell Alienware m15',1327,'Student order modern music end blue list kitchen.',86,'Laptop',1),(8,'Dell OptiPlex 3090',761,'Third color pretty worry and federal.',91,'Monitor',1),(9,'Dell Vostro 3500',1305,'Indicate employee agree head major east big maintain.',38,'Monitor',1),(10,'Dell Chromebook 3100',1202,'Himself study billion us value beat read station dog serious our.',67,'Desktop',1),(11,'Dell UltraSharp Monitor',886,'Those home camera heart particularly service little church culture.',69,'Accessory',1),(12,'Dell Dock WD19',171,'Design message guess who fill notice go case face health artist enjoy.',43,'Laptop',1),(13,'Dell PowerEdge T40',617,'Exist Mrs current want far reason camera but.',16,'Desktop',1),(14,'Dell EMC Unity XT',1062,'To these tough base feeling idea.',44,'Laptop',1),(15,'Dell Wyse 5070',1159,'Race paper care since million spend million people.',34,'Accessory',1),(16,'Dell G7 17 Gaming',1845,'Student agent security wall forget safe any particularly our between evidence be.',77,'Monitor',1),(17,'Dell Inspiron 7000',1653,'Deal agree race oil pressure prove.',79,'Desktop',1),(18,'Dell P2422H Monitor',185,'Appear find go laugh finish green reflect reduce structure suggest boy cell.',17,'Laptop',1),(19,'Dell Rugged Extreme 7220',1255,'Fact strong under we yet interview door final bill reflect act.',10,'Monitor',1),(20,'Dell Alienware Aurora R12',1743,'Million college upon out side suddenly director cover leave wish.',35,'Accessory',1),(21,'Dell OptiPlex 7080',170,'Like chair Congress brother run recognize minute the road building recognize.',11,'Accessory',1),(22,'Dell Latitude 5420',295,'Yes ask bed also away reveal suggest start save.',21,'Laptop',1),(23,'Dell Inspiron 15 3000',500,'Law high call sit fact see difficult letter whatever face between.',27,'Desktop',1),(24,'Dell G3 Gaming',1987,'Card street song consumer describe record your special none although but.',57,'Desktop',1),(25,'Dell UltraSharp Webcam',1935,'Should effort company staff man try determine old guess these land another activity.',13,'Accessory',1),(26,'Macintosh 69',589,'May theory let occur during note article customer.',55,'Apple MAC',0);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales`
--

DROP TABLE IF EXISTS `sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sale_total_value` decimal(10,0) DEFAULT NULL,
  `quantity_sold` int DEFAULT NULL,
  `customers_id` int NOT NULL,
  `status` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_sales_customers1_idx` (`customers_id`),
  CONSTRAINT `fk_sales_customers1` FOREIGN KEY (`customers_id`) REFERENCES `customers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales`
--

LOCK TABLES `sales` WRITE;
/*!40000 ALTER TABLE `sales` DISABLE KEYS */;
INSERT INTO `sales` VALUES (1,3754,3,16,'Pending'),(2,3374,10,7,'Completed'),(3,760,10,24,'Pending'),(4,2943,8,11,'Cancelled'),(5,2575,8,6,'Completed'),(6,3731,6,1,'Cancelled'),(7,1562,1,21,'Pending'),(8,4341,4,11,'Pending'),(9,4007,8,19,'Cancelled'),(10,4014,7,18,'Completed'),(11,4298,8,23,'Pending'),(12,4989,7,14,'Cancelled'),(13,4045,8,23,'Completed'),(14,3043,5,12,'Cancelled'),(15,3657,8,1,'Pending'),(16,2445,6,25,'Completed'),(17,3193,2,12,'Cancelled'),(18,2651,3,13,'Cancelled'),(19,1303,5,23,'Completed'),(20,699,1,16,'Completed'),(21,918,7,15,'Completed'),(22,2057,3,5,'Pending'),(23,558,4,20,'Completed'),(24,1204,5,22,'Cancelled'),(25,4064,9,15,'Completed');
/*!40000 ALTER TABLE `sales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','admin_pwd','admin');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-14 12:27:42
