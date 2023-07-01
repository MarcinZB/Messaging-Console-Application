from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

CREATE_DATABASE = "CREATE DATABASE messanger_db"

CREATE_TABLE_USERS = """CREATE TABLE users 
                    (
                        user_id serial ,
                        username varchar(255),
                        hashed_password varchar(80)
                        PRIMARY KEY (id)
                    );"""

CREATE_TABLE_MESSAGES = """CREATE TABLE messages 
                    (
                        message_id serial ,
                        from_id int,
                        to_id int,
                        creation_date timestamp,
                        text varchar(255)
                        PRIMARY KEY (id),
                        FOREIGN KEY (from_id) REFERENCES users(user_id),
                        FOREIGN KEY (to_id) REFERENCES users(user_id)
                    );"""