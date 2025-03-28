from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Optional, List, Tuple
import mysql.connector
from fastapi import HTTPException
from dotenv import load_dotenv
import os
from sendEmail import send_email, EmailSchema
from fastapi.responses import JSONResponse

load_dotenv()
host = os.getenv("DB_HOSTNAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_DATABASE")


class ActivityFormCreate(BaseModel):
    studentID: int
    type: str
    startTime: datetime
    endTime: datetime
    code: str
    departmentName: str
    title: str
    location: str
    propose: str
    payment: float
    staffID: int
    sustainabilityDetail: str
    sustainabilityPropose: str
    activityCharacteristic: str
    codeOfHonor: str
    prepareStart: datetime
    prepareEnd: datetime
    prepareFile: Optional[bytes] = "None"
    evaluationFile: Optional[bytes] = "None"
    budgetDetails: Optional[bytes] = "None"
    scheduleDetails: Optional[bytes] = "None"
    participant: List[Tuple[int, int]] = []                  # [(participantID, count)]
    activity: List[Tuple[int, int]] = []                     # [(activityID, countHour)]
    problem: List[Tuple[str, str]] = []                      # [(problemDetail, solution)]
    studentQF: List[Tuple[int, int]] = []                    # [studentQF_ID, percentage]
    entrepreneurial: List[int] = []                          # [entrepreneurialID]
    evaluation: List[Tuple[int, Optional[str]]] = []         # [(evaluationID, otherEvaluationName)]
    result: List[Tuple[str, str, str]] = []                  # [(kpi, detail, target)]
    sustainability: List[Tuple[int, Optional[int]]] = []     # [sustainabilityID, goalID]
    committee: List[Tuple[int, str]] = []                    # [studentID, position]
    staffIDProgress2: int                                    # นายก/ประธานชมรม
    staffIDProgress3: int                                    # ประธานฝ่าย


class ActivityFormUpdate(BaseModel):
    type: str
    startTime: datetime
    endTime: datetime
    code: str
    departmentName: str
    title: str
    location: str
    propose: str
    payment: float
    sustainabilityDetail: str
    sustainabilityPropose: str
    activityCharacteristic: str
    codeOfHonor: str
    prepareStart: datetime
    prepareEnd: datetime
    prepareFile: Optional[bytes] = "None"
    evaluationFile: Optional[bytes] = "None"
    budgetDetails: Optional[bytes] = "None"
    scheduleDetails: Optional[bytes] = "None"
    participant: List[Tuple[int, int]] = []                 # [(participantID, count)]
    activity: List[Tuple[int, int]] = []                    # [(activityID, countHour)]
    problem: List[Tuple[str, str]] = []                     # [(problemDetail, solution)]
    studentQF: List[Tuple[int, int]] = []                    # [studentQF_ID, percentage]
    entrepreneurial: List[int] = []                         # [entrepreneurialID]
    evaluation: List[Tuple[int, Optional[str]]] = []        # [(evaluationID, otherEvaluationName)]
    result: List[Tuple[str, str, str]] = []                 # [(kpi, detail, target)]
    sustainability: List[Tuple[int, Optional[int]]] = []    # [sustainabilityID, goalID]
    committee: List[Tuple[int, str]] = []                   # [studentID, position]


class ActivityApproveDetail(BaseModel):
    progressID: int
    staffID: int
    documentID: int
    status: str = "Approve"


class ActivityRejectDetail(BaseModel):
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


