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


class FormCreate(BaseModel):
    studentID: int
    studentFacultyID: int
    studentDepartmentID: int
    type: str
    startTime: datetime
    endTime: datetime
    detail: str
    attachmentFile1: bytes
    attachmentFile2: bytes
    attachmentFile2Name: str
    # createDate: datetime
    # editDate: datetime


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
            cursor.execute(select_department, (userResult[8],))
            departmentName = cursor.fetchone()
            # get faculty name
            select_faculty = "SELECT facultyName FROM faculty WHERE facultyID = %s"
            cursor.execute(select_faculty, (userResult[9],))
            facultyName = cursor.fetchone()

            user_info = {
                "studentID": userResult[0],
                "username": userResult[1],
                "firstName": userResult[3],
                "lastName": userResult[4],
                "tel": userResult[5],
                "alterEmail": userResult[6],
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
            cursor.execute(select_department, (userResult[8],))
            departmentName = cursor.fetchone()
            # get faculty name
            select_faculty = "SELECT facultyName FROM faculty WHERE facultyID = %s"
            cursor.execute(select_faculty, (userResult[9],))
            facultyName = cursor.fetchone()

            user_info = {
                "staffID": userResult[0],
                "username": userResult[1],
                "firstName": userResult[3],
                "lastName": userResult[4],
                "tel": userResult[5],
                "alterEmail": userResult[6],
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
async def create_document(form: FormCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        create_date = datetime.now()
        edit_date = create_date
        insert_form = """INSERT INTO form (studentID, type, startTime, endTime, detail, attachmentFile1,
                      attachmentFile2, attachmentFile2Name, createDate, editDate)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(insert_form, (
            form.studentID,
            form.type,
            form.startTime,
            form.endTime,
            form.detail,
            form.attachmentFile1,
            form.attachmentFile2,
            form.attachmentFile2Name,
            create_date,
            edit_date
        ))
        document_id = cursor.lastrowid

        staffID_query = """select staffID from student_advisor where studentID = %s"""
        cursor.execute(staffID_query, (
            form.studentID,
        ))
        staffID_results = cursor.fetchall()

        if not staffID_results:
            raise HTTPException(status_code=404, detail="No staffIDs found for the given studentID")

        # List to hold all staff details
        all_staff_details = []

        # Loop through each staffID and get details from the staff table
        for (staffID,) in staffID_results:
            staff_query = """SELECT * FROM staff 
                          JOIN role ON staff.roleID = role.roleID 
                          WHERE staffID = %s"""
            cursor.execute(staff_query, (staffID,))
            staff_details = cursor.fetchall()

            if staff_details:
                all_staff_details.extend(staff_details)  # Add each staff's details to the list

        if not all_staff_details:
            raise HTTPException(status_code=404, detail="No staff details found for the given staffIDs")

        signer_query = """SELECT * FROM staff 
                       JOIN role ON staff.roleID = role.roleID 
                       WHERE staff.facultyID = %s 
                       AND (role.roleName = 'Head of dept' OR role.roleName = 'Dean')"""
        cursor.execute(signer_query, (form.studentFacultyID,))
        staff = cursor.fetchall()
        if staff:
            all_staff_details.extend(staff)

        insert_progress = """INSERT INTO progress (staffID, staff_roleID, documentID,
                          studentID, createDate, editDate)
                          VALUES (%s, %s, %s, %s, %s, %s)"""
        for s in all_staff_details:
            cursor.execute(insert_progress, (
                s[0],
                s[7],
                document_id,
                form.studentID,
                create_date,
                edit_date
            ))

        conn.commit()
        # return {"staff_details": all_staff_details}
        return {"message": "Created successfully"}, 201

    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Document creation failed: {e}")

    finally:
        cursor.close()
        conn.close()


@app.get("/document/{id}")
async def get_all_document(id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
                SELECT 'student' AS table_name FROM student WHERE studentID = %s
                UNION
                SELECT 'staff' AS table_name FROM staff WHERE staffID = %s
                """
        cursor.execute(query, (id, id))
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        userRole = result[0]

        if userRole == "student":
            query = """SELECT * FROM form WHERE studentID = %s"""
            cursor.execute(query, (id,))
            result = cursor.fetchall()
            return {"document": result, "Table": "document"}
        else:
            query = """SELECT * FROM progress 
                    JOIN form ON progress.documentID = form.documentID 
                    WHERE staffID = %s
                    """
            cursor.execute(query, (id,))
            result = cursor.fetchall()
            return {"document": result, "Table": "progress"}

    finally:
        cursor.close()
        conn.close()


@app.get("/document/{documentID}")
async def get_document_by_id(documentID: str):
    conn = get_db_connection()
    cursor = conn.cursor()