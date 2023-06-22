import boto3
from botocore.exceptions import ClientError
from flask import Flask, jsonify, render_template
import json
import mysql.connector
import configparser

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    return response

@app.route('/')
def index():
    # Create a configparser object
    config = configparser.ConfigParser()

    # Read the properties file
    config.read('properties.db')

    # Access the values from the 'database' section
    user = config.get('database', 'user')
    password = config.get('database', 'password')
    host = config.get('database', 'host')
    database = config.get('database', 'database')

    # Establish the MySQL connection
    cnx = mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        database=database
    )

    cursor = cnx.cursor()

    # Create the table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS studentlist (name VARCHAR(50) NOT NULL, roll INT NOT NULL, grade CHAR(1) NOT NULL);
    """
    cursor.execute(create_table_query)

    #     # Delete all values from the table
    # delete_query = "DELETE FROM studentlist"
    # cursor = cnx.cursor()
    # cursor.execute(delete_query)
    # cnx.commit()

    # Insert values into the table
    insert_query = """
    INSERT INTO studentlist (name, roll, grade)
    VALUES (%s, %s, %s)
    """
    values = [('hari', 143, 'A'), ('reddy', 124, 'B'), ('seshu', 564, 'C')]  # Example values to insert
    cursor.executemany(insert_query, values)

    # Commit the changes
    cnx.commit()

    # Retrieve data from the "studentlist" table
    select_query = "SELECT * FROM studentlist"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    # Close the database connection
    cnx.close()

    return render_template('table.html', rows=rows)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)