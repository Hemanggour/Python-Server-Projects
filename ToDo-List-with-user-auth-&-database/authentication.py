from database.db import Database
import hashlib
import random
import datetime


class Authenticate:

    def signUp(self, username, email, password):
        dataBase = Database()
        dataBase.addUser(username=username, email=email, password=password)

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
        dbEmail = dataBase.getEmail(email=email)
        if dbEmail:
            if email == dbEmail[0]:
                dbPass = dataBase.getPass(email=email)
                if dbPass:
                    if password == dbPass[0]:
                        return False
                    return "Incorrect Password!!"
        return "User Not Found!"

    def authSignUp(self, username, email, password):
        dataBase = Database()
        dbEmail = dataBase.getEmail(email)
        if dbEmail:
            if dbEmail[0] == email:
                return "User Already Exists!"
        return False

    def authUser(self, username, password):
        dataBase = Database()
        data = dataBase.getUserAndPass(username, password)
        if data:
            if (data[0] == username) and (data[1] == password):
                return True
        return "Invalid Username or Password!"

class Update():

    def password(self, email, oldPassword, newPassword):
        dataBase = Database()
        dataBase.updatePass(email=email, oldPassword=oldPassword, newPassword=newPassword)

    def email(self, username, password, newEmail):
        dataBase = Database()
        dataBase.updateEmail(username=username, password=password, newEmail=newEmail)
    
    def username(self, userId, newName):
        dataBase = Database()
        dataBase.updateUsername(newUsername=newName, userId=userId)

    def passById(self, userId, newPassword):
        dataBase = Database()
        dataBase.updatePassById(user_id=userId, new_password=newPassword)

    def deleteTokenById(self, userId):
        dataBase = Database()
        dataBase.deleteResetTokenById(userId)

class Token():

    def generateResetToken(self, userId):
        dataBase = Database()

        token = hashlib.sha256(str(random.random()).encode('utf-8')).hexdigest()
        expires_at = datetime.datetime.now() + datetime.timedelta(hours=1)  # Token expires in 1 hour
        
        dataBase.insertToken(userId, token, expires_at=expires_at)
        return token
    
    def generateSignUpToken(self, username, email, password):
        dataBase = Database()

        token = hashlib.sha256(str(random.random()).encode('utf-8')).hexdigest()
        expires_at = datetime.datetime.now() + datetime.timedelta(hours=1)  # Token expires in 1 hour
        
        dataBase.addNotVerifiedUser(username=username, email=email, password=password, token=token, expire=expires_at)
        # dataBase.insertToken(userId, token, expires_at=expires_at)
        return token

    def isTokenValid(self, token):
        dataBase = Database()
        result = dataBase.getIdByToken(token=token)
        print(result)
        if result:
            user_id, expires_at = result
            if datetime.datetime.now() < expires_at:
                return user_id
            else:
                dataBase.deleteToken(token=token)
                return None
        return None
    
    def isSignUpTokenValid(self, token):
        dataBase = Database()
        result = dataBase.getNotVerifiedUser(token=token)
        if result:
            username, email, password, expires_at = result
            if datetime.datetime.now() < expires_at:
                return (username, email, password)
            else:
                dataBase.deleteNotVerifiedUser(email=email)
                return None
        return None
    
    def checkUserInNotVerified(self, email):
        dataBase = Database()
        if data := dataBase.getNotVerifiedEmail(email=email):
            if data[0] == email:
                return True
        return False

    def checkTokenExists(self, userId):
        dataBase = Database()
        if token := dataBase.getTokenById(userId=userId):
            return token
        return False

if __name__ == '__main__':
    # t = Token()
    # token = t.generateSignUpToken('hemang', 'hemang@gmail.com', '0801')
    # if data := t.isSignUpTokenValid(token=token):
    #     print(data[0], data[1], data[2])
    # dab = Database()
    # dab.deleteNotVerifiedUser('hemang@gmail.com')

    # print(t.checkUserInNotVerified('hggamer812004@gmail.com'))

    pass