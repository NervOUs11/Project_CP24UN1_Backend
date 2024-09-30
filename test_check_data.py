import mysql.connector
import os


def write_to_file(binary_data, filename):
    with open(filename, 'wb') as file:
        file.write(binary_data)
    print(f"{filename} has been created.")


# Connect to the MySQL database and retrieve the file data
def retrieve_file(file_id, output_image_path, output_pdf_path):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Ounitit2910',
            database='test_file_storage'
        )

        cursor = connection.cursor()

        # SQL query to fetch the file based on the ID
        sql_select_query = """SELECT image, pdf FROM file_data WHERE id = %s"""

        # Execute the query
        cursor.execute(sql_select_query, (file_id,))
        record = cursor.fetchone()

        if record:
            # Write the image and PDF to respective files
            image_data = record[0]
            pdf_data = record[1]

            write_to_file(image_data, output_image_path)
            write_to_file(pdf_data, output_pdf_path)

        else:
            print(f"No data found for id {file_id}")

    except mysql.connector.Error as error:
        print(f"Failed to retrieve data: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# Example usage to retrieve and store files
file_id = 1
image_output_path = 'output_image.jpg'
pdf_output_path = 'output_file.pdf'

retrieve_file(file_id, image_output_path, pdf_output_path)

if os.path.exists(image_output_path):
    os.system(f"open {image_output_path}")

if os.path.exists(pdf_output_path):
    os.system(f"open {pdf_output_path}")
