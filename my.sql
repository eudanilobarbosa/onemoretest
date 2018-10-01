# Tabela do banco de dados MySQL
CREATE TABLE `twitter` (`id` int(11) NOT NULL AUTO_INCREMENT, `tweet_id` varchar(250) DEFAULT NULL, `username` varchar(128) DEFAULT NULL, `tweeted_at` timestamp NULL DEFAULT NULL, `happening` text, PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8;
