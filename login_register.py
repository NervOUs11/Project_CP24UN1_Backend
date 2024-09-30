import mysql.connector
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from argon2 import PasswordHasher

app = FastAPI()
ph = PasswordHasher()
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
            database=database
        )
        return connection

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")


class UserRegister(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


@app.post("/signup")
async def sign_up(user: UserRegister):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        hashed_password = ph.hash(user.password)
        insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(insert_query, (user.username, hashed_password))
        conn.commit()
        return {"message": "User registered successfully"}

    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="User registration failed")

    finally:
        cursor.close()
        conn.close()


@app.post("/login")
async def log_in(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        select_query = "SELECT password FROM users WHERE username = %s"
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
