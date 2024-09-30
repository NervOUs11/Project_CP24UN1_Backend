from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from argon2 import PasswordHasher
import mysql.connector
from mysql.connector import Error

app = FastAPI()
ph = PasswordHasher()

# MySQL Database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Ounitit2910",
            database="test_file_storage"
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")


# Pydantic models
class UserRegister(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


@app.post("/signup")
# Sign up endpoint
async def sign_up(user: UserRegister):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Hash the password using Argon2
        hashed_password = ph.hash(user.password)

        # Insert user into the database
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
# Log in endpoint
async def log_in(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Retrieve user from the database
        select_query = "SELECT password FROM users WHERE username = %s"
        cursor.execute(select_query, (user.username,))
        result = cursor.fetchone()

        if result is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Check the password
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
