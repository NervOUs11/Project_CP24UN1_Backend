from argon2 import PasswordHasher
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("DB_HOSTNAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_DATABASE")
ph = PasswordHasher()

connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Create a cursor object
cursor = connection.cursor()

# Data to insert
faculty_data = [
    ('Engineering',),  # 1
    ('Science',),  # 2
    ('Business Administration',),  # 3
    ('SIT',)  # 4
]

department_data = [
    ('Computer Science', 1),  # 1
    ('Electrical Engineering', 1),  # 2
    ('Physics', 2),  # 3
    ('Finance', 3),  # 4
    ('IT', 4),  # 5
    ('CS', 4),  # 6
    ('DSI', 4)  # 7
]

role_data = [
    ('Administrator',),  # 1
    ('Professor',),  # 2
    ('Researcher',),  # 3
    ('Lecturer',),  # 4
    ('Advisor',),  # 5
    ('Head of dept',),  # 6
    ('Dean',)  # 7
]

staff_data = [
    ('staff1@kmutt.ac.th', ph.hash("password123"), 'John', 'Doe', '0912345678', 'john.doe@gmail.com', 1, 1, 1),
    ('staff2@kmutt.ac.th', ph.hash("password123"), 'Jane', 'Smith', '0912345679', 'jane.smith@gmail.com', 2, 5, 4),
    ('staff3@kmutt.ac.th', ph.hash("password123"), 'Bob', 'Johnson', '0912345680', 'bob.johnson@gmail.com', 3, 5, 4),
    ('staff4@kmutt.ac.th', ph.hash("password123"), 'Tom', 'Lee', '0912345111', 'Tom.lee@gmail.com', 3, 3, 2),
    ('staff5@kmutt.ac.th', ph.hash("password123"), 'Alice', 'A.', '0912345111', 'Alice@gmail.com', 6, 5, 4),
    ('staff6@kmutt.ac.th', ph.hash("password123"), 'Ben', 'B.', '0912345111', 'Ben@gmail.com', 7, 5, 4),
    ('staff7@kmutt.ac.th', ph.hash("password123"), 'George', 'S.', '0912345111', 'George@gmail.com', 6, 3, 2),
    ('staff8@kmutt.ac.th', ph.hash("password123"), 'Tim', 'S.', '0912345111', 'Tim@gmail.com', 7, 3, 2)
]

student_data = [
    (64130500045, 'nitis.visa@kmutt.ac.th', ph.hash("password123"), 'Nitis', 'Visayataksin', '0812345678',
     'v.ounitit@gmail.com', 2, 5, 4),
    (64130500051, 'Phongsathon@kmutt.ac.th', ph.hash("password123"), 'Phongsathon', 'Chansongkrao', '0812345678',
     'kitokidandkwa@gmail.com', 3, 3, 2),
    # (64130500001, 'Sasithon@kmutt.ac.th', ph.hash("password123"), 'Sasithon', 'Dontree', '0812345678',
    #  'jonathan.jillef@gmail.com', 3, 4, 3),
]

student_advisor_data = [
    (2, 64130500045),
    (3, 64130500045),
    (4, 64130500051)
]

try:
    connection.start_transaction()

    # Insert data into `faculty` table
    faculty_count = 0
    for faculty in faculty_data:
        cursor.execute("INSERT INTO `faculty` (`facultyName`) VALUES (%s)", faculty)
        faculty_count += 1
    print(f"Added {faculty_count} rows in 'faculty' table successfully.")

    # Insert data into `department` table
    department_count = 0
    for department in department_data:
        cursor.execute("INSERT INTO `department` (`departmentName`, `facultyID`) VALUES (%s, %s)", department)
        department_count += 1
    print(f"Added {department_count} rows in 'department' table successfully.")

    # Insert data into `role` table
    role_count = 0
    for role in role_data:
        cursor.execute("INSERT INTO `role` (`roleName`) VALUES (%s)", role)
        role_count += 1
    print(f"Added {role_count} rows in 'role' table successfully.")

    # Insert data into `staff` table
    staff_count = 0
    for staff in staff_data:
        cursor.execute("""
            INSERT INTO `staff` (`username`, `password`, `firstName`, `lastName`, `tel`, `alterEmail`, `roleID`, `departmentID`, `facultyID`) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, staff)
        staff_count += 1
    print(f"Added {staff_count} rows in 'staff' table successfully.")

    # Insert data into `student` table
    student_count = 0
    for student in student_data:
        cursor.execute("""
            INSERT INTO `student` (`studentID`, `username`, `password`, `firstName`, `lastName`, `tel`, `alterEmail`, `year`, `departmentID`, `facultyID`) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, student)
        student_count += 1
    print(f"Added {student_count} rows in 'student' table successfully.")

    # Insert data into `student_advisor` table
    advisor_count = 0
    for advisor in student_advisor_data:
        cursor.execute("INSERT INTO `student_advisor` (`staffID`, `studentID`) VALUES (%s, %s)", advisor)
        advisor_count += 1
    print(f"Added {advisor_count} rows in 'student_advisor' table successfully.")

    # Commit the transaction
    connection.commit()
    print("All data inserted successfully!")

except mysql.connector.Error as err:
    connection.rollback()
    print(f"Error: {err}")

finally:
    cursor.close()
    connection.close()
