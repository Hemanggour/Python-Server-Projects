# from . database.db import Database
from .database import dataBase as db
import hashlib
import random
import datetime

Database = db.Database

class Authenticate:

    def signUp(self, username, email, password):
        dataBase = Database()
        dataBase.createUser(username=username, email=email, password=password)

    def authPass(self, password):
        import re
        if len(password) < 8:
            return "Password must be at least 8 characters long."
        if not re.search(r"[A-Z]", password):
            return "Password must contain at least one uppercase letter."
        if not re.search(r"[a-z]", password):
            return "Password must contain at least one lowercase letter."
        if not re.search(r"\d", password):
            return "Password must contain at least one digit."
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return "Password must contain at least one special character."
        if re.search(r"\s", password):
            return "Password should not contain any spaces."
        return True

    def authLogin(self, email, password):
        dataBase = Database()
        if data := dataBase.getUserByEmail(email=email):
            if dbEmail := data.email:
                if email == dbEmail:
                    dbPass = data.password
                    if dbPass:
                        if password == dbPass:
                            return False
                        return "Incorrect Password!!"
        return "User Not Found!"

    def authSignUp(self, username, email, password):
        dataBase = Database()
        dbEmail = dataBase.getUserByEmail(email)
        if dbEmail:
            if dbEmail.email == email:
                return "User Already Exists!"
        return False

    def authUser(self, username, password):
        dataBase = Database()
        data = dataBase.getUserCredentials(username, password)
        if data:
            if (data.username == username) and (data.password == password):
                return True
        return "Invalid Username or Password!"

class Update():

    def password(self, email, oldPassword, newPassword):
        dataBase = Database()
        dataBase.updateUserPassword(email=email, oldPassword=oldPassword, newPassword=newPassword)

    def email(self, username, password, newEmail):
        dataBase = Database()
        dataBase.updateUserEmail(username=username, password=password, newEmail=newEmail)
    
    def username(self, userId, newName):
        dataBase = Database()
        dataBase.updateUsernameById(userId=userId, newName=newName)

    def passById(self, userId, newPassword):
        dataBase = Database()
        dataBase.updateUserPasswordById(userId=userId, newPassword=newPassword)

    def setGoal(self, userId, goal):
        dataBase = Database()
        dataBase.updateGoal(userId, goal)

    def deleteTokenById(self, userId):
        dataBase = Database()
        dataBase.deleteTokenById(userId)

class Token():

    def generateResetToken(self, userId):
        dataBase = Database()

        token = hashlib.sha256(str(random.random()).encode('utf-8')).hexdigest()
        expires_at = datetime.datetime.now() + datetime.timedelta(hours=1)  # Token expires in 1 hour
        
        dataBase.createToken(userId, token=token, expiresAt=expires_at)
        return token
    
    def generateSignUpToken(self, username, email, password):
        dataBase = Database()

        token = hashlib.sha256(str(random.random()).encode('utf-8')).hexdigest()
        expires_at = datetime.datetime.now() + datetime.timedelta(hours=1)  # Token expires in 1 hour
        
        dataBase.createVerifyEmail(username=username, email=email, password=password, token=token, expiresAt=expires_at)
        # dataBase.insertToken(userId, token, expires_at=expires_at)
        return token

    def isTokenValid(self, token):
        dataBase = Database()
        result = dataBase.getTokenByToken(token=token)
        if result:
            user_id, expires_at = result.user_id, result.expires_at
            if datetime.datetime.now() < expires_at.replace(tzinfo=None):
                return user_id
            else:
                dataBase.deleteExpiredTokens()
                return None
        return None
    
    def isSignUpTokenValid(self, token):
        dataBase = Database()
        result = dataBase.getUserForVerification(token=token)
        if result:
            username, email, password, expires_at = result.username, result.email, result.password, result.expires_at
            if datetime.datetime.now() < expires_at.replace(tzinfo=None):
                return (username, email, password)
            else:
                dataBase.deleteExpiredTokens()
                return None
        return None
    
    def checkUserInNotVerified(self, email):
        dataBase = Database()
        if data := dataBase.getVerifyEmail(email=email):
            if data.email == email:
                return True
        return False

    def checkTokenExists(self, userId):
        dataBase = Database()
        if data := dataBase.getTokenById(userId=userId):
            return data.token
        return False