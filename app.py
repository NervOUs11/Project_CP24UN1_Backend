import mysql.connector
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from argon2 import PasswordHasher
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sendEmail import email_notification, EmailSchema
from login_JWT import get_token
from adminService import (get_all_user, get_all_role, get_all_club, edit_user_role, edit_user_club,
                          UpdateUserRole, UpdateUserClub)
from absenceDocument import (create_absence_document, delete_absence_document, update_absence_document,
                             approve_absence_document, reject_absence_document, detail_absence_document,
                             AbsenceFormCreate, AbsenceFormUpdate, ApproveDetail, RejectDetail)
from activityDocument import (create_activity_document, delete_activity_document, update_activity_document,
                             approve_activity_document, reject_activity_document, detail_activity_document,
                             ActivityFormCreate, ActivityFormUpdate, ApproveDetail, RejectDetail)

app = FastAPI()
ph = PasswordHasher()
load_dotenv()
host = os.getenv("DB_HOSTNAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_DATABASE")
frontend_url = os.getenv("FRONTEND_URL")
frontend_url_secondary = os.getenv("FRONTEND_URL_SECONDARY")
frontend_url_test = os.getenv("FRONTEND_URL_TEST")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, frontend_url_secondary, frontend_url_test],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserLogin(BaseModel):
    username: str
    password: str


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
        # Login with my own database
        # username_query = """SELECT 'student' AS user_type, username
        #                  FROM student WHERE username = %s
        #                  UNION ALL
        #                  SELECT 'staff' AS user_type, username
        #                  FROM staff WHERE username = %s"""
        # cursor.execute(username_query, (user.username, user.username))
        # result = cursor.fetchone()
        # if result is None:
        #     raise HTTPException(status_code=404, detail="User not found")
        # userRole = result[0]
        #
        # try:
        #     if userRole == 'student':
        #         select_query = "SELECT password FROM student WHERE username = %s"
        #     elif userRole == 'staff':
        #         select_query = "SELECT password FROM staff WHERE username = %s"
        #     else:
        #         select_query = "SELECT password FROM student WHERE username = %s"
        #         print("Not student or staff")
        #     cursor.execute(select_query, (user.username,))
        #     passwordResult = cursor.fetchone()
        #     stored_password = passwordResult[0]
        #     ph.verify(stored_password, user.password)
        # except Exception:
        #     raise HTTPException(status_code=401, detail="Invalid password")

        # Login with JWT
        try:
            response = await get_token(user.username, user.password)

        except Exception:
            raise HTTPException(status_code=401, detail="Username or Password incorrect")

        userRole = ""

        if response.status_code == 200:
            try:
                username_query = """SELECT 'student' AS user_type, username 
                                 FROM student WHERE username = %s
                                 UNION ALL
                                 SELECT 'staff' AS user_type, username 
                                 FROM staff WHERE username = %s"""
                cursor.execute(username_query, (user.username, user.username))
                result = cursor.fetchone()
                userRole = result[0]
            except Exception as error:
                print(error)
        else:
            raise HTTPException(status_code=401, detail="Username or Password incorrect")

        try:
            if userRole == "student":
                # get all user data
                select_user = "SELECT * FROM student WHERE username = %s"
                cursor.execute(select_user, (user.username,))
                userResult = cursor.fetchone()

                # get department name
                select_department = "SELECT departmentName FROM department WHERE departmentID = %s"
                cursor.execute(select_department, (userResult[7],))
                departmentName = cursor.fetchone()

                # get faculty name
                select_faculty = "SELECT facultyName FROM faculty WHERE facultyID = %s"
                cursor.execute(select_faculty, (userResult[8],))
                facultyName = cursor.fetchone()

                # get advisor
                select_advisor = """SELECT concat(staff.firstName, " ", staff.lastName)
                                 FROM student_advisor 
                                 JOIN staff ON staff.staffID = student_advisor.staffID
                                 WHERE studentID = %s"""
                cursor.execute(select_advisor, (userResult[0],))
                advisorName = cursor.fetchall()

                user_info = {
                    "studentID": userResult[0],
                    "username": userResult[1],
                    "firstName": userResult[2],
                    "lastName": userResult[3],
                    "role": "Student",
                    "tel": userResult[4],
                    "email": userResult[5],
                    "year": userResult[6],
                    "departmentID": userResult[7],
                    "department": departmentName[0],
                    "facultyID": userResult[8],
                    "faculty": facultyName[0],
                    "currentGPA": userResult[9],
                    "cumulativeGPA": userResult[10],
                    "advisor": advisorName
                }
            else:  # staff
                # get all user data
                select_user = "SELECT * FROM staff WHERE username = %s"
                cursor.execute(select_user, (user.username,))
                userResult = cursor.fetchone()
                # get role name
                select_department = "SELECT roleName FROM role WHERE roleID = %s"
                cursor.execute(select_department, (userResult[6],))
                roleName = cursor.fetchone()
                # get department name
                select_department = "SELECT departmentName FROM department WHERE departmentID = %s"
                cursor.execute(select_department, (userResult[7],))
                departmentName = cursor.fetchone()
                # get faculty name
                select_faculty = "SELECT facultyName FROM faculty WHERE facultyID = %s"
                cursor.execute(select_faculty, (userResult[8],))
                facultyName = cursor.fetchone()

                user_info = {
                    "staffID": userResult[0],
                    "username": userResult[1],
                    "firstName": userResult[2],
                    "lastName": userResult[3],
                    "tel": userResult[4],
                    "email": userResult[5],
                    "role": roleName[0],
                    "departmentID": userResult[7],
                    "department": departmentName[0],
                    "facultyID": userResult[8],
                    "faculty": facultyName[0],
                }
            return user_info

        except Exception as e:
            print(e)

    finally:
        cursor.close()
        conn.close()


