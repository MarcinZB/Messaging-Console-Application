import argparse
import db_operations
from psycopg2 import connect, OperationalError
from crypto import check_password

parser = argparse.ArgumentParser()

parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--password', help='password')
parser.add_argument('-t', '--to', help='the name of the user to whom the message is to be sent')
parser.add_argument('-m', '--message', help='message')
parser.add_argument('-l', '--list', help='request to list all user messages (flag)', action='store_true')

args = parser.parse_args()


def list_user_messages(cursor, username, password):
    """
    This function retrieves and prints all messages for a given user from the database, provided the username and password are correct.

    Args:
    cursor: A database cursor object.
    username (str): The username of the user whose messages are to be retrieved.
    password (str): The password of the user.

    Returns:
    None

    Raises:
    None

    Example:
    cursor = db_operations.create_cursor()
    list_user_messages(cursor, 'example_user', 'password123')
    """
    user = db_operations.User.load_user_by_username(cursor, username)

    if user:
        if check_password(password, user.hashed_password):
            messages = db_operations.Message.load_all_messages(cursor)
            counter = 1

            for message in messages:
                to_ = db_operations.User.load_user_by_id(cursor, message.to_id)
                print(f"""Message no.{counter}: 
                Message to : {to_.username},
                Message: {message.text},
                Message date: {message._creation_date}""")
                counter += 1
        else:
            print("Incorrect password !")


def send_message(cursor, username, password, to, message):
    """
    This function sends a message from one user to another user in the database, provided the sender's username and password are correct.

    Args:
    cursor: A database cursor object.
    username (str): The username of the sender.
    password (str): The password of the sender.
    to (str): The username of the recipient.
    message (str): The message content to be sent.

    Returns:
    None

    Raises:
    None

    Example:
    cursor = db_operations.create_cursor()
    send_message(cursor, 'sender_user', 'password123', 'recipient_user', 'Hello, how are you?')
    """

    user = db_operations.User.load_user_by_username(cursor, username)
    user_hashed_passwd = user.hashed_password

    if user:

        if check_password(password, user_hashed_passwd):
            reciver = db_operations.User.load_user_by_username(cursor, to)
            if reciver:
                shipper_id = user.id
                reciver_id = reciver.id
                if len(message) <= 255:
                    final_message = db_operations.Message(shipper_id, reciver_id, message)
                    final_message.save_to_db(cursor)
                    print("Message sent !")
                else:
                    print("The message is too long, please try to hold in 255 characters.")
            else:
                print(f"There is no user named {to}")
        else:
            print("Incorrect password !")


if __name__ == '__main__':

    try:
        connection = connect(user='postgres', password='coderslab', host='localhost', database='messanger_db')
        connection.autocommit = True
        cursor = connection.cursor()

        if args.username and args.password and args.list:
            list_user_messages(cursor, args.username, args.password)
        elif args.username and args.password and args.to and args.message:
            send_message(cursor, args.username, args.password, args.to, args.message)
        else:
            parser.print_help()
        connection.close()

    except OperationalError as opr_err:
        print("Connection Error: ", opr_err)