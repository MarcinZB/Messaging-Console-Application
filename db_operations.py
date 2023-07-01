import crypto


class User:
    def __init__(self, username, password="", salt=""):
        self._id = -1
        self.username = username
        self._hashed_password = crypto.hash_password(password, salt)


    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def new_password(self, password, salt=""):
        self._hashed_password = crypto.hash_password(password, salt)

    def save_to_db(self, cursor):
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


