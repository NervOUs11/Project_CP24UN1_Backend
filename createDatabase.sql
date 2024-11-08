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
  `backupEmail` VARCHAR(50) NULL,
  `signature` LONGBLOB NOT NULL,
  `profileImg` LONGBLOB NULL,
  `roleID` INT NOT NULL,
  PRIMARY KEY (`staffID`, `roleID`),
  INDEX `fk_signer_role1_idx` (`roleID` ASC) VISIBLE,
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  CONSTRAINT `fk_signer_role1`
    FOREIGN KEY (`roleID`)
    REFERENCES `kmutt_database`.`role` (`roleID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


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
  `tel` VARCHAR(10) NULL,
  `backupEmail` VARCHAR(50) NULL,
  `signature` LONGBLOB NOT NULL,
  `profileImg` LONGBLOB NULL,
  `advisorID1` INT NOT NULL,
  `advisorID2` INT NOT NULL,
  `facultyID` INT NOT NULL,
  `departmentID` INT NOT NULL,
  PRIMARY KEY (`studentID`, `advisorID1`, `advisorID2`, `facultyID`, `departmentID`),
  INDEX `fk_student_signer1_idx` (`advisorID1` ASC) VISIBLE,
  INDEX `fk_student_signer2_idx` (`advisorID2` ASC) VISIBLE,
  INDEX `fk_student_department1_idx` (`departmentID` ASC) VISIBLE,
  INDEX `fk_student_faculty1_idx` (`facultyID` ASC) VISIBLE,
  CONSTRAINT `fk_student_signer1`
    FOREIGN KEY (`advisorID1`)
    REFERENCES `kmutt_database`.`staff` (`staffID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_student_signer2`
    FOREIGN KEY (`advisorID2`)
    REFERENCES `kmutt_database`.`staff` (`staffID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_student_department1`
    FOREIGN KEY (`departmentID`)
    REFERENCES `kmutt_database`.`department` (`departmentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_student_faculty1`
    FOREIGN KEY (`facultyID`)
    REFERENCES `kmutt_database`.`faculty` (`facultyID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`documentActivityEvent`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`documentActivityEvent` (
  `documentActivityEventID` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(100) NOT NULL,
  `to` VARCHAR(50) NOT NULL,
  `senderFaculty` VARCHAR(50) NOT NULL,
  `description` VARCHAR(1000) NOT NULL,
  `amount` DECIMAL NOT NULL,
  `academicAndSkillDevelopment` INT NULL,
  `sportsAndHealth` INT NULL,
  `volunteer` INT NULL,
  `artAndCulturalPreservation` INT NULL,
  `characterDevelopment` INT NULL,
  `universityCommitment` INT NULL,
  `location` VARCHAR(100) NOT NULL,
  `startDate` DATETIME NOT NULL,
  `endDate` DATETIME NOT NULL,
  `studentID` BIGINT NOT NULL,
  `documentFilePDF` LONGBLOB NULL,
  `createDate` DATETIME NOT NULL,
  `editDate` DATETIME NOT NULL,
  PRIMARY KEY (`documentActivityEventID`, `studentID`),
  INDEX `fk_documentActivityEvent_student1_idx` (`studentID` ASC) VISIBLE,
  CONSTRAINT `fk_documentActivityEvent_student1`
    FOREIGN KEY (`studentID`)
    REFERENCES `kmutt_database`.`student` (`studentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`documentAbsence`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`documentAbsence` (
  `documentAbsenceID` INT NOT NULL AUTO_INCREMENT,
  `studentFirstName` VARCHAR(50) NOT NULL,
  `studentLastName` VARCHAR(50) NOT NULL,
  `studentFaculty` VARCHAR(50) NOT NULL,
  `studentDepartment` VARCHAR(50) NOT NULL,
  `studentGpax` VARCHAR(50) NOT NULL,
  `advisorName1` VARCHAR(50) NOT NULL,
  `advisorName2` VARCHAR(50) NULL,
  `studentTel` VARCHAR(10) NOT NULL,
  `studentEmail` VARCHAR(50) NOT NULL,
  `description` VARCHAR(300) NOT NULL,
  `subject` VARCHAR(100) NOT NULL,
  `startDate` DATETIME NOT NULL,
  `endDate` DATETIME NOT NULL,
  `evidenceFile` LONGBLOB NOT NULL,
  `otherEvidenceFile` LONGBLOB NULL,
  `studentID` BIGINT NOT NULL,
  `documentFilePDF` LONGBLOB NULL,
  `createDate` DATETIME NOT NULL,
  `editDate` DATETIME NOT NULL,
  PRIMARY KEY (`documentAbsenceID`, `studentID`),
  INDEX `fk_documentAbsence_student1_idx` (`studentID` ASC) VISIBLE,
  CONSTRAINT `fk_documentAbsence_student1`
    FOREIGN KEY (`studentID`)
    REFERENCES `kmutt_database`.`student` (`studentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`documentAbsenceProgress`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`documentAbsenceProgress` (
  `progressID` INT NOT NULL,
  `staffID` INT NOT NULL,
  `staff_roleID` INT NOT NULL,
  `documentAbsenceID` INT NOT NULL,
  `studentID` BIGINT NOT NULL,
  `isApprove` VARCHAR(45) NULL,
  `comment` VARCHAR(400) NULL,
  PRIMARY KEY (`progressID`, `staffID`, `staff_roleID`, `documentAbsenceID`, `studentID`),
  INDEX `fk_documentAbsenceProgress_staff1_idx` (`staffID` ASC, `staff_roleID` ASC) VISIBLE,
  INDEX `fk_documentAbsenceProgress_documentAbsence1_idx` (`documentAbsenceID` ASC, `studentID` ASC) VISIBLE,
  CONSTRAINT `fk_documentAbsenceProgress_staff1`
    FOREIGN KEY (`staffID` , `staff_roleID`)
    REFERENCES `kmutt_database`.`staff` (`staffID` , `roleID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_documentAbsenceProgress_documentAbsence1`
    FOREIGN KEY (`documentAbsenceID` , `studentID`)
    REFERENCES `kmutt_database`.`documentAbsence` (`documentAbsenceID` , `studentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`documentActivityEventProgress`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`documentActivityEventProgress` (
  `progessID` INT NOT NULL,
  `staffID` INT NOT NULL,
  `staff_roleID` INT NOT NULL,
  `documentActivityEventID` INT NOT NULL,
  `studentID` BIGINT NOT NULL,
  `isApprove` VARCHAR(45) NULL,
  `comment` VARCHAR(400) NULL,
  PRIMARY KEY (`progessID`, `staffID`, `staff_roleID`, `documentActivityEventID`, `studentID`),
  INDEX `fk_documentActivityEventProgress_staff1_idx` (`staffID` ASC, `staff_roleID` ASC) VISIBLE,
  INDEX `fk_documentActivityEventProgress_documentActivityEvent1_idx` (`documentActivityEventID` ASC, `studentID` ASC) VISIBLE,
  CONSTRAINT `fk_documentActivityEventProgress_staff1`
    FOREIGN KEY (`staffID` , `staff_roleID`)
    REFERENCES `kmutt_database`.`staff` (`staffID` , `roleID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_documentActivityEventProgress_documentActivityEvent1`
    FOREIGN KEY (`documentActivityEventID` , `studentID`)
    REFERENCES `kmutt_database`.`documentActivityEvent` (`documentActivityEventID` , `studentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
