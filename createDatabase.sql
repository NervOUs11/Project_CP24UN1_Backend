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
  `roleName` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`roleID`),
  UNIQUE INDEX `roleName_UNIQUE` (`roleName` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`faculty`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`faculty` (
  `facultyID` INT NOT NULL AUTO_INCREMENT,
  `facultyName` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`facultyID`),
  UNIQUE INDEX `facultycol_UNIQUE` (`facultyName` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`department`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`department` (
  `departmentID` INT NOT NULL AUTO_INCREMENT,
  `departmentName` VARCHAR(50) NOT NULL,
  `facultyID` INT NOT NULL,
  PRIMARY KEY (`departmentID`, `facultyID`),
  UNIQUE INDEX `departmentName_UNIQUE` (`departmentName` ASC) VISIBLE,
  INDEX `fk_department_faculty2_idx` (`facultyID` ASC) VISIBLE,
  CONSTRAINT `fk_department_faculty2`
    FOREIGN KEY (`facultyID`)
    REFERENCES `kmutt_database`.`faculty` (`facultyID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`club`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`club` (
  `clubID` INT NOT NULL AUTO_INCREMENT,
  `clubName` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`clubID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`staff`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`staff` (
  `staffID` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL,
  `firstName` VARCHAR(50) NOT NULL,
  `lastName` VARCHAR(50) NOT NULL,
  `tel` VARCHAR(10) NULL,
  `email` VARCHAR(50) NULL,
  `roleID` INT NOT NULL,
  `departmentID` INT NOT NULL,
  `facultyID` INT NOT NULL,
  `clubID` INT NULL,
  PRIMARY KEY (`staffID`, `roleID`, `departmentID`, `facultyID`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  INDEX `fk_staff_role1_idx` (`roleID` ASC) VISIBLE,
  INDEX `fk_staff_department2_idx` (`departmentID` ASC, `facultyID` ASC) VISIBLE,
  INDEX `fk_staff_table11_idx` (`clubID` ASC) VISIBLE,
  CONSTRAINT `fk_staff_role1`
    FOREIGN KEY (`roleID`)
    REFERENCES `kmutt_database`.`role` (`roleID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_staff_department2`
    FOREIGN KEY (`departmentID` , `facultyID`)
    REFERENCES `kmutt_database`.`department` (`departmentID` , `facultyID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_staff_table11`
    FOREIGN KEY (`clubID`)
    REFERENCES `kmutt_database`.`club` (`clubID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`student`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`student` (
  `studentID` BIGINT NOT NULL,
  `username` VARCHAR(50) NOT NULL,
  `firstName` VARCHAR(50) NOT NULL,
  `lastName` VARCHAR(50) NOT NULL,
  `tel` VARCHAR(10) NULL,
  `email` VARCHAR(50) NULL,
  `year` INT NOT NULL,
  `departmentID` INT NOT NULL,
  `facultyID` INT NOT NULL,
  `currentGPA` FLOAT NOT NULL,
  `cumulativeGPA` FLOAT NOT NULL,
  `clubID` INT NULL,
  PRIMARY KEY (`studentID`, `departmentID`, `facultyID`),
  INDEX `fk_student_department2_idx` (`departmentID` ASC, `facultyID` ASC) VISIBLE,
  INDEX `fk_student_table11_idx` (`clubID` ASC) VISIBLE,
  CONSTRAINT `fk_student_department2`
    FOREIGN KEY (`departmentID` , `facultyID`)
    REFERENCES `kmutt_database`.`department` (`departmentID` , `facultyID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_student_table11`
    FOREIGN KEY (`clubID`)
    REFERENCES `kmutt_database`.`club` (`clubID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`absenceDocument`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`absenceDocument` (
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
  INDEX `fk_absenceDocument_student1_idx` (`studentID` ASC) VISIBLE,
  CONSTRAINT `fk_absenceDocument_student1`
    FOREIGN KEY (`studentID`)
    REFERENCES `kmutt_database`.`student` (`studentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`activityDocument`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`activityDocument` (
  `documentID` INT NOT NULL,
  `studentID` BIGINT NOT NULL,
  `type` VARCHAR(45) NOT NULL,
  `startTime` DATETIME NOT NULL,
  `endTime` DATETIME NOT NULL,
  `createDate` DATETIME NOT NULL,
  `editDate` DATETIME NOT NULL,
  `code` VARCHAR(50) NOT NULL,
  `departmentName` VARCHAR(50) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  `location` VARCHAR(100) NOT NULL,
  `propose` VARCHAR(2000) NOT NULL,
  `payment` FLOAT NOT NULL,
  `staffID` INT NOT NULL,
  `sustainabilityDetail` VARCHAR(2000) NOT NULL,
  `sustainabilityPropose` VARCHAR(2000) NOT NULL,
  `activityCharacteristic` VARCHAR(2000) NOT NULL,
  `codeOfHonor` VARCHAR(2000) NOT NULL,
  `prepareStart` DATETIME NOT NULL,
  `prepareEnd` DATETIME NOT NULL,
  `prepareFile` LONGBLOB NOT NULL,
  `evaluationFile` LONGBLOB NOT NULL,
  `budgetDetails` LONGBLOB NOT NULL,
  `scheduleDetail` LONGBLOB NOT NULL,
  PRIMARY KEY (`documentID`, `studentID`, `staffID`),
  INDEX `fk_activityDocument_student1_idx` (`studentID` ASC) VISIBLE,
  INDEX `fk_activityDocument_staff1_idx` (`staffID` ASC) VISIBLE,
  CONSTRAINT `fk_activityDocument_student1`
    FOREIGN KEY (`studentID`)
    REFERENCES `kmutt_database`.`student` (`studentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_activityDocument_staff1`
    FOREIGN KEY (`staffID`)
    REFERENCES `kmutt_database`.`staff` (`staffID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`absenceProgress`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`absenceProgress` (
  `progressID` INT NOT NULL AUTO_INCREMENT,
  `step` INT NOT NULL,
  `staffID` INT NOT NULL,
  `staff_roleID` INT NOT NULL,
  `documentID` INT NOT NULL,
  `studentID` BIGINT NOT NULL,
  `status` VARCHAR(45) NULL,
  `comment` VARCHAR(400) NULL,
  `createDate` DATETIME NOT NULL,
  `editDate` DATETIME NOT NULL,
  `approvedAt` DATETIME NULL,
  PRIMARY KEY (`progressID`, `staffID`, `staff_roleID`, `documentID`, `studentID`),
  INDEX `fk_progress_absenceDocument1_idx` (`documentID` ASC, `studentID` ASC) VISIBLE,
  INDEX `fk_progress_staff1_idx` (`staffID` ASC, `staff_roleID` ASC) VISIBLE,
  CONSTRAINT `fk_progress_absenceDocument1`
    FOREIGN KEY (`documentID` , `studentID`)
    REFERENCES `kmutt_database`.`absenceDocument` (`documentID` , `studentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_progress_staff1`
    FOREIGN KEY (`staffID` , `staff_roleID`)
    REFERENCES `kmutt_database`.`staff` (`staffID` , `roleID`)
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
  INDEX `fk_staff_has_student_student1_idx` (`studentID` ASC) VISIBLE,
  INDEX `fk_staff_has_student_staff1_idx` (`staffID` ASC) VISIBLE,
  CONSTRAINT `fk_staff_has_student_staff1`
    FOREIGN KEY (`staffID`)
    REFERENCES `kmutt_database`.`staff` (`staffID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_staff_has_student_student1`
    FOREIGN KEY (`studentID`)
    REFERENCES `kmutt_database`.`student` (`studentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`activityProgress`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`activityProgress` (
  `progressID` INT NOT NULL AUTO_INCREMENT,
  `step` INT NOT NULL,
  `staffID` INT NOT NULL,
  `staff_roleID` INT NOT NULL,
  `documentID` INT NOT NULL,
  `studentID` BIGINT NOT NULL,
  `status` VARCHAR(45) NULL,
  `comment` VARCHAR(400) NULL,
  `createDate` DATETIME NOT NULL,
  `editDate` DATETIME NOT NULL,
  `approvedAt` DATETIME NULL,
  PRIMARY KEY (`progressID`, `staffID`, `staff_roleID`, `documentID`, `studentID`),
  INDEX `fk_activityProgress_staff1_idx` (`staffID` ASC, `staff_roleID` ASC) VISIBLE,
  INDEX `fk_activityProgress_activityDocument1_idx` (`documentID` ASC, `studentID` ASC) VISIBLE,
  CONSTRAINT `fk_activityProgress_staff1`
    FOREIGN KEY (`staffID` , `staff_roleID`)
    REFERENCES `kmutt_database`.`staff` (`staffID` , `roleID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_activityProgress_activityDocument1`
    FOREIGN KEY (`documentID` , `studentID`)
    REFERENCES `kmutt_database`.`activityDocument` (`documentID` , `studentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`goal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`goal` (
  `goalID` INT NOT NULL AUTO_INCREMENT,
  `goalName` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`goalID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`student_commitee`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`student_commitee` (
  `studentID` BIGINT NOT NULL,
  `documentID` INT NOT NULL,
  `position` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`studentID`, `documentID`),
  INDEX `fk_student_has_activityDocument_activityDocument1_idx` (`documentID` ASC) VISIBLE,
  INDEX `fk_student_has_activityDocument_student1_idx` (`studentID` ASC) VISIBLE,
  CONSTRAINT `fk_student_has_activityDocument_student1`
    FOREIGN KEY (`studentID`)
    REFERENCES `kmutt_database`.`student` (`studentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_student_has_activityDocument_activityDocument1`
    FOREIGN KEY (`documentID`)
    REFERENCES `kmutt_database`.`activityDocument` (`documentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`studentQF`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`studentQF` (
  `Student_QF_ID` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`Student_QF_ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`entrepreneurial`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`entrepreneurial` (
  `entrepreneurialID` INT NOT NULL AUTO_INCREMENT,
  `entrepreneurialName` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`entrepreneurialID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`participant`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`participant` (
  `participantID` INT NOT NULL AUTO_INCREMENT,
  `participantName` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`participantID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`evaluation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`evaluation` (
  `evaluationID` INT NOT NULL AUTO_INCREMENT,
  `evaluationName` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`evaluationID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`document_participant`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`document_participant` (
  `documentID` INT NOT NULL,
  `participantID` INT NOT NULL,
  `count` INT NOT NULL,
  PRIMARY KEY (`documentID`, `participantID`),
  INDEX `fk_activityDocument_has_participant_participant1_idx` (`participantID` ASC) VISIBLE,
  INDEX `fk_activityDocument_has_participant_activityDocument1_idx` (`documentID` ASC) VISIBLE,
  CONSTRAINT `fk_activityDocument_has_participant_activityDocument1`
    FOREIGN KEY (`documentID`)
    REFERENCES `kmutt_database`.`activityDocument` (`documentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_activityDocument_has_participant_participant1`
    FOREIGN KEY (`participantID`)
    REFERENCES `kmutt_database`.`participant` (`participantID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`document_studentQF`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`document_studentQF` (
  `documentID` INT NOT NULL,
  `student_QF_ID` INT NOT NULL,
  PRIMARY KEY (`documentID`, `student_QF_ID`),
  INDEX `fk_activityDocument_has_studentQF_studentQF1_idx` (`student_QF_ID` ASC) VISIBLE,
  INDEX `fk_activityDocument_has_studentQF_activityDocument1_idx` (`documentID` ASC) VISIBLE,
  CONSTRAINT `fk_activityDocument_has_studentQF_activityDocument1`
    FOREIGN KEY (`documentID`)
    REFERENCES `kmutt_database`.`activityDocument` (`documentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_activityDocument_has_studentQF_studentQF1`
    FOREIGN KEY (`student_QF_ID`)
    REFERENCES `kmutt_database`.`studentQF` (`Student_QF_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`document_entrepreneurial`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`document_entrepreneurial` (
  `documentID` INT NOT NULL,
  `entrepreneurialID` INT NOT NULL,
  PRIMARY KEY (`documentID`, `entrepreneurialID`),
  INDEX `fk_activityDocument_has_entrepreneurial_entrepreneurial1_idx` (`entrepreneurialID` ASC) VISIBLE,
  INDEX `fk_activityDocument_has_entrepreneurial_activityDocument1_idx` (`documentID` ASC) VISIBLE,
  CONSTRAINT `fk_activityDocument_has_entrepreneurial_activityDocument1`
    FOREIGN KEY (`documentID`)
    REFERENCES `kmutt_database`.`activityDocument` (`documentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_activityDocument_has_entrepreneurial_entrepreneurial1`
    FOREIGN KEY (`entrepreneurialID`)
    REFERENCES `kmutt_database`.`entrepreneurial` (`entrepreneurialID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`document_evaluation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`document_evaluation` (
  `documentID` INT NOT NULL,
  `evaluationID` INT NOT NULL,
  `otherEvaluationName` VARCHAR(50) NULL,
  PRIMARY KEY (`documentID`, `evaluationID`),
  INDEX `fk_activityDocument_has_evaluation_evaluation1_idx` (`evaluationID` ASC) VISIBLE,
  INDEX `fk_activityDocument_has_evaluation_activityDocument1_idx` (`documentID` ASC) VISIBLE,
  CONSTRAINT `fk_activityDocument_has_evaluation_activityDocument1`
    FOREIGN KEY (`documentID`)
    REFERENCES `kmutt_database`.`activityDocument` (`documentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_activityDocument_has_evaluation_evaluation1`
    FOREIGN KEY (`evaluationID`)
    REFERENCES `kmutt_database`.`evaluation` (`evaluationID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`activity`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`activity` (
  `activityID` INT NOT NULL AUTO_INCREMENT,
  `activityName` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`activityID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`document_activity`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`document_activity` (
  `activityID` INT NOT NULL,
  `documentID` INT NOT NULL,
  `countHour` INT NOT NULL,
  PRIMARY KEY (`activityID`, `documentID`),
  INDEX `fk_activity_has_activityDocument_activityDocument1_idx` (`documentID` ASC) VISIBLE,
  INDEX `fk_activity_has_activityDocument_activity1_idx` (`activityID` ASC) VISIBLE,
  CONSTRAINT `fk_activity_has_activityDocument_activity1`
    FOREIGN KEY (`activityID`)
    REFERENCES `kmutt_database`.`activity` (`activityID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_activity_has_activityDocument_activityDocument1`
    FOREIGN KEY (`documentID`)
    REFERENCES `kmutt_database`.`activityDocument` (`documentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`result`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`result` (
  `documentID` INT NOT NULL,
  `kpiID` VARCHAR(2000) NOT NULL,
  `detail` VARCHAR(2000) NOT NULL,
  `target` VARCHAR(2000) NOT NULL,
  PRIMARY KEY (`documentID`),
  INDEX `fk_activityDocument_has_KPI_activityDocument1_idx` (`documentID` ASC) VISIBLE,
  CONSTRAINT `fk_activityDocument_has_KPI_activityDocument1`
    FOREIGN KEY (`documentID`)
    REFERENCES `kmutt_database`.`activityDocument` (`documentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`problem`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`problem` (
  `documentID` INT NOT NULL,
  `problemDetail` VARCHAR(2000) NOT NULL,
  `solution` VARCHAR(2000) NOT NULL,
  PRIMARY KEY (`documentID`),
  CONSTRAINT `fk_problem_activityDocument1`
    FOREIGN KEY (`documentID`)
    REFERENCES `kmutt_database`.`activityDocument` (`documentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`sustainability`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`sustainability` (
  `sustainabilityID` INT NOT NULL AUTO_INCREMENT,
  `sustainabilityName` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`sustainabilityID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kmutt_database`.`document_sustainability`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kmutt_database`.`document_sustainability` (
  `documentID` INT NOT NULL,
  `sustainabilityID` INT NOT NULL,
  `goalID` INT NULL,
  PRIMARY KEY (`documentID`, `sustainabilityID`),
  INDEX `fk_table1_sustainability1_idx` (`sustainabilityID` ASC) VISIBLE,
  INDEX `fk_table1_goal1_idx` (`goalID` ASC) VISIBLE,
  CONSTRAINT `fk_table1_activityDocument1`
    FOREIGN KEY (`documentID`)
    REFERENCES `kmutt_database`.`activityDocument` (`documentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_table1_sustainability1`
    FOREIGN KEY (`sustainabilityID`)
    REFERENCES `kmutt_database`.`sustainability` (`sustainabilityID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_table1_goal1`
    FOREIGN KEY (`goalID`)
    REFERENCES `kmutt_database`.`goal` (`goalID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
