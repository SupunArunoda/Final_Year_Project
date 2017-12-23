-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Nov 01, 2017 at 02:01 PM
-- Server version: 5.6.17
-- PHP Version: 5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `adist`
--

-- --------------------------------------------------------

--
-- Table structure for table `preprocess_file`
--

CREATE TABLE IF NOT EXISTS `preprocess_file` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `input_filename` varchar(255) NOT NULL,
  `uploaded_time` datetime NOT NULL,
  `last_process_start` datetime DEFAULT NULL,
  `last_process_end` datetime DEFAULT NULL,
  `output_filename` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=95 ;

--
-- Dumping data for table `preprocess_file`
--

INSERT INTO `preprocess_file` (`id`, `input_filename`, `uploaded_time`, `last_process_start`, `last_process_end`, `output_filename`) VALUES
(37, './app/data/data.csv', '2017-08-28 10:25:07', '2017-08-28 10:25:07', '2017-08-28 10:26:20', './app/output/ex_type_static_normalize.csv'),
(38, './app/data/data.csv', '2017-08-28 10:49:37', '2017-08-28 10:49:37', '2017-08-28 10:50:53', './app/output/ex_type_static_normalize.csv'),
(39, './app/data/data.csv', '2017-08-28 10:53:32', '2017-08-28 10:53:32', '2017-08-28 10:54:46', './app/output/ex_type_static_normalize.csv'),
(40, './app/data/data.csv', '2017-08-28 10:57:15', '2017-08-28 10:57:15', '2017-08-28 10:58:32', './app/output/ex_type_static_normalize.csv'),
(41, './app/data/data.csv', '2017-08-28 11:12:11', '2017-08-28 11:12:11', '2017-08-28 11:13:29', './app/output/ex_type_static_normalize.csv'),
(42, './app/data/data.csv', '2017-08-28 11:15:42', '2017-08-28 11:15:42', '2017-08-28 11:16:56', './app/output/ex_type_static_normalize.csv'),
(43, './app/data/data.csv', '2017-08-28 11:33:13', '2017-08-28 11:33:13', '2017-08-28 11:34:25', './app/output/ex_type_static_normalize.csv'),
(44, './app/data/data.csv', '2017-08-29 04:00:21', '2017-08-29 04:00:21', '2017-08-29 04:01:42', './app/output/ex_type_static_normalize.csv'),
(45, './app/data/data.csv', '2017-08-29 08:27:42', '2017-08-29 08:27:42', '2017-08-29 08:29:05', './app/output/ex_type_static_normalize.csv'),
(46, './app/data/data.csv', '2017-08-29 08:36:33', '2017-08-29 08:36:33', '2017-08-29 08:38:01', './app/output/ex_type_static_normalize.csv'),
(47, './app/data/data.csv', '2017-08-29 08:41:11', '2017-08-29 08:41:11', '2017-08-29 08:42:33', './app/output/ex_type_static_normalize.csv'),
(48, './app/data/data.csv', '2017-08-29 08:44:29', '2017-08-29 08:44:29', '2017-08-29 08:46:01', './app/output/ex_type_static_normalize.csv'),
(49, './app/data/data.csv', '2017-08-29 08:54:24', '2017-08-29 08:54:24', '2017-08-29 08:55:46', './app/output/ex_type_static_normalize.csv'),
(50, './app/data/data.csv', '2017-08-29 08:57:25', '2017-08-29 08:57:25', '2017-08-29 08:58:42', './app/output/ex_type_static_normalize.csv'),
(51, './app/data/data.csv', '2017-08-29 09:00:24', '2017-08-29 09:00:24', '2017-08-29 09:01:47', './app/output/ex_type_static_normalize.csv'),
(52, './app/data/data.csv', '2017-08-29 09:04:01', '2017-08-29 09:04:01', '2017-08-29 09:05:17', './app/output/ex_type_static_normalize.csv'),
(53, './app/data/data.csv', '2017-09-02 12:51:15', '2017-09-02 12:51:15', '2017-09-02 12:52:58', './app/output/ex_type_static_normalize.csv'),
(54, './app/data/data.csv', '2017-09-02 15:55:50', '2017-09-02 15:55:50', '2017-09-02 15:57:19', './app/output/ex_type_static_normalize.csv'),
(55, './app/data/data.csv', '2017-09-02 17:07:39', '2017-09-02 17:07:39', '2017-09-02 17:09:08', './app/output/ex_type_static_normalize.csv'),
(56, './app/data/data.csv', '2017-09-02 17:15:24', '2017-09-02 17:15:24', '2017-09-02 17:17:01', './app/output/ex_type_static_normalize.csv'),
(57, './app/data/data.csv', '2017-09-02 17:19:55', '2017-09-02 17:19:55', '2017-09-02 17:21:12', './app/output/ex_type_static_normalize.csv'),
(58, './app/data/data.csv', '2017-09-02 17:24:34', '2017-09-02 17:24:34', '2017-09-02 17:26:03', './app/output/ex_type_static_normalize.csv'),
(59, './app/data/data.csv', '2017-09-02 17:26:35', '2017-09-02 17:26:35', '2017-09-02 17:28:05', './app/output/ex_type_static_normalize.csv'),
(60, './app/data/data.csv', '2017-09-02 17:44:40', '2017-09-02 17:44:40', '2017-09-02 17:46:12', './app/output/ex_type_static_normalize.csv'),
(61, './app/data/data.csv', '2017-09-02 17:47:56', '2017-09-02 17:47:56', '2017-09-02 17:49:27', './app/output/ex_type_static_normalize.csv'),
(62, './app/data/data.csv', '2017-09-02 18:12:04', '2017-09-02 18:12:04', '2017-09-02 18:13:33', './app/output/ex_type_static_normalize.csv'),
(63, './app/data/data.csv', '2017-09-02 18:15:54', '2017-09-02 18:15:54', '2017-09-02 18:17:10', './app/output/ex_type_static_normalize.csv'),
(64, './app/data/data.csv', '2017-09-02 18:22:12', '2017-09-02 18:22:12', '2017-09-02 18:23:32', './app/output/ex_type_static_normalize.csv'),
(65, './app/data/data.csv', '2017-09-02 18:35:22', '2017-09-02 18:35:22', '2017-09-02 18:36:33', './app/output/ex_type_static_normalize.csv'),
(66, './app/data/data.csv', '2017-09-03 06:03:37', '2017-09-03 06:03:37', '2017-09-03 06:04:58', './app/output/ex_type_static_normalize.csv'),
(67, './app/data/data.csv', '2017-09-04 15:16:05', '2017-09-04 15:16:05', '2017-09-04 15:17:29', './app/output/ex_type_static_normalize.csv'),
(68, './app/data/data.csv', '2017-09-04 15:22:05', '2017-09-04 15:22:05', '2017-09-04 15:23:18', './app/output/ex_type_static_normalize.csv'),
(69, './app/data/data.csv', '2017-09-04 15:59:00', '2017-09-04 15:59:00', '2017-09-04 16:00:19', './app/output/ex_type_static_normalize.csv'),
(70, './app/data/data.csv', '2017-09-04 16:13:10', '2017-09-04 16:13:10', '2017-09-04 16:14:23', './app/output/ex_type_static_normalize.csv'),
(71, './app/data/data.csv', '2017-09-09 09:33:44', '2017-09-09 09:33:44', '2017-09-09 09:35:03', './app/output/ex_type_static_normalize.csv'),
(72, './app/data/data.csv', '2017-09-09 09:40:00', '2017-09-09 09:40:00', '2017-09-09 09:41:33', './app/output/ex_type_static_normalize.csv'),
(73, './app/data/data.csv', '2017-09-09 09:53:15', '2017-09-09 09:53:15', '2017-09-09 09:54:44', './app/output/ex_type_static_normalize.csv'),
(74, './app/data/data.csv', '2017-09-09 09:56:55', '2017-09-09 09:56:55', '2017-09-09 09:58:13', './app/output/ex_type_static_normalize.csv'),
(75, './app/data/data.csv', '2017-09-09 10:02:06', '2017-09-09 10:02:06', '2017-09-09 10:03:24', './app/output/ex_type_static_normalize.csv'),
(76, './app/data/data.csv', '2017-09-09 10:05:34', '2017-09-09 10:05:34', '2017-09-09 10:06:47', './app/output/ex_type_static_normalize.csv'),
(77, './app/data/data.csv', '2017-09-09 10:10:59', '2017-09-09 10:10:59', '2017-09-09 10:12:11', './app/output/ex_type_static_normalize.csv'),
(78, './app/data/data.csv', '2017-09-09 10:13:37', '2017-09-09 10:13:37', '2017-09-09 10:14:50', './app/output/ex_type_static_normalize.csv'),
(79, './app/data/data.csv', '2017-09-09 10:28:06', '2017-09-09 10:28:06', '2017-09-09 10:29:28', './app/output/ex_type_static_normalize.csv'),
(80, './app/data/data.csv', '2017-09-09 10:49:16', '2017-09-09 10:49:16', '2017-09-09 10:50:39', './app/output/ex_type_static_normalize.csv'),
(81, './app/data/data.csv', '2017-09-09 10:54:31', '2017-09-09 10:54:31', '2017-09-09 10:56:03', './app/output/ex_type_static_normalize.csv'),
(82, './app/data/data.csv', '2017-09-09 11:06:55', '2017-09-09 11:06:55', '2017-09-09 11:08:21', './app/output/ex_type_static_normalize.csv'),
(83, './app/data/data.csv', '2017-09-09 12:05:16', '2017-09-09 12:05:16', '2017-09-09 12:06:55', './app/output/ex_type_static_normalize.csv'),
(84, './app/data/data.csv', '2017-09-09 14:53:32', '2017-09-09 14:53:32', '2017-09-09 14:54:46', './app/output/ex_type_static_normalize.csv'),
(85, './app/data/data.csv', '2017-09-12 20:43:43', '2017-09-12 20:43:43', '2017-09-12 20:44:53', './app/output/ex_type_static_normalize.csv'),
(86, './app/data/data.csv', '2017-09-12 20:55:16', '2017-09-12 20:55:16', '2017-09-12 20:56:34', './app/output/ex_type_static_normalize.csv'),
(87, './app/data/data.csv', '2017-09-12 20:58:25', '2017-09-12 20:58:25', '2017-09-12 20:59:33', './app/output/ex_type_static_normalize.csv'),
(88, './app/data/data.csv', '2017-09-13 05:24:29', '2017-09-13 05:24:29', '2017-09-13 05:25:57', './app/output/ex_type_static_normalize.csv'),
(89, './app/data/data.csv', '2017-09-13 05:34:17', '2017-09-13 05:34:17', '2017-09-13 05:35:34', './app/output/ex_type_static_normalize.csv'),
(90, './app/data/data.csv', '2017-09-27 11:27:10', '2017-09-27 11:27:10', '2017-09-27 11:28:57', './app/output/ex_type_static_normalize.csv'),
(91, './app/data/data.csv', '2017-09-27 11:35:48', '2017-09-27 11:35:48', '2017-09-27 11:37:00', './app/output/ex_type_static_normalize.csv'),
(92, './app/data/data.csv', '2017-09-27 11:39:36', '2017-09-27 11:39:36', '2017-09-27 11:40:49', './app/output/ex_type_static_normalize.csv'),
(93, './app/data/data.csv', '2017-09-27 11:43:32', '2017-09-27 11:43:32', '2017-09-27 11:45:03', './app/output/ex_type_static_normalize.csv'),
(94, './app/data/data.csv', '2017-09-29 04:07:58', '2017-09-29 04:07:58', '2017-09-29 04:09:32', './app/output/ex_type_static_normalize.csv');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
