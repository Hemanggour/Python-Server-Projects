from ..models import User, Note, Token, VerifyEmail
from django.utils.timezone import now

class Database:

    def createUser(self, username, email, password):
        user = User.objects.create(username=username, email=email, password=password)
        return user

    def addNote(self, user_id, notedescription, notes):
        user = User.objects.get(id=user_id)
        note = Note.objects.create(user=user, notedescription=notedescription, notes=notes)
        return note

    def getNotes(self, userId):
        return Note.objects.filter(user_id=userId)

    def getNotesIds(self, userId):
        note_ids = Note.objects.filter(user_id=userId).values_list('id', flat=True)
        return list(note_ids)


    def deleteNote(self, noteId):
        Note.objects.filter(id=noteId).delete()

    def getUserByEmail(self, email):
        return User.objects.filter(email=email).first()

    def getUserById(self, userId):
        return User.objects.filter(id=userId).first()

    def getUserCredentials(self, username, password):
        return User.objects.filter(username=username, password=password).first()

    def updateUserEmail(self, username, password, newEmail):
        User.objects.filter(username=username, password=password).update(email=newEmail)

    def updateUserPassword(self, email, oldPassword, newPassword):
        User.objects.filter(email=email, password=oldPassword).update(password=newPassword)
    
    def updateUserPasswordById(self, userId, newPassword):
        User.objects.filter(id=userId).update(password=newPassword)
    
    def updateUsernameById(self, userId, newName):
        User.objects.filter(id=userId).update(username=newName)

    def createToken(self, userId, token, expiresAt):
        user = User.objects.get(id=userId)
        Token.objects.create(user=user, token=token, expires_at=expiresAt)

    def getTokenById(self, userId):
        return Token.objects.filter(user_id=userId).first()

    def deleteTokenById(self, userId):
        Token.objects.filter(user_id=userId).delete()

    def deleteExpiredTokens(self):
        Token.objects.filter(expires_at=now()).delete()

    def updateGoal(self, userId, goal):
        User.objects.filter(id=userId).update(goal=goal)

    def createVerifyEmail(self, username, email, password, token, expiresAt):
        VerifyEmail.objects.create(
            username=username,
            email=email,
            password=password,
            token=token,
            expires_at=expiresAt,
        )

    def getVerifyEmail(self, email):
        return VerifyEmail.objects.filter(email=email).first()

    def deleteVerifyEmail(self, email):
        VerifyEmail.objects.filter(email=email).delete()

    def getUserForVerification(self, token):
        return VerifyEmail.objects.filter(token=token).first()
    
    def getTokenByToken(self, token):
        return Token.objects.filter(token=token).first()

    def deleteAllTokens(self):
        Token.objects.all().delete()