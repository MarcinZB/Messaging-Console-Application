import os

from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable


username = "postgres"
passwd = "coderslab"
server = "localhost"



CREATE_DATABASE = "CREATE DATABASE messanger_db"

CREATE_TABLE_USERS = """CREATE TABLE users
                    (
                        user_id serial ,
                        username varchar(255),
                        hashed_password varchar(80),
                        PRIMARY KEY(user_id)
                    );"""

CREATE_TABLE_MESSAGES = """CREATE TABLE messages 
                    (
                        message_id serial ,
                        from_id int,
                        to_id int,
                        creation_date timestamp DEFAULT current_timestamp,
                        text varchar(255),
                        PRIMARY KEY(message_id),
                        FOREIGN KEY(from_id) REFERENCES users(user_id) ON DELETE CASCADE,
                        FOREIGN KEY(to_id) REFERENCES users(user_id) ON DELETE CASCADE 
                    );"""


try:
    connection = connect(user=username, password=passwd, host=server)
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(CREATE_DATABASE)
        print("NOTE: DATABASE CREATED")
    except DuplicateDatabase as dd:
        print("WARNING: DATABASE EXISTS", dd)
    connection.close()

except OperationalError as oe:
    print("WARNING: ERROR!", oe)

try:
    connection = connect(user=username, password=passwd, host=server, database='messanger_db')
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(CREATE_TABLE_USERS)
        print("NOTE: TABLE users CREATED")
    except DuplicateTable as dt:
        print("WARNING: TABLE EXISTS", dt)

    try:
        cursor.execute(CREATE_TABLE_MESSAGES)
        print("NOTE: TABLE messages CREATED")
    except DuplicateTable as dt:
        print("WARNING: TABLE EXISTS", dt)
    connection.close()
except OperationalError as oe:
    print("WARNING: ERROR", oe)
