import argparse
import db_operations
from psycopg2.errors import UniqueViolation
from psycopg2 import connect, OperationalError
from crypto import check_password, hash_password

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help="username")
parser.add_argument('-p', '--password', help="user password")
parser.add_argument('-n', '--new_pass', help='new password')
parser.add_argument('-e', '--edit', help='edit user')

args = parser.parse_args()


def create_user(cursor, username, password):
    """Create a user with the given username and password.

        Args:
            cursor: The database cursor object.
            username (str): The username of the user to be created.
            password (str): The password for the user.

        Returns:
            None

        Raises:
            None

        Prints a success message if the user is created successfully. If the password
        is too short (less than 8 characters), it prints an error message. If a user
        with the same username already exists, it prints an error message.

        """
    if len(password) >= 8:
        try:
            user = db_operations.User(username, password)
            user.save_to_db(cursor)
            print(f"User Created: Nice to meet you {username}!")
        except UniqueViolation:
            print(f"User with username {username} already exists !")
    else:
        print("Password is too short, please use at least 8 characters")


def edit_password(cursor, username, password, new_pass):
    """Edit the password for a user with the given username.

        Args:
            cursor: The database cursor object.
            username (str): The username of the user.
            password (str): The current password.
            new_pass (str): The new password.

        Returns:
            None

        Raises:
            None

        Prints a success message if the password is changed successfully. If the new password
        is the same as the old password, it prints an error message. If the current password
        is incorrect, it prints an error message. If the user does not exist, it prints an
        error message. If the new password is too short (less than 8 characters), it prints
        an error message.

        """
    user = db_operations.User.load_user_by_username(cursor, username)
    user_hashed = user.hashed_password

    if user:
        if check_password(password, user_hashed):
            if new_pass == password:
                print("New password cannot be the same as old password")
            else:
                if len(new_pass) >= 8:
                    user_hashed = new_pass
                    user.save_to_db(cursor)
                    print("Password changed!")
                else:
                    print("New password is too short, please use at least 8 characters")

        else:
            print('Incorrect password !')
    else:
        print("User does not exist !")



connection = connect(user='postgres', password='coderslab', host='localhost', database='messanger_db')
connection.autocommit = True
cursor = connection.cursor()

