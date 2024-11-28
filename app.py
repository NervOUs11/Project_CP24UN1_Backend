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
    attachmentFile1: Optional[bytes] = None
    attachmentFile2: Optional[bytes] = None
    attachmentFile2Name: Optional[str] = None
    # createDate: datetime
    # editDate: datetime


class ApproveDetail(BaseModel):
    progressID: int
    staffID: int
    documentID: int
    isApprove: str = "Approve"


class RejectDetail(BaseModel):
    progressID: int
    staffID: int
    documentID: int
    isApprove: str = "Reject"
    comment: str


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            connection_timeout=30
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")


@app.post("/api/login")
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
                "role": "Student",
                "tel": userResult[5],
                "alterEmail": userResult[6],
                "year": userResult[7],
                "departmentID": userResult[8],
                "department": departmentName[0],
                "facultyID": userResult[9],
                "faculty": facultyName[0],
                "currentGPA": userResult[10],
                "cumulativeGPA": userResult[11]
            }
        else:  # staff
            # get all user data
            select_user = "SELECT * FROM staff WHERE username = %s"
            cursor.execute(select_user, (user.username,))
            userResult = cursor.fetchone()
            # get role name
            select_department = "SELECT roleName FROM role WHERE roleID = %s"
            cursor.execute(select_department, (userResult[7],))
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
                "departmentID": userResult[8],
                "department": departmentName[0],
                "facultyID": userResult[9],
                "faculty": facultyName[0],
            }
        return user_info

    finally:
        cursor.close()
        conn.close()


@app.post("/api/signup")
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


@app.get("/api/allStaff")
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


@app.get("/api/allFaculty")
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


