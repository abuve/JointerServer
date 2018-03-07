-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: AutoDeploy2
-- ------------------------------------------------------
-- Server version	5.7.17-log

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
-- Dumping data for table `user_center_permission`
--

LOCK TABLES `user_center_permission` WRITE;
/*!40000 ALTER TABLE `user_center_permission` DISABLE KEYS */;
INSERT INTO `user_center_permission` VALUES (10,'dashboard','GET','控制面板'),(11,'cmdb-server-list','GET',''),(12,'cmdb-server-json','GET',''),(13,'cmdb-server-json','POST',''),(14,'cmdb-server-json','PUT',''),(15,'cmdb-server-json','DELETE',''),(16,'cmdb-asset-create','GET','CMDB资源新增页'),(17,'cmdb-docker-list','GET','Docker列表页'),(18,'cmdb-docker-json','GET','Docker列表页Json数据'),(19,'cmdb-asset-detail','GET','CMDB资产详情页'),(20,'cmdb-approval-list','GET','CMDB资产审批页'),(21,'cmdb-approval-json','GET','CMDB资产审批Json数据'),(22,'cmdb-approval-json','POST','CMDB资产审批数据提交'),(23,'cmdb-approval-json','PUT','CMDB资产审批数据修改'),(24,'cmdb-approval-json','DELETE','CMDB资产审批数据删除'),(25,'cmdb-business-list','GET','业务线列表页'),(26,'cmdb-business-json','GET','业务线Json数据'),(27,'cmdb-business-json','POST','业务线数据新增'),(28,'cmdb-business-json','PUT','业务线数据修改'),(29,'cmdb-business-json','DELETE','业务线数据删除'),(30,'cmdb-business-detail','GET','业务线数据详情模块'),(31,'cmdb-idc-list','GET','IDC列表页'),(32,'cmdb-idcs','GET','IDC列表页Json数据'),(33,'cmdb-idcs','POST','IDC数据新增'),(34,'cmdb-idcs','PUT','IDC数据修改'),(35,'cmdb-idcs','DELETE','IDC数据删除'),(36,'cmdb-add-idc','GET','IDC数据新增页面'),(37,'cmdb-edit-idc','GET','IDC数据编辑页面'),(38,'server-config-nginx','GET','Nginx配置管理页'),(39,'server-config-nginx-fileTreeJson','POST','Nginx配置目录json数据获取'),(40,'server-config-nginx-version-json','GET','Nginx配置目录版本信息获取'),(41,'server-config-nginx-version-json','POST','Nginx配置目录版本信息提交'),(42,'server-config-nginx-version-json','PUT','Nginx配置目录版本信息修改'),(43,'server-config-nginx-version-tree','GET','Nginx配置目录版本信息获取'),(44,'server-config-nginx-file-data','GET','Nginx配置文件-查询'),(45,'server-config-nginx-file-data','POST','Nginx配置文件-新增'),(46,'server-config-nginx-file-data','PUT','Nginx配置文件-修改'),(47,'server-config-nginx-file-data','DELETE','Nginx配置文件-删除'),(48,'server-config-nginx-file-push','POST','Nginx配置文件版本发布'),(49,'server-config-nginx-rightStatus','POST','Nginx配置右侧信息获取'),(50,'server-config-group','GET','应用配置-分组管理'),(51,'server-config-group-json','GET','应用配置-分组Json数据获取'),(52,'server-config-group-json','POST','应用配置-分组数据添加'),(53,'server-config-group-json','PUT','应用配置-分组数据修改'),(54,'server-config-group-json','DELETE','应用配置-分组数据删除'),(55,'server-config-instance','GET','应用配置-实例页面管理'),(56,'server-config-instance-json','GET','应用配置-实例Json数据获取'),(57,'server-config-instance-update-server-instance','GET','应用配置-实例数据-查询'),(58,'server-config-instance-update-server-instance','POST','应用配置-实例数据-创建'),(59,'server-config-instance-update-server-instance','PUT','应用配置-实例数据-修改'),(60,'server-config-instance-update-server-instance','DELETE','应用配置-实例数据-删除'),(61,'server-config-instance-get-instance-by-groupid','GET','应用配置-根据分组ID获取实例数据'),(62,'server-config-group-update-server-group','GET','应用配置-分组数据查询'),(63,'server-config-group-update-server-group','POST','应用配置-分组数据创建'),(64,'server-config-group-update-server-group','PUT','应用配置-分组数据修改'),(65,'server-config-group-update-server-group','DELETE','应用配置-分组数据删除'),(66,'server-config-group-update-public-group','GET','应用配置-公共分组数据查询'),(67,'server-config-group-update-public-group','POST','应用配置-公共分组数据创建'),(68,'server-config-docker','GET','应用配置-Docker配置管理页面'),(69,'server-config-docker-json','GET','应用配置-Docker页面Json数据获取'),(70,'server-config-docker-update-server-docker','GET','应用配置-Docker数据-查询'),(71,'server-config-docker-update-server-docker','POST','应用配置-Docker数据-创建'),(72,'server-config-docker-update-server-docker','PUT','应用配置-Docker数据-修改'),(73,'server-config-docker-update-server-docker','DELETE','应用配置-Docker数据-删除'),(74,'server-config-logs','GET','应用配置-日志地址页面'),(75,'server-config-logs-json','GET','应用配置-日志地址-json数据获取'),(76,'server-config-logs-update-server-logs','GET','应用配置-日志地址-获取'),(77,'server-config-logs-update-server-logs','POST','应用配置-日志地址-创建'),(78,'server-config-logs-update-server-logs','PUT','应用配置-日志地址-修改'),(79,'server-config-logs-update-server-logs','DELETE','应用配置-日志地址-删除'),(80,'server-config-urlmaps','GET','应用配置-url映射管理页'),(81,'server-config-urlmaps-json','GET','应用配置-url映射Json数据获取'),(82,'server-config-get-urlmaps-detail','POST','应用配置-url映射详情数据'),(83,'server-config-urlmaps-update-server-urlmaps','GET','应用配置-url映射-查询'),(84,'server-config-urlmaps-update-server-urlmaps','POST','应用配置-url映射-创建'),(85,'server-config-urlmaps-update-server-urlmaps','PUT','应用配置-url映射-修改'),(86,'server-config-urlmaps-update-server-urlmaps','DELETE','应用配置-url映射-删除'),(87,'server-config-urlmaps-update-server-urlmaps-groups','GET','应用配置-url映射分组-获取'),(88,'server-config-urlmaps-update-server-urlmaps-groups','POST','应用配置-url映射分组-创建'),(89,'user_center-user-list','GET','用户管理页面'),(90,'user_center-users','GET','用户管理数据查询'),(91,'user_center-users','POST','用户管理数据新增'),(92,'user_center-users','PUT','用户管理数据修改'),(93,'user_center-users','DELETE','用户管理数据删除'),(94,'user_center-edit-user','GET','用户管理数据编辑页面'),(95,'user_center-group-list','GET','用户管理-分组管理页面'),(96,'user_center-groups','GET','用户管理-分组数据-查询'),(97,'user_center-groups','POST','用户管理-分组数据-新增'),(98,'user_center-groups','PUT','用户管理-分组数据-修改'),(99,'user_center-groups','DELETE','用户管理-分组数据-删除'),(100,'user_center-add-group','GET','用户管理-分组数据-新增页面'),(101,'user_center-edit-group','GET','用户管理-分组数据-修改页面'),(102,'user_center-permission-list','GET','权限管理页面'),(103,'user_center-permission-json','GET','权限管理Json数据获取'),(104,'user_center-permission-json','POST','权限管理数据添加'),(105,'user_center-permission-json','PUT','权限管理数据修改'),(106,'user_center-permission-json','DELETE','权限管理数据删除'),(107,'user_center-permission-add','GET','权限管理数据添加html页面'),(108,'user_center-permission-edit','GET','权限管理-修改页面html'),(109,'user_center-roles-list','GET','角色管理html页面'),(110,'user_center-roles-json','GET','角色管理-json数据获取'),(111,'user_center-roles-json','POST','角色管理-数据添加'),(112,'user_center-roles-json','PUT','角色管理-数据修改'),(113,'user_center-roles-json','DELETE','角色管理-数据删除'),(114,'user_center-roles-add','GET','权限管理-数据添加页面'),(115,'user_center-roles-edit','GET','角色管理修改页面html'),(116,'application-server','GET','应用列表页'),(117,'application-servers','GET','应用管理页Json数据'),(118,'application-servers','POST','应用数据新增'),(119,'application-servers','PUT','应用数据修改'),(120,'application-servers','DELETE','应用数据删除'),(121,'server-config','GET','应用配置html页面'),(122,'application-add-server','GET','应用添加html页面'),(123,'application-edit-server','GET','应用修改html页面'),(124,'get_app_by_project','GET','任务管理-根据project获取app信息'),(125,'mission-mission-list','GET','任务管理html页面'),(126,'mission-mission-json','GET','任务管理-Json数据获取'),(127,'mission-mission-json','PUT','任务管理-数据修改'),(128,'mission-mission-json','DELETE','任务管理-数据删除'),(129,'mission-mission-create','GET','任务管理-任务创建html页面'),(130,'mission-mission-create','POST','任务管理-任务创建数据添加'),(131,'mission-mission-detail','GET','任务管理-任务详情html页面'),(132,'mission-mission-detail-json','GET','任务管理-详情页面json数据获取'),(133,'project-project-list','GET','Project项目管理页'),(134,'project-project-json','GET','Project项目管理-Json数据获取'),(135,'project-project-json','POST','Project项目管理-数据新增'),(136,'project-project-json','PUT','Project项目管理-数据修改'),(137,'project-project-json','DELETE','Project项目管理-数据删除'),(138,'project-add-project','GET','Project项目管理-项目新增页面'),(139,'project-edit-project','GET','	Project项目管理-数据修改页面'),(140,'project-projectviews','GET','Project项目管理-项目视图页面'),(141,'project-appviews','GET','Project项目管理-应用视图页面'),(142,'dashboard-chart-ajax','GET','控制面板json数据');
/*!40000 ALTER TABLE `user_center_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `user_center_roles`
--

LOCK TABLES `user_center_roles` WRITE;
/*!40000 ALTER TABLE `user_center_roles` DISABLE KEYS */;
INSERT INTO `user_center_roles` VALUES (1,'系统管理员',''),(5,'OM一般用户','');
/*!40000 ALTER TABLE `user_center_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `user_center_roles_permissions`
--

LOCK TABLES `user_center_roles_permissions` WRITE;
/*!40000 ALTER TABLE `user_center_roles_permissions` DISABLE KEYS */;
INSERT INTO `user_center_roles_permissions` VALUES (186,1,10),(187,1,11),(188,1,12),(189,1,13),(190,1,14),(191,1,15),(192,1,16),(193,1,17),(194,1,18),(195,1,19),(196,1,20),(197,1,21),(198,1,22),(199,1,23),(200,1,24),(201,1,25),(202,1,26),(203,1,27),(204,1,28),(205,1,29),(206,1,30),(207,1,31),(208,1,32),(209,1,33),(210,1,34),(211,1,35),(212,1,36),(213,1,37),(214,1,38),(215,1,39),(216,1,40),(217,1,41),(218,1,42),(219,1,43),(220,1,44),(221,1,45),(222,1,46),(223,1,47),(224,1,48),(225,1,49),(226,1,50),(227,1,51),(228,1,52),(229,1,53),(230,1,54),(231,1,55),(232,1,56),(233,1,57),(234,1,58),(235,1,59),(236,1,60),(237,1,61),(238,1,62),(239,1,63),(240,1,64),(241,1,65),(242,1,66),(243,1,67),(244,1,68),(245,1,69),(246,1,70),(247,1,71),(248,1,72),(249,1,73),(250,1,74),(251,1,75),(252,1,76),(253,1,77),(254,1,78),(255,1,79),(256,1,80),(257,1,81),(258,1,82),(259,1,83),(260,1,84),(261,1,85),(262,1,86),(263,1,87),(264,1,88),(265,1,89),(266,1,90),(267,1,91),(268,1,92),(269,1,93),(270,1,94),(271,1,95),(272,1,96),(273,1,97),(274,1,98),(275,1,99),(276,1,100),(277,1,101),(278,1,102),(279,1,103),(280,1,104),(281,1,105),(282,1,106),(283,1,107),(284,1,108),(285,1,109),(286,1,110),(287,1,111),(288,1,112),(289,1,113),(290,1,114),(291,1,115),(292,1,116),(293,1,117),(294,1,118),(295,1,119),(296,1,120),(297,1,121),(298,1,122),(299,1,123),(300,1,124),(301,1,125),(302,1,126),(303,1,127),(304,1,128),(305,1,129),(306,1,130),(307,1,131),(308,1,132),(309,1,133),(310,1,134),(311,1,135),(312,1,136),(313,1,137),(314,1,138),(315,1,139),(316,1,140),(317,1,141),(318,1,142),(319,5,10),(320,5,11),(321,5,12),(322,5,17),(323,5,18),(324,5,25),(325,5,26),(326,5,31),(327,5,32),(328,5,50),(329,5,51),(330,5,55),(331,5,56),(332,5,68),(333,5,69),(334,5,74),(335,5,75),(336,5,80),(337,5,81),(338,5,116),(339,5,117),(340,5,121),(341,5,133),(342,5,134),(343,5,140),(344,5,141),(345,5,142);
/*!40000 ALTER TABLE `user_center_roles_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-03-05 16:48:34
