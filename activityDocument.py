from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import mysql.connector
from fastapi import HTTPException
from dotenv import load_dotenv
import os
from sendEmail import email_notification, EmailSchema


load_dotenv()
host = os.getenv("DB_HOSTNAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_DATABASE")


class ActivityFormCreate(BaseModel):
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


class ActivityFormUpdate(BaseModel):
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
    status: str = "Approve"


class RejectDetail(BaseModel):
    progressID: int
    staffID: int
    documentID: int
    status: str = "Reject"
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


async def create_activity_document(form: ActivityFormCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        create_date = datetime.now()
        edit_date = create_date
        insert_form = """INSERT INTO absenceDocument (studentID, type, startTime, endTime, detail, attachmentFile1,
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

        insert_progress = """INSERT INTO absenceProgress (step, staffID, staff_roleID, documentID,
                          studentID, status, createDate, editDate)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        step_count = 0
        # main_email_2 = None
        # alter_email_2 = None
        if len(all_staff_details) == 4:  # student has 2 advisor
            step = [1, 1, 2, 3]
            # main_email_1 = all_staff_details[0][1]  # first advisor main email
            # alter_email_1 = all_staff_details[0][6]  # first advisor alter email
            # main_email_2 = all_staff_details[1][1]  # second advisor main email
            # alter_email_2 = all_staff_details[1][6]  # second advisor alter email
        else:
            step = [1, 2, 3]  # student has 1 advisor
            # main_email_1 = all_staff_details[0][1]  # first advisor main email
            # alter_email_1 = all_staff_details[0][6]  # first advisor alter email
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

        # # Send email notification
        # subject = "New Document to sign."
        # body = (f"You have document to sign\n"
        #         f"From student ID: {form.studentID}\n"
        #         f"Go to this website: https://capstone24.sit.kmutt.ac.th/un1")
        #
        # # If student has 1 advisor (main_email_2 and alter_email_2 is None)
        # if main_email_2 is None and alter_email_2 is None:
        #     email_payload = {
        #         "primary_recipient": main_email_1,
        #         "alternate_recipient": alter_email_1,
        #         "subject": subject,
        #         "body": body
        #     }
        #     await email_notification(EmailSchema(**email_payload))
        # # If student has 2 advisor
        # else:
        #     email_payload = {
        #         "primary_recipient": main_email_1,
        #         "alternate_recipient": alter_email_1,
        #         "subject": subject,
        #         "body": body
        #     }
        #     email_payload_2 = {
        #         "primary_recipient": main_email_2,
        #         "alternate_recipient": alter_email_2,
        #         "subject": subject,
        #         "body": body
        #     }
        #     await email_notification(EmailSchema(**email_payload))
        #     await email_notification(EmailSchema(**email_payload_2))

        return {"message": "Created successfully"}, 201

    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Document creation failed: {e}")

    finally:
        cursor.close()
        conn.close()


async def delete_activity_document(documentID: str, id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        document_check_query = """SELECT * 
                               FROM absenceDocument 
                               WHERE documentID = %s"""
        cursor.execute(document_check_query, (documentID,))
        document_match = cursor.fetchone()
        if not document_match:
            raise HTTPException(status_code=404, detail="Document not found")

        user_check_query = """SELECT * 
                           FROM absenceDocument 
                           WHERE studentID = %s AND documentID = %s"""
        cursor.execute(user_check_query, (id, documentID))
        user_match = cursor.fetchone()
        if not user_match:
            raise HTTPException(status_code=403, detail="User do not have permission to delete")

        delete_in_progress = """DELETE FROM absenceProgress
                             WHERE studentID = %s AND documentID = %s"""
        cursor.execute(delete_in_progress, (id, documentID))

        delete_in_form = """DELETE FROM absenceDocument
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


async def update_activity_document(documentID: str, id: str, form: ActivityFormUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        document_check_query = """SELECT * 
                               FROM absenceDocument 
                               WHERE documentID = %s"""
        cursor.execute(document_check_query, (documentID,))
        document_match = cursor.fetchone()
        if not document_match:
            raise HTTPException(status_code=404, detail="Document not found")

        user_check_query = """SELECT * 
                           FROM absenceDocument 
                           WHERE studentID = %s AND documentID = %s"""
        cursor.execute(user_check_query, (id, documentID))
        user_match = cursor.fetchone()
        if not user_match:
            raise HTTPException(status_code=403, detail="User do not have permission to edit")

        editDate = datetime.now()
        update_form = """UPDATE absenceDocument
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

        update_progress = """UPDATE absenceProgress
                          SET status = %s, editDate = %s
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


async def detail_activity_document(documentID: str, id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    progress = []

    try:
        query_form_detail = """SELECT * FROM absenceDocument
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
                              FROM absenceDocument 
                              WHERE documentID = %s AND studentID = %s"""
            cursor.execute(query_authority, (documentID, id))
            authority_result = cursor.fetchone()
        else:
            query_authority = """SELECT progressID 
                              FROM absenceProgress 
                              WHERE documentID = %s AND staffID = %s"""
            cursor.execute(query_authority, (documentID, id))
            authority_result = cursor.fetchone()

        if not authority_result:
            raise HTTPException(status_code=403, detail="You do not have permission to access this document")

        query_progress = """SELECT absenceProgress.*, concat(staff.firstName, " ", staff.lastName), 
                         role.roleName
                         FROM absenceProgress
                         JOIN role ON absenceProgress.staff_roleID = role.roleID
                         JOIN staff ON absenceProgress.staffID = staff.staffID
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


async def approve_activity_document(detail: ApproveDetail):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if progressID and documentID exist
        check_query = """SELECT progressID, documentID 
                      FROM absenceProgress 
                      WHERE progressID = %s AND documentID = %s"""
        cursor.execute(check_query, (detail.progressID, detail.documentID))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Invalid progressID or documentID")

        # Check if staffID matches progressID and documentID
        staff_check_query = """SELECT staffID 
                            FROM absenceProgress 
                            WHERE progressID = %s AND documentID = %s AND staffID = %s"""
        cursor.execute(staff_check_query, (detail.progressID, detail.documentID, detail.staffID))
        staff_match = cursor.fetchone()

        if not staff_match:
            raise HTTPException(status_code=403, detail="Staff does not have the authority to approve this document")

        # Approve form
        update_approve_query = """UPDATE absenceProgress
                               SET status = %s
                               WHERE progressID = %s AND staffID = %s AND documentID = %s"""
        cursor.execute(update_approve_query, (
            detail.status,
            detail.progressID,
            detail.staffID,
            detail.documentID
        ))

        # If student has 2 advisor set another advisor status column to "Other advisor approve"
        other_advisor_query = """SELECT absenceProgress.staffID, role.roleName 
                              FROM absenceProgress
                              JOIN role ON absenceProgress.staff_roleID = role.roleID
                              WHERE absenceProgress.documentID = %s 
                              AND NOT absenceProgress.staffID = %s
                              AND role.roleName NOT IN ('Dean', 'Head of dept')
                              AND  absenceProgress.status = 'Waiting for approve'"""
        cursor.execute(other_advisor_query, (detail.documentID, detail.staffID))
        staffID = cursor.fetchone()
        if staffID:
            update_other_approve_query = """UPDATE absenceProgress
                                         SET status = %s
                                         WHERE staffID = %s AND documentID = %s;"""
            cursor.execute(update_other_approve_query, (
                "Other advisor approve",
                staffID[0],
                detail.documentID
            ))

        # Send email to notify next staff
        # next_staff_query = """SELECT absenceProgress.step, absenceProgress.studentID, staff.username, staff.email
        #                    FROM staff
        #                    JOIN absenceProgress ON staff.staffID = absenceProgress.staffID
        #                    WHERE absenceProgress.documentID = %s
        #                    AND absenceProgress.status = 'Waiting for approve'
        #                    GROUP BY staff.staffID
        #                    ORDER BY absenceProgress.step ASC
        #                    LIMIT 1"""
        # cursor.execute(next_staff_query, (detail.documentID, ))
        # next_staff = cursor.fetchone()
        # if next_staff:
        #     subject = "New Document to sign."
        #     body = (f"You have document to sign\n"
        #             f"From student ID: {next_staff[1]}\n"
        #             f"Go to this website: https://capstone24.sit.kmutt.ac.th/un1")
        #     email_payload = {
        #         "primary_recipient": next_staff[2],
        #         "alternate_recipient": next_staff[3],
        #         "subject": subject,
        #         "body": body
        #     }
        #     await email_notification(EmailSchema(**email_payload))

        conn.commit()

        return {"message": "Approve successfully"}

    except HTTPException as e:
        raise e

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


async def reject_activity_document(detail: RejectDetail):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if progressID and documentID exist
        check_query = """SELECT progressID, documentID 
                      FROM absenceProgress 
                      WHERE progressID = %s AND documentID = %s"""
        cursor.execute(check_query, (detail.progressID, detail.documentID))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Invalid progressID or documentID")

        # Check if staffID matches progressID and documentID
        staff_check_query = """SELECT staffID 
                            FROM absenceProgress 
                            WHERE progressID = %s AND documentID = %s AND staffID = %s"""
        cursor.execute(staff_check_query, (detail.progressID, detail.documentID, detail.staffID))
        staff_match = cursor.fetchone()

        if not staff_match:
            raise HTTPException(status_code=403, detail="Staff does not have the authority to approve this document")

        update_query = """UPDATE absenceProgress
                       SET status = %s, comment = %s
                       WHERE progressID = %s AND staffID = %s AND documentID = %s"""
        cursor.execute(update_query, (
            detail.status,
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