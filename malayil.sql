-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Oct 31, 2020 at 07:36 AM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.4.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `malayil`
--

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `customer_id` int(11) NOT NULL,
  `name` varchar(128) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `phone` int(11) DEFAULT NULL,
  `location` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `customers`
--

UPDATE `customers` SET `customer_id` = 1,`name` = 'asd',`email` = 'asd@gmail.com',`phone` = 515,`location` = 'asd' WHERE `customers`.`customer_id` = 1;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` int(11) NOT NULL,
  `name` varchar(128) DEFAULT NULL,
  `barcode` int(11) DEFAULT NULL,
  `price` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `products`
--

UPDATE `products` SET `product_id` = 1,`name` = 'asd',`barcode` = 151,`price` = 153 WHERE `products`.`product_id` = 1;
UPDATE `products` SET `product_id` = 2,`name` = 'asd',`barcode` = 151,`price` = 152 WHERE `products`.`product_id` = 2;

-- --------------------------------------------------------

--
-- Table structure for table `sales`
--

CREATE TABLE `sales` (
  `sales_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `sales`
--

UPDATE `sales` SET `sales_id` = 1,`customer_id` = 1,`product_id` = 1,`user_id` = 1,`timestamp` = '2020-10-30 18:04:57' WHERE `sales`.`sales_id` = 1;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `user_name` varchar(128) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL,
  `name` varchar(128) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `phone_no` varchar(15) DEFAULT NULL,
  `role` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `users`
--

UPDATE `users` SET `user_id` = 1,`user_name` = 'asd',`password` = '$argon2id$v=19$m=102400,t=2,p=8$Yux9DwFAKMX4/x8DQEiJcQ$mGqoi7QrsnFojaVTXdZBcg\r\n\r\n',`name` = 'asd',`email` = 'asd',`phone_no` = '515',`role` = 1 WHERE `users`.`user_id` = 1;
UPDATE `users` SET `user_id` = 2,`user_name` = NULL,`password` = NULL,`name` = 'Raza',`email` = 'raz@gmail.com',`phone_no` = NULL,`role` = NULL WHERE `users`.`user_id` = 2;
UPDATE `users` SET `user_id` = 3,`user_name` = NULL,`password` = NULL,`name` = 'Raza',`email` = 'raz@gmail.com',`phone_no` = NULL,`role` = NULL WHERE `users`.`user_id` = 3;
UPDATE `users` SET `user_id` = 4,`user_name` = 'user',`password` = '$argon2id$v=19$m=102400,t=2,p=8$4nwv5TzH2BtDSKlVCiHEGA$k6XW5CfwsvTCT8sM/am4NQ',`name` = 'user',`email` = 'user@example.com',`phone_no` = '0',`role` = 1 WHERE `users`.`user_id` = 4;
UPDATE `users` SET `user_id` = 5,`user_name` = 'balal',`password` = '$argon2id$v=19$m=102400,t=2,p=8$CYGw1pqTUsrZmxPiXAthjA$2G+0BDMXPKOPb+OSw9duJg',`name` = 'balal',`email` = 'balal@gmail.com',`phone_no` = '9876543210',`role` = 0 WHERE `users`.`user_id` = 5;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customer_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `sales`
--
ALTER TABLE `sales`
  ADD PRIMARY KEY (`sales_id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `sales`
--
ALTER TABLE `sales`
  MODIFY `sales_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `sales`
--
ALTER TABLE `sales`
  ADD CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`),
  ADD CONSTRAINT `sales_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`),
  ADD CONSTRAINT `sales_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
