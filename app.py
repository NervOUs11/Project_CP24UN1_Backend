import mysql.connector
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from argon2 import PasswordHasher
from pydantic import BaseModel

app = FastAPI()
ph = PasswordHasher()
load_dotenv()
host = os.getenv("DB_HOSTNAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_DATABASE")


class StudentSignUp(BaseModel):
    studentID: int
    username: str
    password: str
    firstname: str
    lastname: str
    phone_number: str
    backup_email: str
    signature: bytes = b"dummySignature"
    advisor1_fullname: str
    advisor2_fullname: str
    faculty: str
    department: str


class UserLogin(BaseModel):
    username: str
    password: str

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow only the frontend's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


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
        select_query = "SELECT password FROM student WHERE username = %s"
        cursor.execute(select_query, (user.username,))
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        stored_password = result[0]

        try:
            ph.verify(stored_password, user.password)

        except Exception:
            raise HTTPException(status_code=400, detail="Invalid password")
        return {"message": "Login successful"}

    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail="Login failed")

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

        # Check for advisor1
        cursor.execute("SELECT signerID FROM signer WHERE CONCAT(firstName, ' ', lastName) = %s",
                       (student.advisor1_fullname,))
        advisor1_id = cursor.fetchone()
        if not advisor1_id:
            raise HTTPException(status_code=400, detail="Advisor 1 not found")

        # Check for advisor2
        cursor.execute("SELECT signerID FROM signer WHERE CONCAT(firstName, ' ', lastName) = %s",
                       (student.advisor2_fullname,))
        advisor2_id = cursor.fetchone()
        if not advisor2_id:
            raise HTTPException(status_code=400, detail="Advisor 2 not found")

        # Check for faculty
        cursor.execute("SELECT facultyID FROM faculty WHERE facultyName = %s", (student.faculty,))
        faculty_id = cursor.fetchone()
        if not faculty_id:
            raise HTTPException(status_code=400, detail="Faculty not found")

        # Check for department
        cursor.execute("SELECT departmentID FROM department WHERE departmentName = %s", (student.department,))
        department_id = cursor.fetchone()
        if not department_id:
            raise HTTPException(status_code=400, detail="Department not found")

        # Insert new student
        insert_query = """
            INSERT INTO student (studentID, username, password, firstname, lastname, 
                                 tel, backupEmail, advisorID1, advisorID2, 
                                 facultyID, departmentID, signature) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            student.studentID,
            student.username,
            hashed_password,
            student.firstname,
            student.lastname,
            student.phone_number,
            student.backup_email,
            advisor1_id[0],
            advisor2_id[0],
            faculty_id[0],
            department_id[0],
            student.signature
        ))
        conn.commit()
        return {"message": "User registered successfully"}, 200

    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"User registration failed: {e}")

    finally:
        cursor.close()
        conn.close()


@app.get("/allSigner")
def get_signer():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:

        cursor.execute("SELECT * FROM signer;")
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