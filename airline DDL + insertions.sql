-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 19, 2022 at 11:23 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `airline`
--
CREATE DATABASE IF NOT EXISTS `airline` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `airline`;

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

CREATE TABLE `airline` (
  `airline_id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`airline_id`, `name`) VALUES
(1, 'American Airlines'),
(2, 'Avelo Airlines'),
(3, 'Delta Airlines');

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

CREATE TABLE `airplane` (
  `plane_id` int(11) NOT NULL,
  `model` varchar(20) NOT NULL,
  `airline_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`plane_id`, `model`, `airline_id`) VALUES
(1, 'Airbus-A319', 1),
(2, 'Boeing 737-700', 1),
(3, 'Boeing-787-8', 2),
(4, 'Boeing 737-800', 2),
(5, 'Bombardier CRJ-200', 3);

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `airport_code` int(11) NOT NULL,
  `country` varchar(3) NOT NULL,
  `city` varchar(20) NOT NULL,
  `name` varchar(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`airport_code`, `country`, `city`, `name`) VALUES
(1, 'USA', 'Los Angeles', 'LAX'),
(2, 'USA', 'Manhattan', 'MHK'),
(3, 'USA', 'Owensboro', 'OWB'),
(4, 'UAE', 'Abu Dhabi', 'AUH'),
(5, 'UAE', 'Dubai', 'DXB');

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

CREATE TABLE `booking` (
  `id` int(11) NOT NULL,
  `booking_time` datetime NOT NULL,
  `seats` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `flight_number` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `booking`
--

INSERT INTO `booking` (`id`, `booking_time`, `seats`, `customer_id`, `flight_number`) VALUES
(1, '2022-04-17 09:41:13', 1, 1, 1),
(2, '2022-04-17 08:41:50', 2, 2, 1),
(3, '2022-04-17 08:30:00', 2, 3, 1),
(4, '2022-04-17 07:10:33', 1, 2, 2),
(5, '2022-04-17 07:20:13', 2, 2, 3),
(6, '2022-04-17 14:47:13', 1, 3, 4);

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `id` int(11) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(60) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`id`, `email`, `password`, `first_name`, `last_name`) VALUES
(1, 'customer1@gmail.com', '$2b$12$AgUcx3XkspkrRHtgnDJ8vOfRYvSmbKqmsloA580nS5KLYquSX/MEK', 'Customer', 'Name 1'),
(2, 'customer2@gmail.com', '$2b$12$d..iCk1aeE9op3AfbH013OWkiVPBxjMqO1.eF6vP8y5UNz0HBh2Pa', 'Customer', 'Name 2'),
(3, 'customer3@gmail.com', '$2b$12$WpYV7iosp8T0lt5D2820JelUzujo3KchHRsQfx20mLkScOsco34l.', 'Customer', 'Name 3');

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `flight_number` int(11) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `destination` varchar(20) NOT NULL,
  `source` varchar(20) NOT NULL,
  `capacity` int(11) NOT NULL,
  `status` varchar(20) NOT NULL,
  `plane_id` int(11) NOT NULL,
  `airport_code_destination` int(11) NOT NULL,
  `airport_code_source` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`flight_number`, `start_time`, `end_time`, `destination`, `source`, `capacity`, `status`, `plane_id`, `airport_code_destination`, `airport_code_source`) VALUES
(1, '2022-04-17 10:00:00', '2022-04-17 13:00:00', 'Los Angeles', 'Manhattan', 400, 'On time', 1, 2, 1),
(2, '2022-04-17 15:00:00', '2022-04-17 18:00:00', 'Los Angeles', 'Dubai', 100, 'On time', 2, 5, 1),
(3, '2022-04-18 15:00:00', '2022-04-18 18:00:00', 'Owensboro', 'Manhattan', 150, 'On time', 3, 3, 2),
(4, '2022-04-18 15:00:00', '2022-04-18 18:00:00', 'Abu Dhabi', 'Owensboro', 700, 'On time', 4, 4, 3),
(5, '2022-04-18 07:00:00', '2022-04-18 09:00:00', 'Manhattan', 'Los Angeles', 200, 'Delayed', 5, 2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

CREATE TABLE `staff` (
  `id` int(11) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(60) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `staff`
--

INSERT INTO `staff` (`id`, `email`, `password`, `first_name`, `last_name`) VALUES
(1, 'staff1@gmail.com', '$2b$12$SH3en56boUlAWpK8Gik2U.cIP3tnBuar981JaWAaE1Qc2elXL/dvW', 'Staff', 'Name 1'),
(2, 'staff2@gmail.com', '$2b$12$4yZX3H20ZiRut5Jf2mGIy.PP5uWLBW4XvLEd8dIcTXOuZK/4t6l9u', 'Staff', 'Name 2');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `airline`
--
ALTER TABLE `airline`
  ADD PRIMARY KEY (`airline_id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `airplane`
--
ALTER TABLE `airplane`
  ADD PRIMARY KEY (`plane_id`),
  ADD UNIQUE KEY `model` (`model`),
  ADD KEY `airline_id` (`airline_id`);

--
-- Indexes for table `airport`
--
ALTER TABLE `airport`
  ADD PRIMARY KEY (`airport_code`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `customer_id` (`customer_id`,`flight_number`),
  ADD KEY `flight_number` (`flight_number`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`flight_number`),
  ADD KEY `plane_id` (`plane_id`),
  ADD KEY `airport_code_destination` (`airport_code_destination`),
  ADD KEY `airport_code_source` (`airport_code_source`);

--
-- Indexes for table `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `airline`
--
ALTER TABLE `airline`
  MODIFY `airline_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `airplane`
--
ALTER TABLE `airplane`
  MODIFY `plane_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `airport`
--
ALTER TABLE `airport`
  MODIFY `airport_code` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `booking`
--
ALTER TABLE `booking`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `flight`
--
ALTER TABLE `flight`
  MODIFY `flight_number` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `staff`
--
ALTER TABLE `staff`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`airline_id`) REFERENCES `airline` (`airline_id`);

--
-- Constraints for table `booking`
--
ALTER TABLE `booking`
  ADD CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
  ADD CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`flight_number`) REFERENCES `flight` (`flight_number`);

--
-- Constraints for table `flight`
--
ALTER TABLE `flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`plane_id`) REFERENCES `airplane` (`plane_id`),
  ADD CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`airport_code_destination`) REFERENCES `airport` (`airport_code`),
  ADD CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`airport_code_source`) REFERENCES `airport` (`airport_code`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
