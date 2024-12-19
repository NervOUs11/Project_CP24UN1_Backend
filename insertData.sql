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
INSERT INTO `kmutt_database`.`staff` (`username`, `firstName`, `lastName`, `tel`, `email`, `roleID`, `departmentID`, `facultyID`) VALUES
('stf01', 'John', 'Doe', '0912345678', 'jonathan.deoe@gmail.com', 1, 1, 1),
('lec01', 'Jane', 'Smith', '0912345679', 'jensen.smithx@gmail.com', 2, 5, 4),
('lec02', 'Bob', 'Johnson', '0912345680', 'bobbybron.johnson@gmail.com', 2, 5, 4),
('lec03', 'Tom', 'Lee', '0912345111', 'tommory.lee@gmail.com', 2, 3, 2),
('lec04', 'Alice', 'A.', '0912345111', 'domchowhurnroman@gmail.com', 3, 5, 4),
('lec05', 'Ben', 'B.', '0912345111', 'domchowhurnromanII@gmail.com', 4, 5, 4),
('lec06', 'George', 'S.', '0912345111', 'domchowhurnromanIII@gmail.com', 3, 3, 2),
('lec07', 'Tim', 'S.', '0912345111', 'kitokidandkwa@gmail.com', 4, 3, 2);

-- Insert data into `student` table
INSERT INTO `kmutt_database`.`student` (`studentID`, `username`, `firstName`, `lastName`, `tel`, `email`,
`year`, `departmentID`, `facultyID`, `currentGPA`, `cumulativeGPA`) VALUES
(64130500045, 'std01', 'Nitis', 'Visayataksin', '0812345678', 'nitis.v@mail.kmutt.ac.th', 2, 5, 4, 3, 2.9),
(64130500051, 'std02', 'Phongsathon', 'Chansongkrao', '0812345678', 'kitokidandkwa@gmail.com', 3, 3, 2, 3, 3.2);

-- Insert data into `student_advisor` table
INSERT INTO `kmutt_database`.`student_advisor` (`staffID`, `studentID`) VALUES
(2, 64130500045),
(3, 64130500045),
(4, 64130500051);