@app.get("/api/admin/allUser")
async def admin_get_all_user():
    try:
        result = await get_all_user()
        return result
    except HTTPException as e:
        raise e


@app.get("/api/admin/allRole")
async def admin_get_all_role():
    try:
        result = await get_all_role()
        return result
    except HTTPException as e:
        raise e


@app.get("/api/admin/allClub")
async def admin_get_all_club():
    try:
        result = await get_all_club()
        return result
    except HTTPException as e:
        raise e


# @app.put("/api/admin/editUserRole/{user_id}")
# async def admin_edit_user_role(user_id: int, role: UpdateUserRole):
#     try:
#         result = await edit_user_role(user_id, role)
#         return result
#     except HTTPException as e:
#         raise e


# @app.put("/api/admin/editUserClub/{user_id}")
# async def admin_edit_user_club(user_id: int, club: UpdateUserClub):
#     try:
#         result = await edit_user_club(user_id, club)
#         return result
#     except HTTPException as e:
#         raise e


@app.get("/api/document/all/{id}")
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
            # Changed form to activityDocument and absenceDocument
            query_activity_doc = """SELECT * FROM activityDocument WHERE studentID = %s"""
            cursor.execute(query_activity_doc, (id,))
            activity_doc_result = cursor.fetchall()

            query_absence_doc = """SELECT * FROM absenceDocument WHERE studentID = %s"""
            cursor.execute(query_absence_doc, (id,))
            absence_doc_result = cursor.fetchall()

            query_activity_progress = """SELECT activityProgress.*, role.roleName 
                                         FROM activityProgress 
                                         JOIN staff ON staff.staffID = activityProgress.staffID
                                         JOIN role ON role.roleID = staff.roleID
                                         WHERE activityProgress.studentID = %s"""
            cursor.execute(query_activity_progress, (id,))
            activity_progress_result = cursor.fetchall()

            query_absence_progress = """SELECT absenceProgress.*, role.roleName 
                                        FROM absenceProgress 
                                        JOIN staff ON staff.staffID = absenceProgress.staffID
                                        JOIN role ON role.roleID = staff.roleID
                                        WHERE absenceProgress.studentID = %s"""
            cursor.execute(query_absence_progress, (id,))
            absence_progress_result = cursor.fetchall()

            progress_by_document = {}
            for p in activity_progress_result + absence_progress_result:
                documentID = p[4]
                if documentID not in progress_by_document:
                    progress_by_document[documentID] = []
                progress_by_document[documentID].append({
                    "status": p[6],
                    "role": p[11]
                })

            for r in activity_doc_result + absence_doc_result:
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
            # Changed progress to activityProgress and absenceProgress
            query_activity_progress = """SELECT activityProgress.*, activityDocument.type
                                         FROM activityProgress
                                         JOIN activityDocument ON activityProgress.documentID = activityDocument.documentID
                                         WHERE activityProgress.staffID = %s
                                         AND (
                                            activityProgress.step = 1
                                            OR EXISTS (
                                                SELECT 1
                                                FROM activityProgress AS prev_progress
                                                WHERE prev_progress.step = activityProgress.step - 1
                                                  AND prev_progress.documentID = activityProgress.documentID
                                                  AND (
                                                    prev_progress.status = 'Approve' 
                                                    OR prev_progress.status = 'Other advisor approve'
                                                  )
                                            )
                                         )"""
            cursor.execute(query_activity_progress, (id,))
            activity_progress_result = cursor.fetchall()

            query_absence_progress = """SELECT absenceProgress.*, absenceDocument.type
                                        FROM absenceProgress
                                        JOIN absenceDocument ON absenceProgress.documentID = absenceDocument.documentID
                                        WHERE absenceProgress.staffID = %s
                                        AND (
                                            absenceProgress.step = 1
                                            OR EXISTS (
                                                SELECT 1
                                                FROM absenceProgress AS prev_progress
                                                WHERE prev_progress.step = absenceProgress.step - 1
                                                  AND prev_progress.documentID = absenceProgress.documentID
                                                  AND (
                                                    prev_progress.status = 'Approve' 
                                                    OR prev_progress.status = 'Other advisor approve'
                                                  )
                                            )
                                         )"""
            cursor.execute(query_absence_progress, (id,))
            absence_progress_result = cursor.fetchall()

            for r in activity_progress_result + absence_progress_result:
                document_info = {
                    "progessID": r[0],
                    "documentID": r[4],
                    "documentType": r[11],
                    "studentID": r[5],
                    "status": r[6],
                    "comment": r[7],
                    "createDate": r[8],
                    "editDate": r[9]
                }
                all_doc.append(document_info)
            return all_doc

    except HTTPException as e:
        raise e

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


