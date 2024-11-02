-- Insert data into the `role` table
INSERT INTO `kmutt_database`.`role` (roleName) VALUES
('Professor'),
('Assistant Professor'),
('Advisor'),
('Lecturer'),
('Administrator');

-- Insert data into the `faculty` table
INSERT INTO `kmutt_database`.`faculty` (facultyName) VALUES
('Engineering'),
('Science'),
('Business'),
('Arts'),
('Education'),
('SIT');

-- Insert data into the `department` table
INSERT INTO `kmutt_database`.`department` (departmentName, facultyID) VALUES
('Computer Engineering', 1),
('Electrical Engineering', 1),
('Chemistry', 2),
('Physics', 2),
('Marketing', 3),
('Finance', 3),
('Fine Arts', 4),
('Music', 4),
('Teacher Education', 5),
('IT', 6),
('CS', 6),
('DSI', 6);

-- Insert data into the `staff` table
INSERT INTO `kmutt_database`.`staff` (username, password, firstName, lastName, tel, alterEmail, signature, profileImg, roleID, departmentID, facultyID) VALUES
('johndoe@gmail.com', 'password123', 'John', 'Doe', '1234567890', 'jdoe@example.com', 'dummySignature1', NULL, 1, 1, 1),
('alicesmith@gmail.com', 'password123', 'Alice', 'Smith', '0987654321', 'asmith@example.com', 'dummySignature1', NULL, 2, 2, 1),
('bobnguyen@gmail.com', 'password123', 'Bob', 'Nguyen', '1122334455', 'bnguyen@example.com', 'dummySignature1', NULL, 3, 3, 2),
('charliejones@gmail.com', 'password123', 'Charlie', 'Jones', '2233445566', 'cjones@example.com', 'dummySignature1', NULL, 4, 5, 3),
('dianajames@gmail.com', 'password123', 'Diana', 'James', '3344556677', 'djames@example.com', 'dummySignature1', NULL, 5, 9, 5);
