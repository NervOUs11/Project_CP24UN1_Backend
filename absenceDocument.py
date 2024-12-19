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


class AbsenceFormCreate(BaseModel):
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


class AbsenceFormUpdate(BaseModel):
    type: str
    startTime: datetime
    endTime: datetime
    detail: str
    attachmentFile1: Optional[bytes] = None
    attachmentFile2: Optional[bytes] = None
    attachmentFile2Name: Optional[str] = None


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


async def create_absence_document(form: AbsenceFormCreate):
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
                s[7],
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


async def delete_absence_document(documentID: str, id: str):
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


async def update_absence_document(documentID: str, id: str, form: AbsenceFormUpdate):
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