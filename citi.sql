-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Aug 04, 2021 at 03:16 PM
-- Server version: 5.7.23
-- PHP Version: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `citi`
--

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
CREATE TABLE IF NOT EXISTS `account` (
  `userID` varchar(11) NOT NULL,
  `password` tinytext NOT NULL,
  `loyaltyPoints` float NOT NULL DEFAULT '0',
  PRIMARY KEY (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`userID`, `password`, `loyaltyPoints`) VALUES
('cash123', 'admin123', 0),
('cust123', 'admin123', 5900),
('cust234', 'admin123', 1200);

-- --------------------------------------------------------

--
-- Table structure for table `purchase`
--

DROP TABLE IF EXISTS `purchase`;
CREATE TABLE IF NOT EXISTS `purchase` (
  `purchaseID` varchar(6) NOT NULL,
  `userID` tinytext NOT NULL,
  `voucherID` varchar(50) NOT NULL,
  `purchaseDateTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `expiryDate` datetime NOT NULL,
  `points` float NOT NULL,
  `status` tinytext NOT NULL,
  PRIMARY KEY (`purchaseID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `purchase`
--

INSERT INTO `purchase` (`purchaseID`, `userID`, `voucherID`, `purchaseDateTime`, `expiryDate`, `points`, `status`) VALUES
('16AE8F', 'cust123', 'fiveguys20', '2021-08-04 10:20:01', '2022-08-04 18:20:01', 1300, 'Redeemed'),
('2125EB', 'cust234', 'adidas100', '2021-08-04 14:53:31', '2022-08-04 22:53:31', 1000, 'Redeemed'),
('4A19E9', 'cust123', 'adidas20', '2021-08-04 14:47:57', '2022-08-04 22:47:57', 2200, 'Redeemable'),
('63CDF6', 'cust123', 'adidas100', '2021-08-04 14:47:56', '2022-08-04 22:47:56', 1000, 'Redeemed'),
('6F25F6', 'cust123', 'adidas50', '2021-08-04 10:27:49', '2022-08-04 18:27:49', 500, 'Redeemable'),
('7CAFB5', 'cust123', 'adidas20', '2021-08-04 15:12:35', '2022-08-04 23:12:35', 200, 'Redeemable'),
('96E6A6', 'cust123', 'adidas50', '2021-08-04 10:17:58', '2022-08-04 18:17:58', 500, 'Redeemable'),
('9BB433', 'cust123', 'adidas100', '2021-08-04 14:47:57', '2022-08-04 22:47:57', 2000, 'Redeemable'),
('B0DCA1', 'cust234', 'adidas20', '2021-08-04 14:53:31', '2022-08-04 22:53:31', 1200, 'Redeemed'),
('B9D885', 'cust123', 'adidas100', '2021-08-04 10:27:49', '2022-08-04 18:27:49', 1500, 'Redeemable'),
('C20A1D', 'cust123', 'adidas100', '2021-08-04 10:20:01', '2022-08-04 18:20:01', 1000, 'Redeemable'),
('C302A8', 'cust123', 'shakeshack10', '2021-08-04 10:20:01', '2022-08-04 18:20:01', 1100, 'Redeemable'),
('E2A76F', 'cust123', 'fiveguys20', '2021-08-04 15:12:35', '2022-08-04 23:12:35', 400, 'Redeemable');

-- --------------------------------------------------------

--
-- Table structure for table `vouchers`
--

DROP TABLE IF EXISTS `vouchers`;
CREATE TABLE IF NOT EXISTS `vouchers` (
  `voucherID` varchar(50) NOT NULL,
  `voucherName` tinytext NOT NULL,
  `voucherCost` float NOT NULL,
  `voucherAmt` float NOT NULL,
  `brand` tinytext NOT NULL,
  PRIMARY KEY (`voucherID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `vouchers`
--

INSERT INTO `vouchers` (`voucherID`, `voucherName`, `voucherCost`, `voucherAmt`, `brand`) VALUES
('adidas100', '$100 off Adidas', 50, 100, 'Adidas'),
('adidas20', '$20 off Adidas', 10, 20, 'Adidas'),
('adidas50', '$50 off Adidas', 25, 50, 'Adidas'),
('fiveguys10', '$10 off Five-guys', 5, 10, 'Five Guys'),
('fiveguys20', '$20 off Five-guys', 10, 20, 'Five Guys'),
('fiveguys5', '$5 off Five-guys', 3, 5, 'Five Guys'),
('shakeshack10', '$10 off Shake Shack', 5, 10, 'Shake Shack'),
('shakeshack5', '$5 off Shake shack', 3, 5, 'Shake Shack');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
