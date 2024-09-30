import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("DB_HOSTNAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_DATABASE")


def convert_to_binary(filename):
    with open(filename, 'rb') as file:
        binary_data = file.read()
    return binary_data


def store_file(image_path, pdf_path):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()
        image_data = convert_to_binary(image_path)
        pdf_data = convert_to_binary(pdf_path)
        sql_insert_query = """INSERT INTO file_data (image, pdf) VALUES (%s, %s)"""
        cursor.execute(sql_insert_query, (image_data, pdf_data))
        connection.commit()
        print(f"Files successfully inserted with id: {cursor.lastrowid}")

    except mysql.connector.Error as error:
        print(f"Failed to insert data: {error}")


image_file_path = 'test_data/homemade-ice-cream.jpg'
pdf_file_path = 'test_data/PDF_test_file.pdf'
store_file(image_file_path, pdf_file_path)