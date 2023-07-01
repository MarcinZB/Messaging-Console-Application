import crypto


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
                     VALUES (%s, %s) RETURNING id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = """UPDATE user SET username = %s, hashed_password=%s
                     WHERE id = %s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql,values)
            return True


