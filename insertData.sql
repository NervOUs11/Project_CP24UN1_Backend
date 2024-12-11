-- Insert data into `faculty` table
INSERT INTO `kmutt_database`.`faculty` (`facultyName`) VALUES
('Engineering'),
('Science'),
('Business Administration'),
('SIT');

-- Insert data into `department` table
INSERT INTO `kmutt_database`.`department` (`departmentName`, `facultyID`) VALUES
('Computer Science', 1),
('Electrical Engineering', 1),
('Physics', 2),
('Finance', 3),
('IT', 4),
('CS', 4),
('DSI', 4);

-- Insert data into `role` table
INSERT INTO `kmutt_database`.`role` (`roleName`) VALUES
('Administrator'),
('Advisor'),
('Head of dept'),
('Dean');

-- Insert data into `staff` table
INSERT INTO `kmutt_database`.`staff` (`username`, `password`, `firstName`, `lastName`, `tel`, `alterEmail`, `roleID`, `departmentID`, `facultyID`) VALUES
('staff1@kmutt.ac.th', '$argon2id$v=19$m=65536,t=3,p=4$pMjaa2R7Rn6Eq5aXNzuzew$JAMNRXN62tpJ6dbLuN9DfxdxjQZNMuiOAY3lrr8MQ2A',
'John', 'Doe', '0912345678', 'john.doe@gmail.com', 1, 1, 1),
('staff2@kmutt.ac.th', '$argon2id$v=19$m=65536,t=3,p=4$pMjaa2R7Rn6Eq5aXNzuzew$JAMNRXN62tpJ6dbLuN9DfxdxjQZNMuiOAY3lrr8MQ2A',
'Jane', 'Smith', '0912345679', 'jane.smith@gmail.com', 2, 5, 4),
('staff3@kmutt.ac.th', '$argon2id$v=19$m=65536,t=3,p=4$pMjaa2R7Rn6Eq5aXNzuzew$JAMNRXN62tpJ6dbLuN9DfxdxjQZNMuiOAY3lrr8MQ2A',
'Bob', 'Johnson', '0912345680', 'bob.johnson@gmail.com', 2, 5, 4),
('staff4@kmutt.ac.th', '$argon2id$v=19$m=65536,t=3,p=4$pMjaa2R7Rn6Eq5aXNzuzew$JAMNRXN62tpJ6dbLuN9DfxdxjQZNMuiOAY3lrr8MQ2A',
'Tom', 'Lee', '0912345111', 'Tom.lee@gmail.com', 2, 3, 2),
('staff5@kmutt.ac.th', '$argon2id$v=19$m=65536,t=3,p=4$pMjaa2R7Rn6Eq5aXNzuzew$JAMNRXN62tpJ6dbLuN9DfxdxjQZNMuiOAY3lrr8MQ2A',
'Alice', 'A.', '0912345111', 'Alice@gmail.com', 3, 5, 4),
('staff6@kmutt.ac.th', '$argon2id$v=19$m=65536,t=3,p=4$pMjaa2R7Rn6Eq5aXNzuzew$JAMNRXN62tpJ6dbLuN9DfxdxjQZNMuiOAY3lrr8MQ2A',
'Ben', 'B.', '0912345111', 'Ben@gmail.com', 4, 5, 4),
('staff7@kmutt.ac.th', '$argon2id$v=19$m=65536,t=3,p=4$pMjaa2R7Rn6Eq5aXNzuzew$JAMNRXN62tpJ6dbLuN9DfxdxjQZNMuiOAY3lrr8MQ2A',
'George', 'S.', '0912345111', 'George@gmail.com', 3, 3, 2),
('staff8@kmutt.ac.th', '$argon2id$v=19$m=65536,t=3,p=4$pMjaa2R7Rn6Eq5aXNzuzew$JAMNRXN62tpJ6dbLuN9DfxdxjQZNMuiOAY3lrr8MQ2A',
'Tim', 'S.', '0912345111', 'Tim@gmail.com', 4, 3, 2);

-- Insert data into `student` table
INSERT INTO `kmutt_database`.`student` (`studentID`, `username`, `password`, `firstName`, `lastName`, `tel`, `alterEmail`,
`year`, `departmentID`, `facultyID`, `currentGPA`, `cumulativeGPA`) VALUES
(64130500045, 'nitis.visa@kmutt.ac.th', '$argon2id$v=19$m=65536,t=3,p=4$pMjaa2R7Rn6Eq5aXNzuzew$JAMNRXN62tpJ6dbLuN9DfxdxjQZNMuiOAY3lrr8MQ2A',
'Nitis', 'Visayataksin', '0812345678', 'v.ounitit@gmail.com', 2, 5, 4, 3, 2.9),
(64130500051, 'Phongsathon@kmutt.ac.th', '$argon2id$v=19$m=65536,t=3,p=4$pMjaa2R7Rn6Eq5aXNzuzew$JAMNRXN62tpJ6dbLuN9DfxdxjQZNMuiOAY3lrr8MQ2A',
'Phongsathon', 'Chansongkrao', '0812345678', 'kitokidandkwa@gmail.com', 3, 3, 2, 3, 3.2);

-- Insert data into `student_advisor` table
INSERT INTO `kmutt_database`.`student_advisor` (`staffID`, `studentID`) VALUES
(2, 64130500045),
(3, 64130500045),
(4, 64130500051);
