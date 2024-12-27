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
('Dean'),                                                 -- คณบดี
("Club's advisor"),                                       -- ที่ปรึกษาชมรม
("Prime Minister"),                                       -- นายก
('Deputy Dean'),                                          -- รองคณบดี
('ประธานฝ่ายบำเพ็ญประโยชน์'),
('ประธานฝ่ายวิชาการ'),
('ประธานฝ่ายศิลปะและวัฒนธรรม'),
('ประธานฝ่ายกีฬา'),
('นายกองค์การนักศึกษา'),
('Vice President of the Student Council'),                -- รองประธานสภานักศึกษา
('President of Student Council'),                         -- ประธานสภานักศึกษา
('Educational Service Provider'),                         -- นักบริการการศึกษา
('Director of Student Affairs Office'),                   -- ผู้อำนวยการสำนักงานกิจการนักศึกษา
('Vice President for Student and Learning Development');  -- รองอธิการบดีฝ่ายพัฒนานักศึกษาและผู้เรียนรู้

-- Insert data into `club` table
INSERT INTO `kmutt_database`.`club` (`clubName`) VALUES
('อาสาพัฒนาชนบท'),
('ติว'),
('พุทธศาสตร์'),
('ฟุตบอล');

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

-- Insert data into `participant ` table
INSERT INTO `kmutt_database`.`participant` (`participantName`) VALUES
("Student"),
("Teacher"),
("Staff"),
("Other");

-- Insert data into `studentQF ` table
INSERT INTO `kmutt_database`.`studentQF` (`name`) VALUES
("Knowledge"),
("Professional Skill"),
("Thinking Skill"),
("Learning Skill"),
("Communication Skill"),
("Management Skill"),
("Leadership"),
("KMUTT’s citizenship");

-- Insert data into `entrepreneurial ` table
INSERT INTO `kmutt_database`.`entrepreneurial` (`entrepreneurialName`) VALUES
("Entrepreneurial Mindset"),
("Knowledge Sharing Society"),
("Research and Innovation Impact"),
("Financial Literacy");

-- Insert data into `evaluation ` table
INSERT INTO `kmutt_database`.`evaluation` (`evaluationName`) VALUES
("Observation"),
("Interview"),
("Questionnaires"),
("Test"),
("Other");

-- Insert data into `activity ` table
INSERT INTO `kmutt_database`.`activity` (`activityName`) VALUES
("ด้านพัฒนาทักษะทางวิชาการและวิชาชีพ"),
("ด้านกีฬาและการส่งเสริมสุขภาพ"),
("ด้านกิจกรรมจิตอาสาและบำเพ็ญประโยชน์"),
("ด้านทำนุบำรุงศิลปะแลวัฒนธรรม"),
("ด้านการพัฒนาคุณลักษณะ"),
("ด้านความภูมิใจและความผูกพันมหาวิทยาลัย");

-- Insert data into `sustainability ` table
INSERT INTO `kmutt_database`.`sustainability` (`sustainabilityName`) VALUES
("SDGs Culture"),
("Sustainability Change Agents"),
("Green University and Smart Campus"),
("Carbon Neutrality ");

-- Insert data into `goal` table
INSERT INTO `kmutt_database`.`goal` (`goalName`) VALUES
("No Poverty"),
("Zero Hunger"),
("Good Health and Well-Being"),
("Quality Education"),
("Gender Equality"),
("Clean Water and Sanitation"),
("Affordable and Clean Energy"),
("Decent Work and Economic Growth"),
("Industry, Innovation, and Infrastructure"),
("Reduced Inequalities"),
("Sustainable Cities and Communities"),
("Responsible Consumption and Production"),
("Climate Action"),
("Life Below Water"),
("Life on Land"),
("Peace, Justice and Strong Institutions"),
("Partnerships");