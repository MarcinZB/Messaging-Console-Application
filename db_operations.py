import crypto
from psycopg2 import connect
import psycopg2.errors



class User:
    def __init__(self, username, password="", salt=""):
        """Initialize a User object.

            Args:
                username (str): The username of the user.
                password (str, optional): The password of the user. Defaults to an empty string.
                salt (str, optional): The salt value used for password hashing. Defaults to an empty string.

            Returns:
                None

            Raises:
                None
            """
        self._id = -1
        self.username = username
        self._hashed_password = crypto.hash_password(password, salt)


    @property
    def id(self):
        """Get the ID of the user.

            Returns:
                int: The ID of the user.
            """
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def new_password(self, password, salt=""):
        """Generate a new hashed password for the user.

            Args:
                password (str): The new password to be hashed.
                salt (str, optional): The salt value used for password hashing. Defaults to "".

            Returns:
                None

            Raises:
                None
            """
        self._hashed_password = crypto.hash_password(password, salt)

    def save_to_db(self, cursor):
        """Save the user object to the database.

            Args:
                cursor: The cursor object used to execute the SQL statements.

            Returns:
                bool: True if the operation is successful, False otherwise.

            Raises:
                psycopg2.Error: If there is an error executing the SQL statements.
            """
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password) 
                     VALUES (%s, %s) RETURNING user_id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = """UPDATE user SET username = %s, hashed_password=%s
                     WHERE id = %s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_username(cursor, username):
        """Load a user from the database by username.

            Args:
                cursor: The cursor object used to execute the SQL query.
                username (str): The username of the user to load.

            Returns:
                User or None: The loaded User object if the user is found, None otherwise.

            Raises:
                psycopg2.Error: If there is an error executing the SQL query.
            """
        sql = """SELECT user_id, username, hashed_password
                 FROM users
                 WHERE username=%s
                    """

        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            print("There is no user with this username")
            return data

    @staticmethod
    def load_user_by_id(cursor, user_id):

        sql = """SELECT user_id, username, hashed_password
                 FROM users
                 WHERE user_id=%s
               """

        cursor.execute(sql, (user_id,))
        data = cursor.fetchone()

        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            print("There is no user with this id number ")

    @staticmethod
    def load_all_users(cursor):
        """Fetch all users from the database.

            Args:
                cursor: The cursor object used to execute the SQL query.

            Returns:
                list: A list of User objects representing all the users in the database.

            Raises:
                psycopg2.Error: If there is an error executing the SQL query.
            """

        sql = """SELECT * FROM users"""
        users = []
        cursor.execute(sql)

        for user_data in cursor.fetchall():
            id_, username, hashed_password = user_data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete_user(self, cursor, id):
        """Delete the user from the database.

           Args:
               cursor: The cursor object used to execute the SQL query.

           Returns:
               bool: True if the deletion is successful, False otherwise.

           Raises:
               psycopg2.Error: If there is an error executing the SQL query.
           """
        sql = """DELETE FROM users WHERE user_id=%s;"""

        try:
            cursor.execute(sql, (id,))
            self._id = -1
            return True
        except psycopg2.Error as e:
            print("Error deleting user:", e)
            return False




