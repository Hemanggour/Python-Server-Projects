import mysql.connector as sql

class Database:

    def __connectDB(self):
        self.mydb = sql.connect(host="localhost", user="root", password="812004Hemang", database="todolistdb", charset="utf8mb4")
        self.cur = self.mydb.cursor()

    def __init__(self):
        self.__connectDB()
        self.dataBase = "todolistdb"
        self.table_users = "users"
        self.table_tasks = "tasks"
        self.table_tokens = "password_resets"
        self.table_verifyEmail = 'verifyEmail'
    
    
    def createDB(self):
        query = f"CREATE DATABASE IF NOT EXISTS {self.dataBase};"
        self.cur.execute(query)
        self.mydb.commit()

    def useDB(self):
        query = f"USE {self.dataBase};"
        self.cur.execute(query)

    def createTB(self):
        query = f"""CREATE TABLE IF NOT EXISTS {self.dataBase}.{self.table_users} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(50) NOT NULL);"""
        self.cur.execute(query)
        self.mydb.commit()

        query = f"""CREATE TABLE IF NOT EXISTS {self.dataBase}.{self.table_tasks} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task_description TEXT NOT NULL,
        status VARCHAR(20) DEFAULT 'Pending',
        user_id INT,
        FOREIGN KEY (user_id) REFERENCES {self.dataBase}.{self.table_users}(id) ON DELETE CASCADE);"""
        self.cur.execute(query)
        self.mydb.commit()

        query = f"""CREATE TABLE IF NOT EXISTS {self.dataBase}.{self.table_tokens} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        token VARCHAR(255) NOT NULL,
        expires_at DATETIME NOT NULL,
        FOREIGN KEY (user_id) REFERENCES {self.dataBase}.{self.table_users}(id) ON DELETE CASCADE);"""
        self.cur.execute(query)
        self.mydb.commit()
        
        query = f"""CREATE TABLE IF NOT EXISTS verifyEmail (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(50) NOT NULL,
        token VARCHAR(255) NOT NULL,
        expires_at DATETIME NOT NULL);"""
        self.cur.execute(query)
        self.mydb.commit()

    # Show Databases
    def showDB(self):
        query = "SHOW DATABASES;"
        self.cur.execute(query)
        return self.cur.fetchall()

    # Show Tables
    def showTB(self):
        query = "SHOW TABLES;"
        self.cur.execute(query)
        return self.cur.fetchall()

    def deleteTB(self):
        query = f"""DROP TABLE IF EXISTS {self.table_tokens}"""
        self.cur.execute(query)
        self.mydb.commit()
        query = f"""DROP TABLE IF EXISTS {self.table_tasks}"""
        self.cur.execute(query)
        self.mydb.commit()
        query = f"""DROP TABLE IF EXISTS {self.table_users}"""
        self.cur.execute(query)
        self.mydb.commit()
        query = f"""DROP TABLE IF EXISTS {self.table_verifyEmail}"""
        self.cur.execute(query)
        self.mydb.commit()

    # Add User
    def addUser(self, username, email, password):
        query = f"INSERT INTO {self.dataBase}.{self.table_users} (username, email, password) VALUES (%s, %s, %s);"
        self.cur.execute(query, (username, email, password))
        self.mydb.commit()

    # Add Task for the current user
    def addTask(self, userId, task_description, status="Pending"):
        if userId:
            query = f"INSERT INTO {self.dataBase}.{self.table_tasks} (task_description, status, user_id) VALUES (%s, %s, %s);"
            self.cur.execute(query, (task_description, status, userId))
            self.mydb.commit()
        else:
            print("User not added. Cannot add task.")

    # Retrieve all tasks for a specific user
    def getTasks(self, userId):
        query = f"SELECT task_description FROM {self.dataBase}.{self.table_tasks} WHERE user_id = %s;"
        self.cur.execute(query, (userId,))
        return self.cur.fetchall()
    
    def getTasksIds(self, userId):
        query = f"SELECT id FROM {self.dataBase}.{self.table_tasks} WHERE user_id = %s;"
        self.cur.execute(query, (userId,))
        return self.cur.fetchall()

    # Update Task Status
    def updateTaskStatus(self, userId, taskDes, new_status):
        query = f"UPDATE {self.dataBase}.{self.table_tasks} SET status = %s WHERE  task_description = %s AND user_id = %s;"
        self.cur.execute(query, (new_status, taskDes, userId))
        self.mydb.commit()

    # Delete a Task
    def deleteTask(self, userId, taskId, task):
        query = f"DELETE FROM {self.dataBase}.{self.table_tasks} WHERE ((task_description = %s AND id = %s) AND user_id = %s);"
        self.cur.execute(query, (task, taskId, userId))
        self.mydb.commit()

    # Get User ID by Email
    def getUserByEmail(self, email):
        query = f"SELECT username FROM {self.dataBase}.{self.table_users} WHERE email = %s;"
        self.cur.execute(query, (email,))
        result = self.cur.fetchone()
        return result
    
    def getUserById(self, userId):
        query = f"SELECT username FROM {self.dataBase}.{self.table_users} WHERE id = %s;"
        self.cur.execute(query, (userId,))
        result = self.cur.fetchone()
        return result
    
    def getUserAndPass(self, username, password):
        query = f"SELECT username, password FROM {self.dataBase}.{self.table_users} WHERE username = %s AND password = %s;"
        self.cur.execute(query, (username, password))
        result = self.cur.fetchone()
        return result
    
    def getUserId(self, email):
        query = f"SELECT id FROM {self.dataBase}.{self.table_users} WHERE email = %s;"
        self.cur.execute(query, (email,))
        result = self.cur.fetchone()
        return result

    def getPass(self, email):
        query = f"SELECT password FROM {self.dataBase}.{self.table_users} WHERE email = %s;"
        self.cur.execute(query, (email,))
        result = self.cur.fetchone()
        return result

    def getEmail(self, email):
        query = f"SELECT email FROM {self.dataBase}.{self.table_users} WHERE email = %s;"
        self.cur.execute(query, (email,))
        result = self.cur.fetchone()
        return result
    
    def getEmailById(self, id):
        query = f"SELECT email FROM {self.dataBase}.{self.table_users} WHERE id = %s;"
        self.cur.execute(query, (id,))
        result = self.cur.fetchone()
        return result
    
    def updateEmail(self, username, password, newEmail):
        query = f"""
            UPDATE {self.dataBase}.{self.table_users}
            SET email = %s
            WHERE username = %s AND password = %s;"""
        self.cur.execute(query, (newEmail, username, password))
        self.mydb.commit()

    def updatePass(self, email, oldPassword, newPassword):
        query = f"""
            UPDATE {self.dataBase}.{self.table_users}
            SET password = %s
            WHERE email = %s AND password = %s;"""
        self.cur.execute(query, (newPassword, email, oldPassword))
        self.mydb.commit()
    
    def updateUsername(self, userId, newUsername):
        query = f"""
            UPDATE {self.dataBase}.{self.table_users}
            SET username = %s
            WHERE id = %s;"""
        self.cur.execute(query, (newUsername, userId))
        self.mydb.commit()
    
    def getData(self, username, email):
        query = f"""SELECT * FROM {self.dataBase}.{self.table_users} WHERE username = %s AND email = %s;"""
        self.cur.execute(query, (username, email))
        return self.cur.fetchall()

    def getUserTBData(self):
        query = f"""SELECT * FROM {self.dataBase}.{self.table_users};"""
        self.cur.execute(query)
        return self.cur.fetchall()
    
    def getTasksTBData(self):
        query = f"""SELECT * FROM {self.dataBase}.{self.table_tasks};"""
        self.cur.execute(query)
        return self.cur.fetchall()

    def getTokensTBData(self):
        query = f"""SELECT * FROM {self.dataBase}.{self.table_tokens};"""
        self.cur.execute(query)
        return self.cur.fetchall()
    
    def insertToken(self, userId, token, expires_at):
        query = f"INSERT INTO {self.dataBase}.{self.table_tokens} (user_id, token, expires_at) VALUES (%s, %s, %s);"
        self.cur.execute(query, (userId, token, expires_at))
        self.mydb.commit()

    def updatePassById(self, user_id, new_password):
        query = f"UPDATE {self.dataBase}.{self.table_users} SET password = %s WHERE id = %s;"
        self.cur.execute(query, (new_password, user_id))
        self.mydb.commit()

    def deleteResetTokenById(self, id):
        query = f"DELETE FROM {self.dataBase}.{self.table_tokens} WHERE user_id = %s;"
        self.cur.execute(query, (id,))
        self.mydb.commit()

    def getIdByToken(self, token):
        query = f"SELECT user_id, expires_at FROM {self.dataBase}.{self.table_tokens} WHERE token = %s;"
        self.cur.execute(query, (token,))
        result = self.cur.fetchone()
        return result

    def getTokenById(self, userId):
        query = f"SELECT token FROM {self.dataBase}.{self.table_tokens} WHERE user_id = %s;"
        self.cur.execute(query, (userId,))
        result = self.cur.fetchone()
        return result
    
    def deleteToken(self, token):
        query = f"DELETE FROM {self.dataBase}.{self.table_tokens} WHERE token = %s;"
        self.cur.execute(query, (token,))
        self.mydb.commit()

    def deleteTokenById(self, userId):
        query = f"DELETE FROM {self.dataBase}.{self.table_tokens} WHERE user_id = %s;"
        self.cur.execute(query, (userId,))
        self.mydb.commit()

    def addNotVerifiedUser(self, username, email, password, token, expire):
        query = f"INSERT INTO {self.dataBase}.{self.table_verifyEmail} (username, email, password, token, expires_at) VALUES (%s, %s, %s, %s, %s);"
        self.cur.execute(query, (username, email, password, token, expire))
        self.mydb.commit()

    def deleteNotVerifiedUser(self, email):
        query = f"DELETE FROM {self.dataBase}.{self.table_verifyEmail} WHERE email = %s;"
        self.cur.execute(query, (email,))
        self.mydb.commit()
    
    def getNotVerifiedEmail(self, email):
        query = f"SELECT email FROM {self.dataBase}.{self.table_verifyEmail} WHERE email = %s;"
        self.cur.execute(query, (email,))
        result = self.cur.fetchone()
        return result

    def getNotVerifiedUser(self, token):
        query = f"SELECT username, email, password, expires_at FROM {self.dataBase}.{self.table_verifyEmail} WHERE token = %s;"
        self.cur.execute(query, (token,))
        result = self.cur.fetchone()
        return result

    def getverifyEmailTBData(self):
        query = f"""SELECT * FROM {self.dataBase}.{self.table_verifyEmail};"""
        self.cur.execute(query)
        return self.cur.fetchall()
    
    def deleteExpiredTokens(self):
        query = f"DELETE FROM {self.dataBase}.{self.table_tokens} WHERE expires_at < NOW();"
        try:
            self.cur.execute(query)
            self.mydb.commit()
            print("Expired tokens deleted successfully.")
        except Exception as e:
            print(f"Error deleting expired tokens: {e}")
            self.mydb.rollback()

    def scheduleDeletion(self):
        query = "SET GLOBAL event_scheduler = ON;"
        self.cur.execute(query)
        self.mydb.commit()

        query = f"""CREATE EVENT IF NOT EXISTS delete_expired_tokens
        ON SCHEDULE EVERY 1 HOUR
        DO
            DELETE FROM {self.dataBase}.{self.table_tokens} WHERE expires_at < NOW();"""
        self.cur.execute(query)
        self.mydb.commit()

    def getPassById(self, userId):
        query = f"SELECT password FROM {self.dataBase}.{self.table_users} WHERE id = %s;"
        self.cur.execute(query, (userId,))
        result = self.cur.fetchone()
        return result

if __name__ == "__main__":
    # db = Database()
    # db.useDB()

    # print(db.showDB())
    # print(db.showTB())

    # print(db.getUserTBData())
    # print(db.getTasksTBData())
    # print(db.getTokensTBData())
    # print(db.getverifyEmailTBData())

    # db.deleteTB()
    # db.createTB()
    pass