@app.get("/api/allDepartment")
def get_department():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""SELECT department.departmentID, 
                       department.departmentName, faculty.facultyName 
                       FROM department JOIN faculty 
                       ON department.facultyID = faculty.facultyID;""")
        roles = cursor.fetchall()
        return roles

    finally:
        cursor.close()
        conn.close()


@app.post("/api/add")
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

        all_staff_details = []
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
                          studentID, isApprove, createDate, editDate)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        for s in all_staff_details:
            cursor.execute(insert_progress, (
                s[0],
                s[7],
                document_id,
                form.studentID,
                "Waiting for approve",
                create_date,
                edit_date
            ))

        conn.commit()
        return {"message": "Created successfully"}, 201

    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Document creation failed: {e}")

    finally:
        cursor.close()
        conn.close()


@app.get("/api/allDocument/{id}")
async def get_all_document(id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    all_doc = []

    try:
        query = """SELECT 'student' AS table_name FROM student WHERE studentID = %s
                    UNION
                    SELECT 'staff' AS table_name FROM staff WHERE staffID = %s"""
        cursor.execute(query, (id, id))
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        userRole = result[0]

        if userRole == "student":
            query_form = """SELECT * FROM form WHERE studentID = %s"""
            cursor.execute(query_form, (id,))
            form_result = cursor.fetchall()

            query_progress = """SELECT progress.*, role.roleName 
                                    FROM progress 
                                    JOIN staff ON staff.staffID = progress.staffID
                                    JOIN role ON role.roleID = staff.roleID
                                    WHERE progress.studentID = %s"""
            cursor.execute(query_progress, (id,))
            progress_result = cursor.fetchall()

            progress_by_document = {}
            for p in progress_result:
                documentID = p[3]
                if documentID not in progress_by_document:
                    progress_by_document[documentID] = []
                progress_by_document[documentID].append({
                    "status": p[5],
                    "role": p[9]
                })

            for r in form_result:
                documentID = r[0]
                document_status = "Waiting for approve"

                if documentID in progress_by_document:
                    approvals = progress_by_document[documentID]

                    # Check for "Reject"
                    has_reject = any(a["status"] == "Reject" for a in approvals)
                    if has_reject:
                        document_status = "Reject"
                    else:
                        # Check for "Approve" conditions
                        roles_with_approve = [a["role"] for a in approvals if a["status"] == "Approve"]
                        if (
                                "Dean" in roles_with_approve and
                                "Head of dept" in roles_with_approve and
                                len(roles_with_approve) >= 3
                        ):
                            document_status = "Approve"

                document_info = {
                    "documentID": documentID,
                    "documentType": r[2],
                    "createDate": r[9],
                    "editDate": r[10],
                    "status": document_status
                }
                all_doc.append(document_info)
            return all_doc
        else:
            query = """SELECT progress.*, form.type
                    FROM progress
                    JOIN form ON progress.documentID = form.documentID
                    WHERE staffID = %s
                      AND (
                        -- Case 1: This is the first progress for the document
                        progress.progressID = (
                          SELECT MIN(first_progress.progressID)
                          FROM progress AS first_progress
                          WHERE first_progress.documentID = progress.documentID
                        )
                        OR
                        -- Case 2: The previous progress was approved
                        EXISTS (
                          SELECT 1
                          FROM progress AS prev_progress
                          WHERE prev_progress.progressID = progress.progressID - 1
                            AND prev_progress.documentID = progress.documentID
                            AND prev_progress.isApprove = 'Approve'
                        )
                      )
                      AND NOT EXISTS (
                        SELECT 1
                        FROM progress AS exclude_progress
                        JOIN role ON exclude_progress.staff_roleID = role.roleID
                        WHERE exclude_progress.documentID = progress.documentID
                          AND exclude_progress.isApprove = 'Approve'
                          AND role.roleName IN ('Dean', 'Head of dept')
                          AND EXISTS (
                            SELECT 1
                            FROM progress AS other_progress
                            WHERE other_progress.documentID = progress.documentID
                              AND other_progress.staffID != %s
                              AND other_progress.isApprove = 'Approve'
                          )
                      );"""
            cursor.execute(query, (id, id))
            result = cursor.fetchall()
            for r in result:
                document_info = {
                    "progessID": r[0],
                    "documentID": r[3],
                    "studentID": r[4],
                    "isApprove": r[5],
                    "comment": r[6],
                    "createDate": r[7],
                    "editDate": r[8],
                    "documentType": r[9]
                }
                all_doc.append(document_info)
            return all_doc

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


@app.get("/api/documentDetail/{documentID}/userID/{id}")
async def get_document_by_id(documentID: str, id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    progress = []

    try:
        query_form_detail = """SELECT * FROM form
                            WHERE documentID = %s"""
        cursor.execute(query_form_detail, (documentID,))
        detail_result = cursor.fetchone()

        if not detail_result:
            raise HTTPException(status_code=404, detail="Document not found")

        query_role = """SELECT 'student' AS table_name FROM student WHERE studentID = %s
                     UNION
                     SELECT 'staff' AS table_name FROM staff WHERE staffID = %s"""
        cursor.execute(query_role, (id, id))
        role = cursor.fetchone()

        if role is None:
            raise HTTPException(status_code=404, detail="User not found")
        userRole = role[0]

        if userRole == "student":
            query_authority = """SELECT * 
                                 FROM form 
                                 WHERE documentID = %s AND studentID = %s"""
            cursor.execute(query_authority, (documentID, id))
            authority_result = cursor.fetchone()
        else:
            query_authority = """SELECT progressID 
                              FROM progress 
                              WHERE documentID = %s AND staffID = %s"""
            cursor.execute(query_authority, (documentID, id))
            authority_result = cursor.fetchone()

        if not authority_result:
            raise HTTPException(status_code=403, detail="You do not have permission to access this document")

        query_progress = """SELECT progress.*, concat(staff.firstName, " ", staff.lastName), 
                         role.roleName
                         FROM progress
                         JOIN role ON progress.staff_roleID = role.roleID
                         JOIN staff ON progress.staffID = staff.staffID
                         WHERE documentID = %s"""
        cursor.execute(query_progress, (documentID,))
        progress_result = cursor.fetchall()

        for p in progress_result:
            info = {
                "progressID": p[0],
                "staffName": p[9],
                "staffRole": p[10],
                "status": p[5]
            }
            progress.append(info)

        document_info = {
            "DocumentID": detail_result[0],
            "DocumentType": detail_result[2],
            "startTime": detail_result[3],
            "endTime": detail_result[4],
            "detail": detail_result[5],
            "file1": detail_result[6],
            "file2": detail_result[7],
            "file2Name": detail_result[8],
            "createDate": detail_result[9],
            "editDate": detail_result[10],
            "allProgress": progress
        }

        if not document_info:
            raise HTTPException(status_code=404, detail="Document not found")

        return document_info

    except HTTPException as http_ex:
        raise http_ex

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    finally:
        cursor.close()
        conn.close()


@app.put("/api/approve")
async def approve(detail: ApproveDetail):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if progressID and documentID exist
        check_query = """SELECT progressID, documentID 
                         FROM progress 
                         WHERE progressID = %s AND documentID = %s;"""
        cursor.execute(check_query, (detail.progressID, detail.documentID))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Invalid progressID or documentID.")

        # Check if staffID matches progressID and documentID
        staff_check_query = """SELECT staffID 
                               FROM progress 
                               WHERE progressID = %s AND documentID = %s AND staffID = %s;"""
        cursor.execute(staff_check_query, (detail.progressID, detail.documentID, detail.staffID))
        staff_match = cursor.fetchone()

        if not staff_match:
            raise HTTPException(status_code=403, detail="Staff does not have the authority to approve this document.")

        update_query = """UPDATE progress
                          SET isApprove = %s
                          WHERE progressID = %s AND staffID = %s AND documentID = %s;"""
        cursor.execute(update_query, (
            detail.isApprove,
            detail.progressID,
            detail.staffID,
            detail.documentID
        ))
        conn.commit()

        return {"message": "Approve successfully."}

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

    finally:
        cursor.close()
        conn.close()


@app.put("/api/reject")
async def reject(detail: RejectDetail):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if progressID and documentID exist
        check_query = """SELECT progressID, documentID 
                                 FROM progress 
                                 WHERE progressID = %s AND documentID = %s;"""
        cursor.execute(check_query, (detail.progressID, detail.documentID))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Invalid progressID or documentID.")

        # Check if staffID matches progressID and documentID
        staff_check_query = """SELECT staffID 
                                       FROM progress 
                                       WHERE progressID = %s AND documentID = %s AND staffID = %s;"""
        cursor.execute(staff_check_query, (detail.progressID, detail.documentID, detail.staffID))
        staff_match = cursor.fetchone()

        if not staff_match:
            raise HTTPException(status_code=403, detail="Staff does not have the authority to approve this document.")

        update_query = """UPDATE progress
                       SET isApprove = %s, comment = %s
                       WHERE progressID = %s AND staffID = %s AND documentID = %s;"""
        cursor.execute(update_query, (
            detail.isApprove,
            detail.comment,
            detail.progressID,
            detail.staffID,
            detail.documentID
        ))
        conn.commit()
        return {"message": "Reject successfully."}

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

    finally:
        cursor.close()
        conn.close()
