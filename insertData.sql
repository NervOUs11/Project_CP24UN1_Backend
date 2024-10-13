-- Insert data into the `role` table
INSERT INTO `kmutt_database`.`role` (`roleName`)
VALUES
('role1'),
('role2'),
('role3'),
('role4'),
('role5'),
('role6'),
('role7'),
('role8');

-- Insert data into the `signer` table
INSERT INTO `kmutt_database`.`signer`
(`username`, `password`, `firstName`, `lastName`, `tel`, `backupEmail`, `signature`, `profileImg`, `roleID`)
VALUES
('signer1', 'password1', 'John', 'Doe', '0123456789', 'john.doe@example.com', 'dummySignature1', NULL, 1),
('signer2', 'password2', 'Jane', 'Smith', '0123456790', 'jane.smith@example.com', 'dummySignature2', NULL, 2),
('signer3', 'password3', 'Mike', 'Johnson', '0123456791', 'mike.johnson@example.com', 'dummySignature3', NULL, 3),
('signer4', 'password4', 'Emily', 'Davis', '0123456792', 'emily.davis@example.com', 'dummySignature4', NULL, 4),
('signer5', 'password5', 'David', 'Brown', '0123456793', 'david.brown@example.com', 'dummySignature5', NULL, 5);

-- Insert data into the `faculty` table
INSERT INTO `kmutt_database`.`faculty` (`facultyName`)
VALUES
('SIT'),
('Engineering'),
('Architecture'),
('Science');

-- Insert data into the `department` table
INSERT INTO `kmutt_database`.`department` (`departmentName`, `facultyID`)
VALUES
('IT', 1),
('CS', 1),
('DSI', 1),
('Mechanical Engineering', 2),
('Electrical Engineering', 2),
('Civil Engineering', 2),
('Urban Design', 3),
('Landscape Architecture', 3),
('Interior Architecture', 3),
('Biology', 4),
('Chemistry', 4),
('Physics', 4);