@app.post("/api/document/absence/add")
async def create_absence_doc(form: AbsenceFormCreate):
    try:
        result = await create_absence_document(form)
        return result
    except HTTPException as e:
        raise e


@app.get("/api/userID/{id}/document/absence/detail/{documentID}")
async def get_absence_document_detail(documentID: str, id: str):
    try:
        result = await detail_absence_document(documentID, id)
        return result
    except HTTPException as e:
        raise e


@app.delete("/api/userID/{id}/document/absence/delete/{documentID}")
async def delete_absence_doc(documentID: str, id: str):
    try:
        result = await delete_absence_document(documentID, id)
        return result
    except HTTPException as e:
        raise e


@app.put("/api/userID/{id}/document/absence/edit/{documentID}")
async def delete_absence_doc(documentID: str, id: str, form: AbsenceFormUpdate):
    try:
        result = await update_absence_document(documentID, id, form)
        return result
    except HTTPException as e:
        raise e


@app.put("/api/document/absence/approve")
async def approve_absence_doc(form: ApproveDetail):
    try:
        result = await approve_absence_document(form)
        return result
    except HTTPException as e:
        raise e


@app.put("/api/document/absence/reject")
async def reject_absence_doc(form: RejectDetail):
    try:
        result = await reject_absence_document(form)
        return result
    except HTTPException as e:
        raise e


@app.post("/api/document/activity/add")
async def create_absence_doc(form: ActivityFormCreate):
    try:
        result = await create_activity_document(form)
        return result
    except HTTPException as e:
        raise e


@app.get("/api/userID/{id}/document/activity/detail/{documentID}")
async def get_activity_document_detail(documentID: str, id: str):
    try:
        result = await detail_activity_document(documentID, id)
        return result
    except HTTPException as e:
        raise e


@app.delete("/api/userID/{id}/document/activity/delete/{documentID}")
async def delete_activity_doc(documentID: str, id: str):
    try:
        result = await delete_activity_document(documentID, id)
        return result
    except HTTPException as e:
        raise e


@app.put("/api/userID/{id}/document/activity/edit/{documentID}")
async def delete_activity_doc(documentID: str, id: str, form: ActivityFormUpdate):
    try:
        result = await update_activity_document(documentID, id, form)
        return result
    except HTTPException as e:
        raise e


@app.put("/api/document/activity/approve")
async def approve_activity_doc(form: ApproveDetail):
    try:
        result = await approve_activity_document(form)
        return result
    except HTTPException as e:
        raise e


@app.put("/api/document/activity/reject")
async def reject_activity_doc(form: RejectDetail):
    try:
        result = await reject_activity_document(form)
        return result
    except HTTPException as e:
        raise e