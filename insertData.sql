-- Insert data into `faculty` table
INSERT INTO `kmutt_database`.`faculty` (`facultyName`) VALUES
('คณะวิศวกรรมศาสตร์'),
('คณะวิทยาศาสตร์'),
('คณะบริหารธุรกิจ'),
('คณะเทคโนโลยีสารสนเทศ'),
('องค์การนักศึกษา'),
('สภานักศึกษา');

-- Insert data into `department` table
INSERT INTO `kmutt_database`.`department` (`departmentName`, `facultyID`) VALUES
('สาขาวิศวกรรมคอมพิวเตอร์', 1),
('สาขาวิศวกรรมไฟฟ้า', 1),
('สาขาฟิสิกส์', 2),
('สาขาการเงิน', 3),
('สาขาเทคโนโลยีสารสนเทศ', 4),
('สาขาวิทยาการคอมพิวเตอร์', 4),
('สาขานวัตกรรมบริการดิจิทัล', 4);

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
('President of the Student Organization'),                -- นายกองค์การนักศึกษา
('Vice President of the Student Council'),                -- รองประธานสภานักศึกษา
('President of Student Council'),                         -- ประธานสภานักศึกษา
('Educational Service Provider'),                         -- นักบริการการศึกษา
('Director of Student Affairs Office'),                   -- ผู้อำนวยการสำนักงานกิจการนักศึกษา
('Vice President for Student and Learning Development');  -- รองอธิการบดีฝ่ายพัฒนานักศึกษาและผู้เรียนรู้

-- Insert data into `club` table
INSERT INTO `kmutt_database`.`club` (`clubName`) VALUES
('ชมรมอาสาพัฒนาชนบท'),
('ชมรมติว'),
('ชมรมพุทธศาสตร์'),
('ชมรมฟุตบอล');

-- Insert data into `staff` table
INSERT INTO `kmutt_database`.`staff` (`username`, `firstName`, `lastName`, `tel`, `email`, `roleID`, `departmentID`, `facultyID`, `clubID`) VALUES
('stf01', 'John', 'Doe', '0912345678', 'jonathan.deoe@gmail.com', 1, 1, 1, null),
('lec01', 'Jane', 'Smith', '0912345679', 'jensen.smithx@gmail.com', 2, 5, 4, null),
('lec02', 'Bob', 'Johnson', '0912345680', 'bobbybron.johnson@gmail.com', 2, 5, 4, null),
('lec03', 'Tom', 'Lee', '0912345111', 'tommory.lee@gmail.com', 2, 3, 2, null),
('lec04', 'Alice', 'A.', '0912345111', 'domchowhurnroman@gmail.com', 3, 5, 4, null),
('lec05', 'Ben', 'B.', '0912345111', 'domchowhurnromanII@gmail.com', 4, 5, 4, null),
('lec06', 'George', 'S.', '0912345111', 'domchowhurnromanIII@gmail.com', 3, 3, 2, null),
('lec07', 'Tim', 'S.', '0912345111', 'kitokidandkwa@gmail.com', 4, 3, 2, null),
('stf02', 'Emily', 'Johnson', '0912345678', 'emily.johnson@gmail.com', 5, null, null, null),
('stf03', 'Michael', 'Brown', '0912345678', 'michael.brown@gmail.com', 6, null, null, null),
('stf04', 'Sarah', 'Davis', '0912345678', 'sarah.davis@gmail.com', 7, null, null, null),
('stf05', 'David', 'Wilson', '0912345678', 'david.wilson@gmail.com', 8, null, null, null),
('stf06', 'Jessica', 'Martinez', '0912345678', 'jessica.martinez@gmail.com', 9, null, null, null),
('stf07', 'Daniel', 'Anderson', '0912345678', 'daniel.anderson@gmail.com', 10, null, null, null),
('stf08', 'Laura', 'Thomas', '0912345678', 'laura.thomas@gmail.com', 11, null, null, null),
('stf09', 'Matthew', 'Taylor', '0912345678', 'matthew.taylor@gmail.com', 12, null, null, null),
('stf10', 'Olivia', 'Harris', '0912345678', 'olivia.harris@gmail.com', 13, null, null, null),
('stf11', 'Christopher', 'Martin', '0912345678', 'christopher.martin@gmail.com', 14, null, null, null),
('stf12', 'Andrew', 'Thompson', '0912345678', 'andrew.thompson@gmail.com', 15, null, null, null),
('stf13', 'Nancy', 'Garcia', '0912345678', 'nancy.garcia@gmail.com', 16, null, null, null),
('stf14', 'Joshua', 'Martinez', '0912345678', 'joshua.martinez@gmail.com', 17, null, null, null);

-- Insert data into `student` table
INSERT INTO `kmutt_database`.`student` (`studentID`, `username`, `firstName`, `lastName`, `tel`, `email`,
`year`, `departmentID`, `facultyID`, `currentGPA`, `cumulativeGPA`, `clubID`) VALUES
(64130500045, 'std01', 'Nitis', 'Visayataksin', '0812345678', 'nitis.v@mail.kmutt.ac.th', 2, 5, 4, 3, 2.9, 1),
(64130500051, 'std02', 'Phongsathon', 'Chansongkrao', '0812345678', 'kitokidandkwa@gmail.com', 3, 3, 2, 3, 3.2, 3);

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
("Knowledge(ความรู้)"),
("Professional Skill(ทักษะทางวิชาชีพ)"),
("Thinking Skill(ทักษะการคิด)"),
("Learning Skill(ทักษะการเรียนรู้)"),
("Communication Skill(ทักษะการสื่อสาร)"),
("Management Skill(ทักษะการบริหารจัดการ)"),
("Leadership(ภาวะผู้นำ)"),
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