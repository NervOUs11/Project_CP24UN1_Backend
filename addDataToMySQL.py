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

cursor = connection.cursor()

# Insert data into `role` table
roles = [
    ('Professor',),
    ('Assistant Professor',),
    ('Advisor',),
    ('Lecturer',),
    ('Administrator',)
]
cursor.executemany("INSERT INTO role (roleName) VALUES (%s)", roles)

# Insert data into `faculty` table
faculties = [
    ('Engineering',),
    ('Science',),
    ('Business',),
    ('Arts',),
    ('Education',),
    ('SIT',)
]
cursor.executemany("INSERT INTO faculty (facultyName) VALUES (%s)", faculties)

# Insert data into `department` table with faculty ID references
departments = [
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
    ('DSI', 6)
]
cursor.executemany("INSERT INTO department (departmentName, facultyID) VALUES (%s, %s)", departments)

# Staff records with plaintext passwords to be hashed
staff_records = [
    ('johndoe@gmail.com', 'password123', 'John', 'Doe', '1234567890', 'jdoe@example.com', 'dummySignature1', None, 1, 1, 1),
    ('alicesmith@gmail.com', 'password123', 'Alice', 'Smith', '0987654321', 'asmith@example.com', 'dummySignature1', None, 2, 2, 1),
    ('bobnguyen@gmail.com', 'password123', 'Bob', 'Nguyen', '1122334455', 'bnguyen@example.com', 'dummySignature1', None, 3, 3, 2),
    ('charliejones@gmail.com', 'password123', 'Charlie', 'Jones', '2233445566', 'cjones@example.com', 'dummySignature1', None, 4, 5, 3),
    ('dianajames@gmail.com', 'password123', 'Diana', 'James', '3344556677', 'djames@example.com', 'dummySignature1', None, 5, 9, 5)
]

# Insert each staff record with hashed password
for record in staff_records:
    username, password, firstName, lastName, tel, alterEmail, signature, profileImg, roleID, departmentID, facultyID = record
    hashed_password = ph.hash(password)  # Hash the password using Argon2

    # SQL query to insert the staff record with hashed password
    sql = """
    INSERT INTO staff (username, password, firstName, lastName, tel, alterEmail, signature, profileImg, roleID, departmentID, facultyID)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = (username, hashed_password, firstName, lastName, tel, alterEmail, signature, profileImg, roleID, departmentID, facultyID)
    cursor.execute(sql, data)

# Commit the transaction
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()

print("Data inserted into `role`, `faculty`, `department`, and `staff` tables.")
