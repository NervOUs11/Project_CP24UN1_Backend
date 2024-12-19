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


class FormUpdate(BaseModel):
    type: str
    startTime: datetime
    endTime: datetime
    detail: str
    attachmentFile1: Optional[bytes] = None
    attachmentFile2: Optional[bytes] = None
    attachmentFile2Name: Optional[str] = None


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


@app.post("/api/document/absence/add")
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

        insert_progress = """INSERT INTO progress (step, staffID, staff_roleID, documentID,
                          studentID, isApprove, createDate, editDate)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        step_count = 0
        main_email_2 = None
        alter_email_2 = None
        if len(all_staff_details) == 4:  # student has 2 advisor
            step = [1, 1, 2, 3]
            main_email_1 = all_staff_details[0][1]  # first advisor main email
            alter_email_1 = all_staff_details[0][6]  # first advisor alter email
            main_email_2 = all_staff_details[1][1]  # second advisor main email
            alter_email_2 = all_staff_details[1][6]  # second advisor alter email
        else:
            step = [1, 2, 3]  # student has 1 advisor
            main_email_1 = all_staff_details[0][1]  # first advisor main email
            alter_email_1 = all_staff_details[0][6]  # first advisor alter email
        for s in all_staff_details:
            cursor.execute(insert_progress, (
                step[step_count],
                s[0],
                s[6],
                document_id,
                form.studentID,
                "Waiting for approve",
                create_date,
                edit_date
            ))
            step_count += 1

        conn.commit()

        # Send email notification
        subject = "New Document to sign."
        body = (f"You have document to sign\n"
                f"From student ID: {form.studentID}\n"
                f"Go to this website: https://capstone24.sit.kmutt.ac.th/un1")

        # If student has 1 advisor (main_email_2 and alter_email_2 is None)
        if main_email_2 is None and alter_email_2 is None:
            email_payload = {
                "primary_recipient": main_email_1,
                "alternate_recipient": alter_email_1,
                "subject": subject,
                "body": body
            }
            await email_notification(EmailSchema(**email_payload))
        # If student has 2 advisor
        else:
            email_payload = {
                "primary_recipient": main_email_1,
                "alternate_recipient": alter_email_1,
                "subject": subject,
                "body": body
            }
            email_payload_2 = {
                "primary_recipient": main_email_2,
                "alternate_recipient": alter_email_2,
                "subject": subject,
                "body": body
            }
            # await email_notification(EmailSchema(**email_payload))
            # await email_notification(EmailSchema(**email_payload_2))

        return {"message": "Created successfully"}, 201

    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Document creation failed: {e}")

    finally:
        cursor.close()
        conn.close()


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
                documentID = p[4]
                if documentID not in progress_by_document:
                    progress_by_document[documentID] = []
                progress_by_document[documentID].append({
                    "status": p[6],
                    "role": p[10]
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
                    WHERE progress.staffID = %s
                    AND (
                     -- Case 1: This is the first step for the document
                     progress.step = 1
                     OR
                     -- Case 2: The previous step was approved
                     EXISTS (
                       SELECT 1
                       FROM progress AS prev_progress
                       WHERE prev_progress.step = progress.step - 1
                         AND prev_progress.documentID = progress.documentID
                         AND (
                            prev_progress.isApprove = 'Approve' 
                            OR
                            prev_progress.isApprove = 'Other advisor approve'
                         )
                     )
                   )"""
            cursor.execute(query, (id, ))
            result = cursor.fetchall()
            for r in result:
                document_info = {
                    "progessID": r[0],
                    "documentID": r[4],
                    "studentID": r[5],
                    "isApprove": r[6],
                    "comment": r[7],
                    "createDate": r[8],
                    "editDate": r[9],
                    "documentType": r[10]
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


@app.get("/api/userID/{id}/document/detail/{documentID}")
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
                "staffID": p[2],
                "staffName": p[10],
                "staffRole": p[11],
                "status": p[6],
                "comment": p[7]
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

    except HTTPException as e:
        raise e

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


@app.put("/api/document/approve")
async def approve(detail: ApproveDetail):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if progressID and documentID exist
        check_query = """SELECT progressID, documentID 
                      FROM progress 
                      WHERE progressID = %s AND documentID = %s"""
        cursor.execute(check_query, (detail.progressID, detail.documentID))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Invalid progressID or documentID")

        # Check if staffID matches progressID and documentID
        staff_check_query = """SELECT staffID 
                            FROM progress 
                            WHERE progressID = %s AND documentID = %s AND staffID = %s"""
        cursor.execute(staff_check_query, (detail.progressID, detail.documentID, detail.staffID))
        staff_match = cursor.fetchone()

        if not staff_match:
            raise HTTPException(status_code=403, detail="Staff does not have the authority to approve this document")

        # Approve form
        update_approve_query = """UPDATE progress
                               SET isApprove = %s
                               WHERE progressID = %s AND staffID = %s AND documentID = %s"""
        cursor.execute(update_approve_query, (
            detail.isApprove,
            detail.progressID,
            detail.staffID,
            detail.documentID
        ))

        # If student has 2 advisor set another advisor isApprove column to "Other advisor approve"
        other_advisor_query = """SELECT progress.staffID, role.roleName 
                              FROM progress
                              JOIN role ON progress.staff_roleID = role.roleID
                              WHERE progress.documentID = %s 
                              AND NOT progress.staffID = %s
                              AND role.roleName NOT IN ('Dean', 'Head of dept')
                              AND  progress.isApprove = 'Waiting for approve'"""
        cursor.execute(other_advisor_query, (detail.documentID, detail.staffID))
        staffID = cursor.fetchone()
        if staffID:
            update_other_approve_query = """UPDATE progress
                                         SET isApprove = %s
                                         WHERE staffID = %s AND documentID = %s;"""
            cursor.execute(update_other_approve_query, (
                "Other advisor approve",
                staffID[0],
                detail.documentID
            ))

        # Send email to notify next staff
        next_staff_query = """SELECT progress.step, progress.studentID, staff.username, staff.alterEmail
                           FROM staff
                           JOIN progress ON staff.staffID = progress.staffID
                           WHERE progress.documentID = %s
                           AND progress.isApprove = 'Waiting for approve'
                           GROUP BY staff.staffID
                           ORDER BY progress.step ASC
                           LIMIT 1"""
        cursor.execute(next_staff_query, (detail.documentID, ))
        next_staff = cursor.fetchone()
        if next_staff:
            subject = "New Document to sign."
            body = (f"You have document to sign\n"
                    f"From student ID: {next_staff[1]}\n"
                    f"Go to this website: https://capstone24.sit.kmutt.ac.th/un1")
            email_payload = {
                "primary_recipient": next_staff[2],
                "alternate_recipient": next_staff[3],
                "subject": subject,
                "body": body
            }
            await email_notification(EmailSchema(**email_payload))

        conn.commit()

        return {"message": "Approve successfully"}

    except HTTPException as e:
        raise e

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


@app.put("/api/document/reject")
async def reject(detail: RejectDetail):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if progressID and documentID exist
        check_query = """SELECT progressID, documentID 
                      FROM progress 
                      WHERE progressID = %s AND documentID = %s"""
        cursor.execute(check_query, (detail.progressID, detail.documentID))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Invalid progressID or documentID")

        # Check if staffID matches progressID and documentID
        staff_check_query = """SELECT staffID 
                            FROM progress 
                            WHERE progressID = %s AND documentID = %s AND staffID = %s"""
        cursor.execute(staff_check_query, (detail.progressID, detail.documentID, detail.staffID))
        staff_match = cursor.fetchone()

        if not staff_match:
            raise HTTPException(status_code=403, detail="Staff does not have the authority to approve this document")

        update_query = """UPDATE progress
                       SET isApprove = %s, comment = %s
                       WHERE progressID = %s AND staffID = %s AND documentID = %s"""
        cursor.execute(update_query, (
            detail.isApprove,
            detail.comment,
            detail.progressID,
            detail.staffID,
            detail.documentID
        ))
        conn.commit()
        return {"message": "Reject successfully"}

    except HTTPException as e:
        raise e

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()


@app.delete("/api/userID/{id}/document/delete/{documentID}")
async def delete(documentID: str, id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        document_check_query = """SELECT * 
                               FROM form 
                               WHERE documentID = %s"""
        cursor.execute(document_check_query, (documentID,))
        document_match = cursor.fetchone()
        if not document_match:
            raise HTTPException(status_code=404, detail="Document not found")

        user_check_query = """SELECT * 
                           FROM form 
                           WHERE studentID = %s AND documentID = %s"""
        cursor.execute(user_check_query, (id, documentID))
        user_match = cursor.fetchone()
        if not user_match:
            raise HTTPException(status_code=403, detail="User do not have permission to delete")

        delete_in_progress = """DELETE FROM progress
                             WHERE studentID = %s AND documentID = %s"""
        cursor.execute(delete_in_progress, (id, documentID))

        delete_in_form = """DELETE FROM form
                         WHERE studentID = %s AND documentID = %s"""
        cursor.execute(delete_in_form, (id, documentID))

        conn.commit()
        return {"message": "Deleted successfully"}

    except HTTPException as e:
        raise e

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


@app.put("/api/userID/{id}/document/edit/{documentID}")
async def update(documentID: str, id: str, form: FormUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        document_check_query = """SELECT * 
                               FROM form 
                               WHERE documentID = %s"""
        cursor.execute(document_check_query, (documentID,))
        document_match = cursor.fetchone()
        if not document_match:
            raise HTTPException(status_code=404, detail="Document not found")

        user_check_query = """SELECT * 
                           FROM form 
                           WHERE studentID = %s AND documentID = %s"""
        cursor.execute(user_check_query, (id, documentID))
        user_match = cursor.fetchone()
        if not user_match:
            raise HTTPException(status_code=403, detail="User do not have permission to edit")

        editDate = datetime.now()
        update_form = """UPDATE form
                      SET type = %s, startTime = %s, endTime = %s, detail = %s, 
                      attachmentFile1 = %s, attachmentFile2 = %s, attachmentFile2Name = %s, editDate = %s
                      WHERE documentID = %s and studentID = %s"""
        cursor.execute(update_form, (
            form.type,
            form.startTime,
            form.endTime,
            form.detail,
            form.attachmentFile1,
            form.attachmentFile2,
            form.attachmentFile2Name,
            editDate,
            documentID,
            id
        ))

        update_progress = """UPDATE progress
                          SET isApprove = %s, editDate = %s
                          WHERE documentID = %s and studentID = %s"""
        cursor.execute(update_progress, (
            "Waiting for approve",
            editDate,
            documentID,
            id
        ))

        conn.commit()
        return {"message": "Edited successfully"}

    except HTTPException as e:
        raise e

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()