class ActivityDocumentService:
    @staticmethod
    async def get_participant():
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query_all_participant = """SELECT * FROM participant"""
            cursor.execute(query_all_participant)
            all_participant = cursor.fetchall()
            if not all_participant:
                raise HTTPException(status_code=404, detail="Participant not found")
            participant_result = [{"participantID": record[0],
                                   "participantName": record[1]}
                                  for record in all_participant]
            return participant_result

        except mysql.connector.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    async def get_studentQF():
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query_all_studentQF = """SELECT * FROM studentQF"""
            cursor.execute(query_all_studentQF)
            all_studentQF = cursor.fetchall()
            if not all_studentQF:
                raise HTTPException(status_code=404, detail="StudentQF not found")
            studentQF_result = [{"studentQF_ID": record[0],
                                 "studentQF_Name": record[1]}
                                for record in all_studentQF]
            return studentQF_result

        except mysql.connector.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    async def get_entrepreneurial():
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query_all_entrepreneurial = """SELECT * FROM entrepreneurial"""
            cursor.execute(query_all_entrepreneurial)
            all_entrepreneurial = cursor.fetchall()
            if not all_entrepreneurial:
                raise HTTPException(status_code=404, detail="Entrepreneurial not found")
            entrepreneurial_result = [{"entrepreneurialID": record[0],
                                       "entrepreneurialName": record[1]}
                                      for record in all_entrepreneurial]
            return entrepreneurial_result

        except mysql.connector.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    async def get_evaluation():
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query_all_entrepreneurial = """SELECT * FROM evaluation"""
            cursor.execute(query_all_entrepreneurial)
            all_evaluation = cursor.fetchall()
            if not all_evaluation:
                raise HTTPException(status_code=404, detail="Evaluation not found")
            evaluation_result = [{"evaluationID": record[0],
                                  "evaluationName": record[1]}
                                 for record in all_evaluation]
            return evaluation_result

        except mysql.connector.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    async def get_activity():
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query_all_activity = """SELECT * FROM activity"""
            cursor.execute(query_all_activity)
            all_activity = cursor.fetchall()
            if not all_activity:
                raise HTTPException(status_code=404, detail="Activity not found")
            activity_result = [{"activityID": record[0],
                                "activityName": record[1]}
                               for record in all_activity]
            return activity_result

        except mysql.connector.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    async def get_sustainability():
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query_all_sustainability = """SELECT * FROM sustainability"""
            cursor.execute(query_all_sustainability)
            all_sustainability = cursor.fetchall()
            if not all_sustainability:
                raise HTTPException(status_code=404, detail="Sustainability not found")
            sustainability_result = [{"sustainabilityID": record[0],
                                      "sustainabilityName": record[1]}
                                     for record in all_sustainability]
            return sustainability_result

        except mysql.connector.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    async def get_goal():
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query_all_goal = """SELECT * FROM goal"""
            cursor.execute(query_all_goal)
            all_goal = cursor.fetchall()
            if not all_goal:
                raise HTTPException(status_code=404, detail="Goal not found")
            goal_result = [{"goalID": record[0],
                            "goalName": record[1]}
                           for record in all_goal]
            return goal_result

        except mysql.connector.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    async def get_staff():
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query_all_staff = """SELECT staff.*, role.roleName
                              FROM staff JOIN role ON staff.roleID = role.roleID"""
            cursor.execute(query_all_staff)
            all_staff = cursor.fetchall()
            if not all_staff:
                raise HTTPException(status_code=404, detail="Staff not found")
            return all_staff

        except mysql.connector.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    async def get_student():
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query_all_student = """SELECT student.studentID, concat(student.firstName, " ", student.lastName),
                                department.departmentName, student.year, student.tel
                                FROM student JOIN department ON student.departmentID = department.departmentID"""
            cursor.execute(query_all_student)
            all_student = cursor.fetchall()
            if not all_student:
                raise HTTPException(status_code=404, detail="Student not found")
            return all_student

        except mysql.connector.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    async def get_faculty():
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query_all_faculty = """SELECT * FROM faculty"""
            cursor.execute(query_all_faculty)
            all_faculty = cursor.fetchall()
            if not all_faculty:
                raise HTTPException(status_code=404, detail="Faculty not found")
            faculty_result = [{"facultyID": record[0],
                               "facultyName": record[1]}
                              for record in all_faculty]
            return faculty_result

        except mysql.connector.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    async def get_club():
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query_all_club = """SELECT * FROM club"""
            cursor.execute(query_all_club)
            all_club = cursor.fetchall()
            if not all_club:
                raise HTTPException(status_code=404, detail="Club not found")
            club_result = [{"clubID": record[0],
                            "clubName": record[1]}
                           for record in all_club]
            return club_result

        except mysql.connector.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

        finally:
            cursor.close()
            conn.close()

    async def create_activity_document(form: ActivityFormCreate):
        conn = get_db_connection()
        cursor = conn.cursor()
        form.startTime = form.startTime.astimezone(timezone.utc)
        form.endTime = form.endTime.astimezone(timezone.utc)
        form.prepareStart = form.prepareStart.astimezone(timezone.utc)
        form.prepareEnd = form.prepareEnd.astimezone(timezone.utc)

        try:
            create_date = datetime.now(timezone.utc)
            edit_date = create_date
            insert_form = """INSERT INTO activityDocument (studentID, type, startTime, endTime, createDate, editDate,
                          code, departmentName, title, location, propose, payment, staffID, sustainabilityDetail,
                          sustainabilityPropose, activityCharacteristic, codeOfHonor, prepareStart, prepareEnd,
                          prepareFile, evaluationFile, budgetDetail, scheduleDetail)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_form, (
                form.studentID,
                form.type,
                form.startTime,
                form.endTime,
                create_date,
                edit_date,
                form.code,
                form.departmentName,
                form.title,
                form.location,
                form.propose,
                form.payment,
                form.staffID,
                form.sustainabilityDetail,
                form.sustainabilityPropose,
                form.activityCharacteristic,
                form.codeOfHonor,
                form.prepareStart,
                form.prepareEnd,
                form.prepareFile,
                form.evaluationFile,
                form.budgetDetails,
                form.scheduleDetails
            ))
            document_id = cursor.lastrowid

            # check activityID in table activity and insert into document_activity table
            for activity in form.activity:
                check_activity_query = """SELECT * FROM activity WHERE activityID = %s"""
                cursor.execute(check_activity_query, (activity[0],))
                activity_result = cursor.fetchone()
                if not activity_result:
                    raise HTTPException(status_code=404, detail="Activity not found")
                insert_activity_query = """INSERT INTO document_activity (documentID, activityID, countHour)
                                        VALUES (%s, %s, %s)"""
                cursor.execute(insert_activity_query, (document_id, activity[0], activity[1]))

            # check participantID in table participant and insert into document_participant table
            for participant in form.participant:
                check_participant_query = """SELECT * FROM participant WHERE participantID = %s"""
                cursor.execute(check_participant_query, (participant[0],))
                participant_result = cursor.fetchone()
                if not participant_result:
                    raise HTTPException(status_code=404, detail="Participant not found")
                insert_participant_query = """INSERT INTO document_participant (documentID, participantID, count)
                                          VALUES (%s, %s, %s)"""
                cursor.execute(insert_participant_query, (document_id, participant[0], participant[1]))

            # insert problem into problem table
            for problem in form.problem:
                insert_problem_query = """INSERT INTO problem (documentID, problemDetail, solution)
                                     VALUES (%s, %s, %s)"""
                cursor.execute(insert_problem_query, (document_id, problem[0], problem[1]))

            # check studentQF_ID in table studentQF and insert into document_studentQF table
            for studentQF in form.studentQF:
                check_studentQF_query = """SELECT * FROM studentQF WHERE student_QF_ID = %s"""
                cursor.execute(check_studentQF_query, (studentQF[0],))
                studentQF_result = cursor.fetchone()
                if not studentQF_result:
                    raise HTTPException(status_code=404, detail="StudentQF not found")
                insert_studentQF_query = """INSERT INTO document_studentQF (documentID, student_QF_ID, percentage)
                                       VALUES (%s, %s, %s)"""
                cursor.execute(insert_studentQF_query, (document_id, studentQF[0], studentQF[1]))

            # check entrepreneurialID in table entrepreneurial and insert into document_entrepreneurial table
            for entrepreneurial in form.entrepreneurial:
                check_entrepreneurial_query = """SELECT * FROM entrepreneurial WHERE entrepreneurialID = %s"""
                cursor.execute(check_entrepreneurial_query, (entrepreneurial,))
                entrepreneurial_result = cursor.fetchone()
                if not entrepreneurial_result:
                    raise HTTPException(status_code=404, detail="Entrepreneurial not found")
                insert_entrepreneurial_query = """INSERT INTO document_entrepreneurial (documentID, entrepreneurialID)
                                             VALUES (%s, %s)"""
                cursor.execute(insert_entrepreneurial_query, (document_id, entrepreneurial))

            # check evaluationID in table evaluation and insert into document_evaluation table
            for evaluation in form.evaluation:
                check_evaluation_query = """SELECT * FROM evaluation WHERE evaluationID = %s"""
                cursor.execute(check_evaluation_query, (evaluation[0],))
                evaluation_result = cursor.fetchone()
                if not evaluation_result:
                    raise HTTPException(status_code=404, detail="Evaluation not found")
                insert_evaluation_query = """INSERT INTO document_evaluation (documentID, evaluationID, otherEvaluationName)
                                         VALUES (%s, %s, %s)"""
                cursor.execute(insert_evaluation_query, (document_id, evaluation[0], evaluation[1]))

            # insert result into result table
            for result in form.result:
                insert_result_query = """INSERT INTO result (documentID, kpi, detail, target)
                                   VALUES (%s, %s, %s, %s)"""
                cursor.execute(insert_result_query, (document_id, result[0], result[1], result[2]))

            # check sustainabilityID in table sustainability and goalID in table goal
            # then insert into document_sustainability table
            for sustainability in form.sustainability:
                check_sustainability_query = """SELECT * FROM sustainability WHERE sustainabilityID = %s"""
                cursor.execute(check_sustainability_query, (sustainability[0],))
                sustainability_result = cursor.fetchone()
                if not sustainability_result:
                    raise HTTPException(status_code=404, detail="Sustainability not found")
                if sustainability[1] is not None:
                    check_goal_query = """SELECT * FROM goal WHERE goalID = %s"""
                    cursor.execute(check_goal_query, (sustainability[1],))
                    goal_result = cursor.fetchone()
                    if not goal_result:
                        raise HTTPException(status_code=404, detail="Goal not found")
                insert_sustainability_query = """INSERT INTO document_sustainability (documentID, sustainabilityID, goalID)
                                            VALUES (%s, %s, %s)"""
                cursor.execute(insert_sustainability_query, (document_id, sustainability[0], sustainability[1]))

            # check studentID in table student and insert into document_committee table
            for committee in form.committee:
                check_student_query = """SELECT * FROM student WHERE studentID = %s"""
                cursor.execute(check_student_query, (committee[0],))
                student_result = cursor.fetchone()
                if not student_result:
                    raise HTTPException(status_code=404, detail="Student not found")
                insert_committee_query = """INSERT INTO student_committee (documentID, studentID, position)
                                     VALUES (%s, %s, %s)"""
                cursor.execute(insert_committee_query, (document_id, committee[0], committee[1]))

            # insert progress 1 into activityProgress table
            role_query = """SELECT roleID FROM staff WHERE staffID = %s"""
            cursor.execute(role_query, (form.staffID,))
            roleID_result = cursor.fetchone()
            if not roleID_result:
                raise HTTPException(status_code=404, detail="Role not found")

            insert_step_one_progress = """INSERT INTO activityProgress (step, staffID, staff_roleID, documentID,
                                       studentID, status, createDate, editDate)
                                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_step_one_progress, (
                1,
                form.staffID,
                roleID_result[0],
                document_id,
                form.studentID,
                "Waiting for approve",
                create_date,
                edit_date
            ))

            # insert progress 2 into activityProgress table
            role_query = """SELECT roleID FROM staff WHERE staffID = %s"""
            cursor.execute(role_query, (form.staffIDProgress2,))
            roleID_result = cursor.fetchone()
            if not roleID_result:
                raise HTTPException(status_code=404, detail="Role not found")

            insert_step_two_progress = """INSERT INTO activityProgress (step, staffID, staff_roleID, documentID,
                                       studentID, status, createDate, editDate)
                                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_step_two_progress, (
                2,
                form.staffIDProgress2,
                roleID_result[0],
                document_id,
                form.studentID,
                "Waiting for approve",
                create_date,
                edit_date
            ))

            # insert progress 3 into activityProgress table
            role_query = """SELECT roleID FROM staff WHERE staffID = %s"""
            cursor.execute(role_query, (form.staffIDProgress3,))
            roleID_result = cursor.fetchone()
            if not roleID_result:
                raise HTTPException(status_code=404, detail="Role not found")

            insert_step_three_progress = """INSERT INTO activityProgress (step, staffID, staff_roleID, documentID,
                                         studentID, status, createDate, editDate)
                                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_step_three_progress, (
                3,
                form.staffIDProgress3,
                roleID_result[0],
                document_id,
                form.studentID,
                "Waiting for approve",
                create_date,
                edit_date
            ))

            fixed_staff_query = """SELECT staff.username, staff.staffID, staff.roleID, role.roleName 
                                FROM staff 
                                JOIN role ON staff.roleID = role.roleID
                                WHERE role.roleName = 'President of the Student Organization' 
                                OR role.roleName = 'Vice President of the Student Council'
                                OR role.roleName = 'President of Student Council'
                                OR role.roleName = 'Educational Service Provider'
                                OR role.roleName = 'Director of Student Affairs Office'
                                OR role.roleName = 'Vice President for Student and Learning Development'"""
            cursor.execute(fixed_staff_query)
            fixed_staff = cursor.fetchall()

            for staff in fixed_staff:
                step = 0
                insert_progress = """INSERT INTO activityProgress (step, staffID, staff_roleID, documentID,
                                  studentID, status, createDate, editDate)
                                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                if staff[3] == "President of the Student Organization":
                    step = 4
                elif staff[3] == "Vice President of the Student Council":
                    step = 5
                elif staff[3] == "President of Student Council":
                    step = 6
                elif staff[3] == "Educational Service Provider":
                    step = 7
                elif staff[3] == "Director of Student Affairs Office":
                    step = 8
                elif staff[3] == "Vice President for Student and Learning Development":
                    step = 9
                cursor.execute(insert_progress, (
                    step,
                    staff[1],
                    staff[2],
                    document_id,
                    form.studentID,
                    "Waiting for approve",
                    create_date,
                    edit_date
                ))

            conn.commit()

            # Send email notification
            staff_email_query = """SELECT staff.email FROM staff
                                JOIN activityProgress ON staff.staffID = activityProgress.staffID
                                WHERE activityProgress.documentID = %s AND activityProgress.step = 1"""
            cursor.execute(staff_email_query, (document_id,))
            staff_email = cursor.fetchone()

            subject = "New Activity Document to sign."
            body = (f"You have document to sign.\n"
                    f"Go to this website: https://capstone24.sit.kmutt.ac.th/un1")
            email_payload = {
                "email": staff_email[0],
                "subject": subject,
                "body": body
            }
            await send_email(EmailSchema(**email_payload))

            return JSONResponse(content={"message": "Created successfully"}, status_code=201)

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
                                   FROM activityDocument 
                                   WHERE documentID = %s"""
            cursor.execute(document_check_query, (documentID,))
            document_match = cursor.fetchone()
            if not document_match:
                raise HTTPException(status_code=404, detail="Document not found")

            user_check_query = """SELECT * 
                               FROM activityDocument 
                               WHERE studentID = %s AND documentID = %s"""
            cursor.execute(user_check_query, (id, documentID))
            user_match = cursor.fetchone()
            if not user_match:
                raise HTTPException(status_code=403, detail="User do not have permission to delete")

            delete_activity = """DELETE FROM document_activity WHERE documentID = %s;"""
            cursor.execute(delete_activity, (documentID,))

            delete_participant = """DELETE FROM document_participant WHERE documentID = %s;"""
            cursor.execute(delete_participant, (documentID,))

            delete_problem = """DELETE FROM problem WHERE documentID = %s;"""
            cursor.execute(delete_problem, (documentID,))

            delete_studentQF = """DELETE FROM document_studentQF WHERE documentID = %s;"""
            cursor.execute(delete_studentQF, (documentID,))

            delete_entrepreneurial = """DELETE FROM document_entrepreneurial WHERE documentID = %s;"""
            cursor.execute(delete_entrepreneurial, (documentID,))

            delete_evaluation = """DELETE FROM document_evaluation WHERE documentID = %s;"""
            cursor.execute(delete_evaluation, (documentID,))

            delete_result = """DELETE FROM result WHERE documentID = %s;"""
            cursor.execute(delete_result, (documentID,))

            delete_sustainability = """DELETE FROM document_sustainability WHERE documentID = %s;"""
            cursor.execute(delete_sustainability, (documentID,))

            delete_committee = """DELETE FROM student_committee WHERE documentID = %s;"""
            cursor.execute(delete_committee, (documentID,))

            delete_in_progress = """DELETE FROM activityProgress WHERE studentID = %s AND documentID = %s"""
            cursor.execute(delete_in_progress, (id, documentID))

            delete_in_form = """DELETE FROM activityDocument WHERE studentID = %s AND documentID = %s"""
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
        form.startTime = form.startTime.astimezone(timezone.utc)
        form.endTime = form.endTime.astimezone(timezone.utc)
        form.prepareStart = form.prepareStart.astimezone(timezone.utc)
        form.prepareEnd = form.prepareEnd.astimezone(timezone.utc)

        try:
            document_check_query = """SELECT * 
                                   FROM activityDocument 
                                   WHERE documentID = %s"""
            cursor.execute(document_check_query, (documentID,))
            document_match = cursor.fetchone()
            if not document_match:
                raise HTTPException(status_code=404, detail="Document not found")

            user_check_query = """SELECT * 
                               FROM activityDocument 
                               WHERE studentID = %s AND documentID = %s"""
            cursor.execute(user_check_query, (id, documentID))
            user_match = cursor.fetchone()
            if not user_match:
                raise HTTPException(status_code=403, detail="User do not have permission to edit")

            editDate = datetime.now(timezone.utc)
            update_form = """UPDATE activityDocument
                          SET type = %s, startTime = %s, endTime = %s, code = %s, departmentName = %s, title = %s,
                          location = %s, propose = %s, payment = %s, sustainabilityDetail = %s, sustainabilityPropose = %s,
                          activityCharacteristic = %s, codeOfHonor = %s, prepareStart = %s, prepareEnd = %s, prepareFile = %s,
                          evaluationFile = %s, budgetDetail = %s, scheduleDetail = %s, editDate = %s
                          WHERE documentID = %s and studentID = %s"""
            cursor.execute(update_form, (
                form.type,
                form.startTime,
                form.endTime,
                form.code,
                form.departmentName,
                form.title,
                form.location,
                form.propose,
                form.payment,
                form.sustainabilityDetail,
                form.sustainabilityPropose,
                form.activityCharacteristic,
                form.codeOfHonor,
                form.prepareStart,
                form.prepareEnd,
                form.prepareFile,
                form.evaluationFile,
                form.budgetDetails,
                form.scheduleDetails,
                editDate,
                documentID,
                id
            ))

            # edit participant in document_participant table
            delete_participant = """DELETE FROM document_participant WHERE documentID = %s"""
            cursor.execute(delete_participant, (documentID,))
            for participant in form.participant:
                check_participant_query = """SELECT * FROM participant WHERE participantID = %s"""
                cursor.execute(check_participant_query, (participant[0],))
                participant_result = cursor.fetchone()
                if not participant_result:
                    raise HTTPException(status_code=404, detail="Participant not found")
                insert_participant_query = """INSERT INTO document_participant (documentID, participantID, count)
                                           VALUES (%s, %s, %s)"""
                cursor.execute(insert_participant_query, (documentID, participant[0], participant[1]))

            # edit activity in document_activity table
            delete_activity = """DELETE FROM document_activity WHERE documentID = %s"""
            cursor.execute(delete_activity, (documentID,))
            for activity in form.activity:
                check_activity_query = """SELECT * FROM activity WHERE activityID = %s"""
                cursor.execute(check_activity_query, (activity[0],))
                activity_result = cursor.fetchone()
                if not activity_result:
                    raise HTTPException(status_code=404, detail="Activity not found")
                insert_activity_query = """INSERT INTO document_activity (documentID, activityID, countHour)
                                        VALUES (%s, %s, %s)"""
                cursor.execute(insert_activity_query, (documentID, activity[0], activity[1]))

            # edit problem in problem table
            delete_problem = """DELETE FROM problem WHERE documentID = %s"""
            cursor.execute(delete_problem, (documentID,))
            for problem in form.problem:
                insert_problem_query = """INSERT INTO problem (documentID, problemDetail, solution)
                                       VALUES (%s, %s, %s)"""
                cursor.execute(insert_problem_query, (documentID, problem[0], problem[1]))

            # edit studentQF in document_studentQF table
            delete_studentQF = """DELETE FROM document_studentQF WHERE documentID = %s"""
            cursor.execute(delete_studentQF, (documentID,))
            for studentQF in form.studentQF:
                check_studentQF_query = """SELECT * FROM studentQF WHERE student_QF_ID = %s"""
                cursor.execute(check_studentQF_query, (studentQF[0],))
                studentQF_result = cursor.fetchone()
                if not studentQF_result:
                    raise HTTPException(status_code=404, detail="StudentQF not found")
                insert_studentQF_query = """INSERT INTO document_studentQF (documentID, student_QF_ID, percentage)
                                         VALUES (%s, %s, %s)"""
                cursor.execute(insert_studentQF_query, (documentID, studentQF[0], studentQF[1]))

            # edit entrepreneurial in document_entrepreneurial table
            delete_entrepreneurial = """DELETE FROM document_entrepreneurial WHERE documentID = %s"""
            cursor.execute(delete_entrepreneurial, (documentID,))
            for entrepreneurial in form.entrepreneurial:
                check_entrepreneurial_query = """SELECT * FROM entrepreneurial WHERE entrepreneurialID = %s"""
                cursor.execute(check_entrepreneurial_query, (entrepreneurial,))
                entrepreneurial_result = cursor.fetchone()
                if not entrepreneurial_result:
                    raise HTTPException(status_code=404, detail="Entrepreneurial not found")
                insert_entrepreneurial_query = """INSERT INTO document_entrepreneurial (documentID, entrepreneurialID)
                                             VALUES (%s, %s)"""
                cursor.execute(insert_entrepreneurial_query, (documentID, entrepreneurial))

            # edit evaluation in document_evaluation table
            delete_evaluation = """DELETE FROM document_evaluation WHERE documentID = %s"""
            cursor.execute(delete_evaluation, (documentID,))
            for evaluation in form.evaluation:
                check_evaluation_query = """SELECT * FROM evaluation WHERE evaluationID = %s"""
                cursor.execute(check_evaluation_query, (evaluation[0],))
                evaluation_result = cursor.fetchone()
                if not evaluation_result:
                    raise HTTPException(status_code=404, detail="Evaluation not found")
                insert_evaluation_query = """INSERT INTO document_evaluation (documentID, evaluationID, otherEvaluationName)
                                         VALUES (%s, %s, %s)"""
                cursor.execute(insert_evaluation_query, (documentID, evaluation[0], evaluation[1]))

            # edit result in result table
            delete_result = """DELETE FROM result WHERE documentID = %s"""
            cursor.execute(delete_result, (documentID,))
            for result in form.result:
                insert_result_query = """INSERT INTO result (documentID, kpi, detail, target)
                                   VALUES (%s, %s, %s, %s)"""
                cursor.execute(insert_result_query, (documentID, result[0], result[1], result[2]))

            # edit sustainability in document_sustainability table
            delete_sustainability = """DELETE FROM document_sustainability WHERE documentID = %s"""
            cursor.execute(delete_sustainability, (documentID,))
            for sustainability in form.sustainability:
                check_sustainability_query = """SELECT * FROM sustainability WHERE sustainabilityID = %s"""
                cursor.execute(check_sustainability_query, (sustainability[0],))
                sustainability_result = cursor.fetchone()
                if not sustainability_result:
                    raise HTTPException(status_code=404, detail="Sustainability not found")
                if sustainability[1] is not None:
                    check_goal_query = """SELECT * FROM goal WHERE goalID = %s"""
                    cursor.execute(check_goal_query, (sustainability[1],))
                    goal_result = cursor.fetchone()
                    if not goal_result:
                        raise HTTPException(status_code=404, detail="Goal not found")
                insert_sustainability_query = """INSERT INTO document_sustainability (documentID, sustainabilityID, goalID)
                                            VALUES (%s, %s, %s)"""
                cursor.execute(insert_sustainability_query, (documentID, sustainability[0], sustainability[1]))

            # edit committee in student_committee table
            delete_committee = """DELETE FROM student_committee WHERE documentID = %s"""
            cursor.execute(delete_committee, (documentID,))
            for committee in form.committee:
                check_student_query = """SELECT * FROM student WHERE studentID = %s"""
                cursor.execute(check_student_query, (committee[0],))
                student_result = cursor.fetchone()
                if not student_result:
                    raise HTTPException(status_code=404, detail="Student not found")
                insert_committee_query = """INSERT INTO student_committee (documentID, studentID, position)
                                     VALUES (%s, %s, %s)"""
                cursor.execute(insert_committee_query, (documentID, committee[0], committee[1]))

            update_progress = """UPDATE activityProgress
                              SET status = %s, editDate = %s
                              WHERE documentID = %s and studentID = %s"""
            cursor.execute(update_progress, (
                "Waiting for approve",
                editDate,
                documentID,
                id
            ))

            conn.commit()

            # Send email notification
            staff_email_query = """SELECT staff.email FROM staff
                                        JOIN activityProgress ON staff.staffID = activityProgress.staffID
                                        WHERE activityProgress.documentID = %s AND activityProgress.step = 1"""
            cursor.execute(staff_email_query, (documentID,))
            staff_email = cursor.fetchone()

            subject = "New Activity Document to sign."
            body = (f"You have document to sign.\n"
                    f"Go to this website: https://capstone24.sit.kmutt.ac.th/un1")
            email_payload = {
                "email": staff_email[0],
                "subject": subject,
                "body": body
            }
            await send_email(EmailSchema(**email_payload))

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
            query_form_detail = """SELECT * FROM activityDocument WHERE documentID = %s"""
            cursor.execute(query_form_detail, (documentID,))
            detail_result = cursor.fetchone()
            if not detail_result:
                raise HTTPException(status_code=404, detail="Document not found")

            query_doc_owner = """SELECT student.*, faculty.facultyName, department.departmentName, club.clubName
                              FROM student 
                              JOIN faculty ON student.facultyID = faculty.facultyID
                              JOIN department ON student.departmentID = department.departmentID
                              JOIN club ON student.clubID = club.clubID
                              WHERE studentID = %s"""
            cursor.execute(query_doc_owner, (detail_result[1],))
            doc_owner = cursor.fetchone()

            query_participant = """SELECT participant.participantName, document_participant.count 
                                FROM participant 
                                JOIN document_participant 
                                ON participant.participantID = document_participant.participantID
                                WHERE document_participant.documentID = %s"""
            cursor.execute(query_participant, (documentID,))
            participant_result = cursor.fetchall()
            participant_list = []
            for p in participant_result:
                participant = {
                    "participantName": p[0],
                    "count": p[1]
                }
                participant_list.append(participant)

            query_document_activity = """SELECT activity.activityName, document_activity.countHour 
                                      FROM activity 
                                      JOIN document_activity 
                                      ON activity.activityID = document_activity.activityID
                                      WHERE document_activity.documentID = %s"""
            cursor.execute(query_document_activity, (documentID,))
            activity_result = cursor.fetchall()
            activity_list = []
            for a in activity_result:
                activity = {
                    "activityName": a[0],
                    "countHour": a[1]
                }
                activity_list.append(activity)

            query_problem = """SELECT problemDetail, solution FROM problem WHERE documentID = %s"""
            cursor.execute(query_problem, (documentID,))
            problem_result = cursor.fetchall()
            problem_list = []
            for p in problem_result:
                problem = {
                    "problemDetail": p[0],
                    "solution": p[1]
                }
                problem_list.append(problem)

            query_document_studentQF = """SELECT studentQF.name, document_studentQF.percentage
                                       FROM studentQF JOIN document_studentQF
                                       ON studentQF.student_QF_ID = document_studentQF.student_QF_ID 
                                       WHERE document_studentQF.documentID = %s"""
            cursor.execute(query_document_studentQF, (documentID,))
            studentQF_result = cursor.fetchall()
            studentQF_list = []
            for s in studentQF_result:
                studentQF = {
                    "name": s[0],
                    "percentage": s[1]
                }
                studentQF_list.append(studentQF)

            query_document_entrepreneurial = """SELECT entrepreneurial.entrepreneurialName FROM entrepreneurial
                                             JOIN document_entrepreneurial 
                                             ON entrepreneurial.entrepreneurialID = document_entrepreneurial.entrepreneurialID
                                             WHERE document_entrepreneurial.documentID = %s"""
            cursor.execute(query_document_entrepreneurial, (documentID,))
            entrepreneurial_result = cursor.fetchall()

            query_document_evaluation = """SELECT evaluation.evaluationName, document_evaluation.otherEvaluationName
                                        FROM evaluation JOIN document_evaluation 
                                        ON evaluation.evaluationID = document_evaluation.evaluationID
                                        WHERE document_evaluation.documentID = %s"""
            cursor.execute(query_document_evaluation, (documentID,))
            evaluation_result = cursor.fetchall()
            evaluation_list = []
            for e in evaluation_result:
                evaluation = {
                    "evaluation": e[0],
                    "otherEvaluation": e[1]
                }
                evaluation_list.append(evaluation)

            query_result = """SELECT kpi, detail, target FROM result WHERE documentID = %s"""
            cursor.execute(query_result, (documentID,))
            result_result = cursor.fetchall()
            result_list = []
            for r in result_result:
                result = {
                    "kpi": r[0],
                    "detail": r[1],
                    "target": r[2]
                }
                result_list.append(result)

            query_sustainability = """SELECT sustainability.sustainabilityName, goal.goalName 
                                   FROM document_sustainability 
                                   JOIN sustainability ON sustainability.sustainabilityID = document_sustainability.sustainabilityID
                                   LEFT JOIN goal ON document_sustainability.goalID = goal.goalID
                                   WHERE document_sustainability.documentID = %s"""
            cursor.execute(query_sustainability, (documentID,))
            sustainability_result = cursor.fetchall()
            sustainability_list = []
            for s in sustainability_result:
                sustainability = {
                    "sustainability": s[0],
                    "goal": s[1]
                }
                sustainability_list.append(sustainability)

            query_committee = """SELECT concat(student.firstName, " ", student.lastName), 
                              student_committee.position, student.studentID, student.tel, student.year
                              FROM student JOIN student_committee
                              ON student.studentID = student_committee.studentID
                              WHERE student_committee.documentID = %s"""
            cursor.execute(query_committee, (documentID,))
            committee_result = cursor.fetchall()
            committee_list = []
            for c in committee_result:
                committee = {
                    "name": c[0],
                    "position": c[1],
                    "studentID": c[2],
                    "tel": c[3],
                    "year": c[4]
                }
                committee_list.append(committee)

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
                                  FROM activityDocument 
                                  WHERE documentID = %s AND studentID = %s"""
                cursor.execute(query_authority, (documentID, id))
                authority_result = cursor.fetchone()
            else:
                query_authority = """SELECT progressID 
                                  FROM activityProgress 
                                  WHERE documentID = %s AND staffID = %s"""
                cursor.execute(query_authority, (documentID, id))
                authority_result = cursor.fetchone()

            if not authority_result:
                raise HTTPException(status_code=403, detail="You do not have permission to access this document")

            query_progress = """SELECT activityProgress.*, concat(staff.firstName, " ", staff.lastName), 
                             role.roleName
                             FROM activityProgress
                             JOIN role ON activityProgress.staff_roleID = role.roleID
                             JOIN staff ON activityProgress.staffID = staff.staffID
                             WHERE documentID = %s"""
            cursor.execute(query_progress, (documentID,))
            progress_result = cursor.fetchall()

            for p in progress_result:
                info = {
                    "progressID": p[0],
                    "staffID": p[2],
                    "staffName": p[11],
                    "staffRole": p[12],
                    "status": p[6],
                    "comment": p[7],
                    "step": p[1],
                }
                progress.append(info)

            document_info = {
                "DocumentID": detail_result[0],
                "type": detail_result[2],
                "startTime": detail_result[3],
                "endTime": detail_result[4],
                "code": detail_result[7],
                "departmentName": detail_result[8],
                "title": detail_result[9],
                "location": detail_result[10],
                "propose": detail_result[11],
                "payment": detail_result[12],
                "sustainabilityDetail": detail_result[14],
                "sustainabilityPropose": detail_result[15],
                "activityCharacteristic": detail_result[16],
                "codeOfHonor": detail_result[17],
                "prepareStart": detail_result[18],
                "prepareEnd": detail_result[19],
                "prepareFile": detail_result[20],
                "evaluationFile": detail_result[21],
                "budgetDetails": detail_result[22],
                "scheduleDetails": detail_result[23],
                "createDate": detail_result[5],
                "editDate": detail_result[6],
                "participant": participant_list,
                "activity": activity_list,
                "problem": problem_list,
                "studentQF": studentQF_list,
                "entrepreneurial": entrepreneurial_result,
                "evaluation": evaluation_list,
                "result": result_list,
                "sustainability": sustainability_list,
                "committee": committee_list,
                "allProgress": progress,
                "Owner": {
                    "studentID": doc_owner[0],
                    "username": doc_owner[1],
                    "name": f"{doc_owner[2]} {doc_owner[3]}",
                    "tel": doc_owner[4],
                    "email": doc_owner[5],
                    "year": doc_owner[6],
                    "facultyID": doc_owner[7],
                    "faculty": doc_owner[12],
                    "departmentID": doc_owner[8],
                    "department": doc_owner[13],
                    "currentGPA": doc_owner[9],
                    "cumulativeGPA": doc_owner[10],
                    "clubID": doc_owner[11],
                    "club": doc_owner[14]
                }
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

    async def approve_activity_document(detail: ActivityApproveDetail):
        conn = get_db_connection()
        cursor = conn.cursor()
        date = datetime.now()

        try:
            # Check if progressID and documentID exist
            check_query = """SELECT progressID, documentID 
                          FROM activityProgress 
                          WHERE progressID = %s AND documentID = %s"""
            cursor.execute(check_query, (detail.progressID, detail.documentID))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Invalid progressID or documentID")

            # Check if staffID matches progressID and documentID
            staff_check_query = """SELECT staffID 
                                FROM activityProgress 
                                WHERE progressID = %s AND documentID = %s AND staffID = %s"""
            cursor.execute(staff_check_query, (detail.progressID, detail.documentID, detail.staffID))
            staff_match = cursor.fetchone()

            if not staff_match:
                raise HTTPException(status_code=403, detail="Staff does not have the authority to approve this document")

            # Approve form
            update_approve_query = """UPDATE activityProgress
                                   SET status = %s, approvedAt = %s
                                   WHERE progressID = %s AND staffID = %s AND documentID = %s"""
            cursor.execute(update_approve_query, (
                detail.status,
                date,
                detail.progressID,
                detail.staffID,
                detail.documentID
            ))
            conn.commit()

            # Check if there are any remaining staff approvals
            next_staff_email_query = """SELECT staff.email
                                     FROM staff
                                     JOIN activityProgress ON staff.staffID = activityProgress.staffID
                                     WHERE activityProgress.documentID = %s
                                     AND activityProgress.status = 'Waiting for approve'
                                     ORDER BY activityProgress.step ASC
                                     LIMIT 1"""
            cursor.execute(next_staff_email_query, (detail.documentID,))
            next_staff_email = cursor.fetchone()

            if next_staff_email:
                # Send email to the next staff
                subject = "New Activity Document to sign."
                body = (f"You have activity document to sign\n"
                        f"Go to this website: https://capstone24.sit.kmutt.ac.th/un1")
                email_payload = {
                    "email": next_staff_email[0],
                    "subject": subject,
                    "body": body
                }
                await send_email(EmailSchema(**email_payload))
            else:
                # If no staff approvals are left, notify the student
                student_email_query = """SELECT student.email
                                      FROM student
                                      JOIN activityDocument ON student.studentID = activityDocument.studentID
                                      WHERE activityDocument.documentID = %s"""
                cursor.execute(student_email_query, (detail.documentID,))
                student_email = cursor.fetchone()

                if student_email:
                    subject = "Your Activity Document Has Been Approved."
                    body = (f"Your activity document has been approved successfully.\n"
                            f"Go to this website: https://capstone24.sit.kmutt.ac.th/un1")
                    email_payload = {
                        "email": student_email[0],
                        "subject": subject,
                        "body": body
                    }
                    await send_email(EmailSchema(**email_payload))

            return {"message": "Approve successfully"}

        except HTTPException as e:
            raise e

        except Exception as e:
            print(e)

        finally:
            cursor.close()
            conn.close()

    async def reject_activity_document(detail: ActivityRejectDetail):
        conn = get_db_connection()
        cursor = conn.cursor()
        date = datetime.now()

        try:
            # Check if progressID and documentID exist
            check_query = """SELECT progressID, documentID 
                          FROM activityProgress 
                          WHERE progressID = %s AND documentID = %s"""
            cursor.execute(check_query, (detail.progressID, detail.documentID))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Invalid progressID or documentID")
            # Check if staffID matches progressID and documentID
            staff_check_query = """SELECT staffID 
                                FROM activityProgress 
                                WHERE progressID = %s AND documentID = %s AND staffID = %s"""
            cursor.execute(staff_check_query, (detail.progressID, detail.documentID, detail.staffID))
            staff_match = cursor.fetchone()

            if not staff_match:
                raise HTTPException(status_code=403, detail="Staff does not have the authority to approve this document")

            update_query = """UPDATE activityProgress
                           SET status = %s, comment = %s, approvedAt = %s
                           WHERE progressID = %s AND staffID = %s AND documentID = %s"""
            cursor.execute(update_query, (
                detail.status,
                detail.comment,
                date,
                detail.progressID,
                detail.staffID,
                detail.documentID
            ))
            conn.commit()

            # send email to student
            student_email_query = """SELECT student.email 
                                  FROM student 
                                  JOIN activityDocument ON student.studentID = activityDocument.studentID
                                  WHERE activityDocument.documentID = %s"""
            cursor.execute(student_email_query, (detail.documentID,))
            student_email = cursor.fetchone()
            if student_email:
                subject = "Your Activity Document Has Been Rejected."
                body = (f"Your activity document has been rejected.\n"
                        f"Go to this website: https://capstone24.sit.kmutt.ac.th/un1")
                email_payload = {
                    "email": student_email[0],
                    "subject": subject,
                    "body": body
                }
                await send_email(EmailSchema(**email_payload))

            return {"message": "Reject successfully"}

        except HTTPException as e:
            raise e

        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()
