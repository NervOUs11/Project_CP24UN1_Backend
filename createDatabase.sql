-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema kmutt_database
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema kmutt_database
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `kmutt_database` DEFAULT CHARACTER SET utf8 ;
USE `kmutt_database` ;

-- -----------------------------------------------------
-- Table `kmutt_database`.`faculty`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`faculty` (
  `facultyID` INT NOT NULL AUTO_INCREMENT,
  `facultyName` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`facultyID`),
  UNIQUE INDEX `facultyName_UNIQUE` (`facultyName` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`department`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`department` (
  `departmentID` INT NOT NULL AUTO_INCREMENT,
  `departmentName` VARCHAR(50) NOT NULL,
  `facultyID` INT NOT NULL,
  PRIMARY KEY (`departmentID`, `facultyID`),
  INDEX `fk_department_faculty1_idx` (`facultyID` ASC) VISIBLE,
  UNIQUE INDEX `departmentName_UNIQUE` (`departmentName` ASC) VISIBLE,
  CONSTRAINT `fk_department_faculty1`
    FOREIGN KEY (`facultyID`)
    REFERENCES `kmutt_database`.`faculty` (`facultyID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`student`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`student` (
  `studentID` BIGINT NOT NULL,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `firstName` VARCHAR(50) NOT NULL,
  `lastName` VARCHAR(50) NOT NULL,
  `tel` VARCHAR(10) NOT NULL,
  `alterEmail` VARCHAR(50) NULL,
  `year` INT NOT NULL,
  `departmentID` INT NOT NULL,
  `facultyID` INT NOT NULL,
  `currentGPA` FLOAT NOT NULL,
  `cumulativeGPA` FLOAT NOT NULL,
  PRIMARY KEY (`studentID`, `departmentID`, `facultyID`),
  INDEX `fk_student_department1_idx` (`departmentID` ASC, `facultyID` ASC) VISIBLE,
  CONSTRAINT `fk_student_department1`
    FOREIGN KEY (`departmentID` , `facultyID`)
    REFERENCES `kmutt_database`.`department` (`departmentID` , `facultyID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`role`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`role` (
  `roleID` INT NOT NULL AUTO_INCREMENT,
  `roleName` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`roleID`),
  UNIQUE INDEX `roleName_UNIQUE` (`roleName` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`staff`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`staff` (
  `staffID` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `firstName` VARCHAR(50) NOT NULL,
  `lastName` VARCHAR(50) NOT NULL,
  `tel` VARCHAR(10) NULL,
  `alterEmail` VARCHAR(50) NULL,
  `roleID` INT NOT NULL,
  `departmentID` INT NOT NULL,
  `facultyID` INT NOT NULL,
  PRIMARY KEY (`staffID`, `roleID`, `departmentID`, `facultyID`),
  INDEX `fk_signer_role1_idx` (`roleID` ASC) VISIBLE,
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  INDEX `fk_staff_department1_idx` (`departmentID` ASC, `facultyID` ASC) VISIBLE,
  CONSTRAINT `fk_signer_role1`
    FOREIGN KEY (`roleID`)
    REFERENCES `kmutt_database`.`role` (`roleID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_staff_department1`
    FOREIGN KEY (`departmentID` , `facultyID`)
    REFERENCES `kmutt_database`.`department` (`departmentID` , `facultyID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`form`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`form` (
  `documentID` INT NOT NULL AUTO_INCREMENT,
  `studentID` BIGINT NOT NULL,
  `type` VARCHAR(45) NOT NULL,
  `startTime` DATETIME NOT NULL,
  `endTime` DATETIME NOT NULL,
  `detail` VARCHAR(500) NOT NULL,
  `attachmentFile1` LONGBLOB NULL,
  `attachmentFile2` LONGBLOB NULL,
  `attachmentFile2Name` VARCHAR(50) NULL,
  `createDate` DATETIME NOT NULL,
  `editDate` DATETIME NOT NULL,
  PRIMARY KEY (`documentID`, `studentID`),
  INDEX `fk_documentActivityEvent_student1_idx` (`studentID` ASC) VISIBLE,
  CONSTRAINT `fk_documentActivityEvent_student1`
    FOREIGN KEY (`studentID`)
    REFERENCES `kmutt_database`.`student` (`studentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`progress`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`progress` (
  `progessID` INT NOT NULL AUTO_INCREMENT,
  `staffID` INT NOT NULL,
  `staff_roleID` INT NOT NULL,
  `documentID` INT NOT NULL,
  `studentID` BIGINT NOT NULL,
  `isApprove` VARCHAR(45) NULL,
  `comment` VARCHAR(400) NULL,
  `createDate` DATETIME NOT NULL,
  `editDate` DATETIME NOT NULL,
  PRIMARY KEY (`progessID`, `staffID`, `staff_roleID`, `documentID`, `studentID`),
  INDEX `fk_documentActivityEventProgress_staff1_idx` (`staffID` ASC, `staff_roleID` ASC) VISIBLE,
  INDEX `fk_documentActivityEventProgress_documentActivityEvent1_idx` (`documentID` ASC, `studentID` ASC) VISIBLE,
  CONSTRAINT `fk_documentActivityEventProgress_staff1`
    FOREIGN KEY (`staffID` , `staff_roleID`)
    REFERENCES `kmutt_database`.`staff` (`staffID` , `roleID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_documentActivityEventProgress_documentActivityEvent1`
    FOREIGN KEY (`documentID` , `studentID`)
    REFERENCES `kmutt_database`.`form` (`documentID` , `studentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`student_advisor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`student_advisor` (
  `staffID` INT NOT NULL,
  `studentID` BIGINT NOT NULL,
  PRIMARY KEY (`staffID`, `studentID`),
  INDEX `fk_student_advisors_student1_idx` (`studentID` ASC) VISIBLE,
  CONSTRAINT `fk_student_advisors_staff1`
    FOREIGN KEY (`staffID`)
    REFERENCES `kmutt_database`.`staff` (`staffID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_student_advisors_student1`
    FOREIGN KEY (`studentID`)
    REFERENCES `kmutt_database`.`student` (`studentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
