-- phpMyAdmin SQL Dump
-- version 5.2.0
-- Version du serveur : 8.0.31
-- Version de PHP : 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `db_boat_game`
--

-- --------------------------------------------------------

--
-- Structure de la table `bg_users`
--

DROP TABLE IF EXISTS `bg_users`;
CREATE TABLE IF NOT EXISTS `bg_users` (
  `BG_ID` int NOT NULL AUTO_INCREMENT COMMENT 'User identifiant',
  `BG_ID_DISCORD` int NOT NULL COMMENT 'User identifiant on Discord',
  `BG_BANK_ACCOUNT` int NOT NULL COMMENT 'Money that the user has in their bank account',
  `BG_ON_MYSELF` int NOT NULL COMMENT 'Money that the user has on him',
  PRIMARY KEY (`BG_ID`),
  UNIQUE KEY `idx_discord_id` (`BG_ID_DISCORD`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='User information';


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
