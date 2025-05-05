from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import mysql.connector
from fastapi import HTTPException
from dotenv import load_dotenv
import os


load_dotenv()
host = os.getenv("DB_HOSTNAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_DATABASE")


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


async def get_all_user():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query_all_staff = """SELECT staff.staffID, staff.username,
                          concat(staff.firstName, " ", staff.lastName) AS fullname,
                          staff.tel, staff.email, role.roleName, faculty.facultyName,
                          department.departmentName, club.clubName
                          FROM staff
                          JOIN role ON staff.roleID = role.roleID
                          JOIN faculty ON staff.facultyID = faculty.facultyID
                          JOIN department ON staff.departmentID = department.departmentID
                          LEFT JOIN club ON staff.clubID = club.clubID"""
        cursor.execute(query_all_staff)
        all_staff = cursor.fetchall()
        staff_result = [{"staffID": record[0], "username": record[1],
                         "name": record[2], "tel": record[3],
                         "email": record[4], "role": record[5],
                         "faculty": record[6], "department": record[7],
                         "club": record[8]} for record in all_staff]

        query_all_student = """SELECT student.studentID, student.username, 
                            concat(student.firstName, " ", student.lastName) AS fullname,
                            student.tel, student.email, student.year, 
                            faculty.facultyName, department.departmentName,
                            student.currentGPA, student.cumulativeGPA, club.clubName
                            FROM student
                            JOIN faculty ON student.facultyID = faculty.facultyID
                            JOIN department ON student.departmentID = department.departmentID
                            LEFT JOIN club ON student.clubID = club.clubID"""
        cursor.execute(query_all_student)
        all_student = cursor.fetchall()
        student_result = [{"studentID": record[0], "username": record[1],
                           "name": record[2], "tel": record[3],
                           "email": record[4], "year": record[5],
                           "faculty": record[6], "department": record[7],
                           "currentGPA": record[8], "cumulativeGPA": record[9],
                           "club": record[10]} for record in all_student]

        all_user_result = staff_result + student_result

        if not all_user_result:
            raise HTTPException(status_code=404, detail="No users found")

        return all_user_result

    except HTTPException as e:
        raise e

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()