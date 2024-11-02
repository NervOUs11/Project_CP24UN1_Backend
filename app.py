import mysql.connector
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from argon2 import PasswordHasher
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

app = FastAPI()
ph = PasswordHasher()
load_dotenv()
host = os.getenv("DB_HOSTNAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_DATABASE")
frontend_url = os.getenv("FRONTEND_URL")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StudentSignUp(BaseModel):
    studentID: int
    username: str
    password: str
    firstname: str
    lastname: str
    phone_number: str
    alter_email: str
    signature: bytes = b"dummySignature"
    advisor1_fullname: str
    advisor2_fullname: str
    faculty: str
    department: str


class UserLogin(BaseModel):
    username: str
    password: str


class DocumentCreate(BaseModel):
    # title: str
    # to: str
    # senderFaculty: str
    # description: str
    # amount: float
    # academicAndSkillDevelopment: Optional[int] = None
    # sportsAndHealth: Optional[int] = None
    # volunteer: Optional[int] = None
    # artAndCulturalPreservation: Optional[int] = None
    # characterDevelopment: Optional[int] = None
    # universityCommitment: Optional[int] = None
    # location: str
    startDate: datetime
    endDate: datetime
    studentID: int
    documentFilePDF: Optional[bytes] = None


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")


@app.post("/login")
async def log_in(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        username_query = """SELECT 'student' AS user_type, username 
                         FROM student WHERE username = %s
                         UNION ALL
                         SELECT 'staff' AS user_type, username 
                         FROM staff WHERE username = %s"""
        cursor.execute(username_query, (user.username, user.username))
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        userRole = result[0]

        # select_query = "SELECT password FROM student WHERE username = %s"
        # cursor.execute(select_query, (user.username,))
        # passwordResult = cursor.fetchone()
        # if passwordResult is None:
        #     raise HTTPException(status_code=404, detail="User not found")
        # stored_password = passwordResult[0]

        try:
            if userRole == 'student':
                select_query = "SELECT password FROM student WHERE username = %s"
            elif userRole == 'staff':
                select_query = "SELECT password FROM staff WHERE username = %s"
            else:
                select_query = "SELECT password FROM student WHERE username = %s"
                print("Not student or staff")
            cursor.execute(select_query, (user.username,))
            passwordResult = cursor.fetchone()
            stored_password = passwordResult[0]
            ph.verify(stored_password, user.password)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid password")

        if userRole == "student":
            # get all user data
            select_user = "SELECT * FROM student WHERE username = %s"
            cursor.execute(select_user, (user.username,))
            userResult = cursor.fetchone()
            # get department name
            select_department = "SELECT departmentName FROM department WHERE departmentID = %s"
            cursor.execute(select_department, (userResult[9],))
            departmentName = cursor.fetchone()
            # get faculty name
            select_faculty = "SELECT facultyName FROM faculty WHERE facultyID = %s"
            cursor.execute(select_faculty, (userResult[10],))
            facultyName = cursor.fetchone()

            user_info = {
                "studentID": userResult[0],
                "username": userResult[1],
                "firstName": userResult[3],
                "lastName": userResult[4],
                "tel": userResult[5],
                "alterEmail": userResult[6],
                "signature": userResult[7],
                "faculty": facultyName[0],
                "department": departmentName[0]
            }
        else:  # staff
            # get all user data
            select_user = "SELECT * FROM staff WHERE username = %s"
            cursor.execute(select_user, (user.username,))
            userResult = cursor.fetchone()
            # get role name
            select_department = "SELECT roleName FROM role WHERE roleID = %s"
            cursor.execute(select_department, (userResult[9],))
            roleName = cursor.fetchone()
            # get department name
            select_department = "SELECT departmentName FROM department WHERE departmentID = %s"
            cursor.execute(select_department, (userResult[10],))
            departmentName = cursor.fetchone()
            # get faculty name
            select_faculty = "SELECT facultyName FROM faculty WHERE facultyID = %s"
            cursor.execute(select_faculty, (userResult[11],))
            facultyName = cursor.fetchone()

            user_info = {
                "studentID": userResult[0],
                "username": userResult[1],
                "firstName": userResult[3],
                "lastName": userResult[4],
                "tel": userResult[5],
                "alterEmail": userResult[6],
                "signature": userResult[7],
                "role": roleName[0],
                "faculty": facultyName[0],
                "department": departmentName[0]
            }
        return {"message": "Login successful", "user": user_info}

    finally:
        cursor.close()
        conn.close()


@app.post("/signup")
async def sign_up(student: StudentSignUp):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Hash the password
        hashed_password = ph.hash(student.password)

        # Check for advisor1 (required)
        cursor.execute("SELECT staffID FROM staff WHERE CONCAT(firstName, ' ', lastName) = %s",
                       (student.advisor1_fullname,))
        advisor1_id = cursor.fetchone()
        if not advisor1_id:
            raise HTTPException(status_code=400, detail="Advisor 1 not found")

        # Check for advisor2 (optional but must exist if provided)
        advisor2_id = None
        if student.advisor2_fullname:
            cursor.execute("SELECT staffID FROM staff WHERE CONCAT(firstName, ' ', lastName) = %s",
                           (student.advisor2_fullname,))
            advisor2_id = cursor.fetchone()
            if not advisor2_id:
                raise HTTPException(status_code=400, detail="Advisor 2 not found")

        # Check for faculty
        cursor.execute("SELECT facultyID FROM faculty WHERE facultyName = %s", (student.faculty,))
        faculty_id = cursor.fetchone()
        if not faculty_id:
            raise HTTPException(status_code=400, detail="Faculty not found")

        # Check if department exists
        cursor.execute("SELECT departmentID, facultyID FROM department WHERE departmentName = %s",
                       (student.department,))
        department_record = cursor.fetchone()
        print(department_record)
        if not department_record:
            raise HTTPException(status_code=400, detail="Department not found")

        # Check if department belongs to the specified faculty
        if department_record[1] != faculty_id[0]:
            raise HTTPException(status_code=400, detail="Department does not belong to the specified faculty")

        # Insert new student
        insert_student_query = """
            INSERT INTO student (studentID, username, password, firstname, lastname,
                                 tel, alterEmail, facultyID, departmentID, signature)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_student_query, (
            student.studentID,
            student.username,
            hashed_password,
            student.firstname,
            student.lastname,
            student.phone_number,
            student.alter_email,
            faculty_id[0],
            department_record[0],
            student.signature
        ))

        # Insert advisor1
        insert_advisor_query = """
            INSERT INTO student_advisor (staffID, studentID)
            VALUES (%s, %s)
        """
        cursor.execute(insert_advisor_query, (advisor1_id[0], student.studentID))

        # Insert advisor2 (optional)
        if advisor2_id:
            cursor.execute(insert_advisor_query, (advisor2_id[0], student.studentID))

        conn.commit()
        return {"message": "User registered successfully"}

    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"User registration failed: {e}")

    finally:
        cursor.close()
        conn.close()


@app.get("/allStaff")
def get_signer():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:

        cursor.execute("SELECT * FROM staff;")
        roles = cursor.fetchall()
        return roles
    finally:
        cursor.close()
        conn.close()


@app.get("/allFaculty")
def get_faculty():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:

        cursor.execute("SELECT * FROM faculty;")
        roles = cursor.fetchall()
        return roles
    finally:
        cursor.close()
        conn.close()


@app.get("/allDepartment")
def get_department():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:

        cursor.execute("SELECT * FROM department;")
        roles = cursor.fetchall()
        return roles
    finally:
        cursor.close()
        conn.close()


@app.post("/add")
async def create_document(document: DocumentCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        create_date = datetime.now()
        edit_date = create_date

        # insert_query = """
        #     INSERT INTO document (title, `to`, senderFaculty, description, amount,
        #                           academicAndSkillDevelopment, sportsAndHealth, volunteer,
        #                           artAndCulturalPreservation, characterDevelopment,
        #                           universityCommitment, location, startDate, endDate,
        #                           studentID, documentFilePDF, createDate, editDate)
        #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        # """
        insert_query = """
                    INSERT INTO document (studentID, documentFilePDF, createDate, editDate)
                    VALUES (%s, %s, %s, %s)
                """

        cursor.execute(insert_query, (
            # document.title,
            # document.to,
            # document.senderFaculty,
            # document.description,
            # document.amount,
            # document.academicAndSkillDevelopment,
            # document.sportsAndHealth,
            # document.volunteer,
            # document.artAndCulturalPreservation,
            # document.characterDevelopment,
            # document.universityCommitment,
            # document.location,
            # document.startDate,
            # document.endDate,
            document.studentID,
            document.documentFilePDF,
            create_date,
            edit_date
        ))

        conn.commit()
        return {"message": "Document created successfully", "documentID": cursor.lastrowid}, 201

    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Document creation failed: {e}")

    finally:
        cursor.close()
        conn.close()