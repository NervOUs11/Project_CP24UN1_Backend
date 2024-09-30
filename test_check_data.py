import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("DB_HOSTNAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_DATABASE")


def write_to_file(binary_data, filename):
    with open(filename, 'wb') as file:
        file.write(binary_data)
    print(f"{filename} has been created.")


def retrieve_file(file_id, output_image_path, output_pdf_path):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()
        sql_select_query = """SELECT image, pdf FROM file_data WHERE id = %s"""
        cursor.execute(sql_select_query, (file_id,))
        record = cursor.fetchone()

        if record:
            image_data = record[0]
            pdf_data = record[1]
            write_to_file(image_data, output_image_path)
            write_to_file(pdf_data, output_pdf_path)

        else:
            print(f"No data found for id {file_id}")

    except mysql.connector.Error as error:
        print(f"Failed to retrieve data: {error}")


id = 1
image_output_path = 'output_image.jpg'
pdf_output_path = 'output_file.pdf'
retrieve_file(id, image_output_path, pdf_output_path)

if os.path.exists(image_output_path):
    os.system(f"open {image_output_path}")

if os.path.exists(pdf_output_path):
    os.system(f"open {pdf_output_path}")