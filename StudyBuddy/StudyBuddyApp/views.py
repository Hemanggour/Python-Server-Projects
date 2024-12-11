from django.shortcuts import render, redirect, HttpResponse
from .authentication import Authenticate, Update, Token
from .database import dataBase as db
from re import search
from .sendEmail import SendEMail
from . import emailContent
from . import AI
from . import getQuiz
import random
import html

quizzes = []
notes = []
quizzesId = 0
a = Authenticate()
update = Update()
t = Token()

        #### Home Section ####

def home(request):
    loggedIn = request.session.get('loggedIn', False)
    user_id = request.session.get('userId', None)
    if ('loggedIn' in request.session and request.session['loggedIn']):
            if user_id:
                user = db.Database().getUserById(userId=user_id)
                return render(request, 'home.html', {'loggedIn': loggedIn, 'userId': user_id, 'username': user.username, 'goal': user.goal})
    return redirect('/login')


def learning(request):
    dataBase = db.Database()
    loggedIn = request.session.get('loggedIn', False)
    user_id = request.session.get('userId', None)
    if ('loggedIn' in request.session and request.session['loggedIn']):
        if request.method == 'POST':
            if loggedIn:
                noteDescription = request.POST.get('noteDescription')
                note = request.POST.get('note')
                userId = request.POST.get('userId')
                if note and noteDescription:
                    if (note.count(" ") == len(note)) and (noteDescription.count(" ") == len(noteDescription)):
                        return redirect('/learning')
                    else:
                        try:
                            if request.session['userId'] == int(userId):
                                notes.append(f"{note}")
                                dataBase.addNote((request.session['userId']), notedescription=noteDescription, notes=note)
                        except:
                            return redirect('/login')
                return redirect('/learning')
            return redirect('/login')
        elif loggedIn and user_id:
            try:
                notes.clear()
                if notesObj := dataBase.getNotes(userId=user_id):
                    user = dataBase.getUserById(userId=user_id)
                    params = {
                        'notes': notesObj,
                        'username': user.username,
                        'goal': user.goal,
                        'userId': request.session['userId'],
                        'loggedIn': loggedIn
                    }
                    return render(request, 'learning.html', params)
                user = dataBase.getUserById(userId=user_id)
                params = {
                    'loggedIn': loggedIn,
                    'userId': user_id,
                    'username': user.username,
                    'goal': user.goal
                }
                return render(request, 'learning.html', params)
            except Exception as e:
                print(f"Error in index: {e}")
                return redirect('/login')
        else:
            return render(request, 'learning.html', {'loggedIn': loggedIn})
    return redirect('/login')


def AIChat(request):
    loggedIn = request.session.get('loggedIn', False)
    user_id = request.session.get('userId', None)
    if ('loggedIn' in request.session and request.session['loggedIn']):
        if request.method == 'POST':
            dataBase = db.Database()
            if loggedIn:
                userMessage = request.POST.get('userMessage')
                try:
                    notes.clear()
                    user = dataBase.getUserById(userId=user_id)
                    params = {
                        'loggedIn': loggedIn,
                        'userId': request.session['userId'],
                        'username': user.username,
                        'goal': user.goal
                    }
                    if notesObj := dataBase.getNotes(userId=user_id):
                        user = dataBase.getUserById(userId=user_id)
                        params.update({'notes': notesObj})
                    if userMessage and (userMessage.count(' ') != len(userMessage)):
                        content = {
                            'parts': [
                                {'text': 'User Name: ' + user.username},
                                {'text': 'User goal: ' + user.goal},
                                {'text': 'User message: ' + userMessage},
                            ]
                        }
                        response = AI.GenerateContent(content)
                        params.update({'User': userMessage})
                        params.update({'Model': response})
                    return render(request, 'learning.html', params)
                except Exception as e:
                    print(f"Error in AIChat: {e}")
                    return redirect('/login')
    return redirect('/')


def settings(request):
    loggedIn = request.session.get('loggedIn', False)
    user_id = request.session.get('userId', None)
    if ('loggedIn' in request.session and loggedIn) and user_id:
        if request.method == 'GET':
            dataBase = db.Database()
            user = dataBase.getUserById(userId=user_id)
            params = {'username': user.username,
                      'email': user.email,
                      'goal': user.goal,
                      'userId': user_id,
                    }
            return render(request, 'settings.html', params)
    return redirect('/')


def setGoal(request):
    if 'loggedIn' in request.session and request.session['loggedIn']:
        if request.method == 'POST':
            goal = request.POST.get('goal')
            userId = request.POST.get('userId')
            if request.session['userId'] == int(userId):
                update.setGoal(request.session['userId'], goal)
        else:
            return render(request, 'set-goal.html', {'userId': request.session['userId']})
    return redirect('/')


def deleteNote(request):
    if request.method == 'POST':
        dataBase = db.Database()
        try:
            if request.session['loggedIn'] == True:
                userId = request.session['userId']
                noteId = int(request.POST.get('noteId'))
                notesIds = dataBase.getNotesIds(userId=userId)
                if notesIds:
                    if noteId in notesIds:
                        dataBase.deleteNote(noteId=noteId)
            return redirect('/learning')
        except Exception as e:
            print(f"Error in deleteNote: {e}")
            return redirect('/login')
    return HttpResponse(status=400)


def submitQuiz(request):
    loggedIn = request.session.get('loggedIn', False)
    user_id = request.session.get('userId', None)
    if ('loggedIn' in request.session and loggedIn) and user_id:
        if request.method == "POST":
            quizzes = request.session.get('quizzes', None)
            if not quizzes:
                return HttpResponse('No active quizzes found!')

            # Process submitted answers
            user_answers = []
            questions = [quiz.get('question') for quiz in quizzes]

            for que, ans in request.POST.items():
                if que in questions:
                    user_answers.append(ans)

            if len(user_answers) != len(questions):
                return redirect('/quiz')

            # Validate answers
            results = []
            correct_count = 0
            for index, quiz in enumerate(quizzes):
                user_answer = user_answers[index]
                correct = user_answer == quiz["correct_answer"]
                results.append({
                    "question": quiz["question"],
                    "user_answer": user_answer,
                    "correct_answer": quiz["correct_answer"],
                    "correct": correct
                })
                if correct:
                    correct_count += 1

            # Calculate accuracy
            total_questions = len(questions)
            accuracy = round((correct_count / total_questions) * 100, 2)

            # Clear quizzes from session
            del request.session['quizzes']

            # Render results
            return render(request, 'quiz.html', {
                "results": results,
                "accuracy": accuracy,
                'userId': user_id,
            })
        else:
            return redirect('/quiz')
    return redirect('/login')


def quiz(request):
    loggedIn = request.session.get('loggedIn', False)
    user_id = request.session.get('userId', None)
    if ('loggedIn' in request.session and loggedIn) and user_id:
        if request.method == 'POST':
            topic = int(request.POST.get('topic'))
            difficulty = int(request.POST.get('difficulty'))
            amount = int(request.POST.get('amount'))
            
            # Fetch quizzes
            res = getQuiz.getQuiz(topic=topic, amount=amount, difficulty=difficulty)
            if not res:
                return HttpResponse('Quizzes Not Found!! Please the refresh page')

            localQuizzes = res.get('results')

            # Process quizzes
            for quiz in localQuizzes:
                quiz["question"] = html.unescape(quiz["question"])
                quiz["correct_answer"] = html.unescape(quiz["correct_answer"])
                quiz["incorrect_answers"] = [html.unescape(answer) for answer in quiz["incorrect_answers"]]

                # Randomize options
                options = quiz["incorrect_answers"] + [quiz["correct_answer"]]
                random.shuffle(options)
                quiz["answers"] = options

            # Save quizzes in the session
            request.session['quizzes'] = localQuizzes

            return render(request, 'quiz.html', {"quizzes": localQuizzes, 'userId': user_id})
        else:
            return render(request, 'quiz.html', {'userId': user_id})
    return redirect('/login')

        #### Authentication Section ####

def login(request):
    dataBase = db.Database()
    if 'loggedIn' in request.session and request.session['loggedIn']:
        return render(request, 'logout.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        data = a.authLogin(email=email, password=password)
        if data:
            if data == 'Incorrect Password!!':
                return render(request, 'login.html', {'var': data})
            elif data == 'User Not Found!':
                return render(request, 'sign-up.html', {'var': data})
        else:
            # request.session.permanent = True
            request.session['loggedIn'] = True
            request.session['userId'] = dataBase.getUserByEmail(email=email).id
            return redirect('/')
    else:
        return render(request, 'login.html')


def signUp(request):
    if 'loggedIn' in request.session and request.session['loggedIn']:
        return render(request, 'logout.html')
    token = request.GET.get('token')
    if (request.method == 'POST') and (not token):
        dataBase = db.Database()
        mail = SendEMail()
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conPassword = request.POST.get('confirmPassword')
        if conPassword != password:
            return render(request, 'sign-up.html', {'var': "Password Doesn't Match!!"})
        validPass = a.authPass(password)
        if validPass != True:
            return render(request, 'sign-up.html', {'var': validPass})
        if a.authSignUp(username=username, email=email, password=password):
            return render(request, 'sign-up.html', {'var': "User Already Exists!"})
        if t.checkUserInNotVerified(email=email):
            dataBase.deleteVerifyEmail(email=email)
        token = t.generateSignUpToken(username=username, email=email, password=password)
        subject = emailContent.subject['emailSignUpVerification']
        body = (emailContent.body['emailSignUpVerification'].format(username, token))
        if mail.send(recEmail=email, subject=subject, body=body):
            return render(request, 'sign-up.html', {'var': "Verification Mail has Been Sent!"})
        return render(request, 'sign-up.html', {'var': "Error Sending Email, Try Again!"})
    elif token:
        dataBase = db.Database()
        if data := t.isSignUpTokenValid(token=token):
            a.signUp(data[0], data[1], data[2])
            dataBase.deleteVerifyEmail(email=data[1])
            return render(request, 'login.html', {'var': "Sign Up Successfull!"})
        return render(request, 'sign-up.html', {'var': "Invalid or expired token."})
            # return render(request, 'verify-sign-up.html', token=token)
    return render(request, 'sign-up.html')


def logout(request):
    try:
        request.session.clear()
        # request.session.permanent = False
        return redirect('/')
    except:
        return redirect('/login')

        #### Forgot Section ####

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        oldPassword = request.POST.get('oldPassword')
        newPassword = request.POST.get('newPassword')
        conNewPassword = request.POST.get('confirmNewPassword')
        notVerified = a.authLogin(email=email, password=oldPassword)
        if notVerified:
            if notVerified == 'Incorrect Password!!':
                return render(request, 'forgot-password.html', {'var': notVerified})
            elif notVerified == 'User Not Found!':
                return render(request, 'sign-up.html', {'var': notVerified})
        else:
            if conNewPassword != newPassword:
                return render(request, 'forgot-password.html', {'var': "Password Doesn't Match!!"})
            if newPassword == oldPassword:
                return render(request, 'forgot-password.html', {'var': "Current Password Can't Be Your New Password!"})
            validPass = a.authPass(newPassword)
            if validPass != True:
                return render(request, 'forgot-password.html', {'var': validPass})
            else:
                update.password(email=email, oldPassword=oldPassword, newPassword=newPassword)
                return render(request, 'login.html', {'var': "Password Reset Successfull!"})
    return render(request, 'forgot-password.html')


def forgotEmail(request):
    token = request.GET.get('token')
    if (request.method == 'POST') and (not token):
        dataBase = db.Database()
        mail = SendEMail()
        username = request.POST.get('username')
        password = request.POST.get('password')
        newEmail = request.POST.get('newEmail')
        notVerified = a.authLogin(email=newEmail, password=password)
        if notVerified:
            if notVerified == 'Incorrect Password!!':
                return render(request, 'forgot-email.html', {'var': "Email Already Exists!"})
            elif notVerified == 'User Not Found!':
                if a.authUser(username=username, password=password) == "Invalid Username or Password!":
                    return render(request, 'forgot-email.html', {'var': "Invalid Username or Password!"})
                else:
                    if t.checkUserInNotVerified(email=newEmail):
                        dataBase.deleteVerifyEmail(email=newEmail)
                    token = t.generateSignUpToken(username=username, email=newEmail, password=password)
                    subject = emailContent.subject["newEmailVerification"]
                    body = (emailContent.body["newEmailVerification"].format(username, token))
                    if mail.send(newEmail, subject=subject, body=body):
                        return render(request, 'forgot-email.html', {'var': "Verification Mail has Been Sent To New Email!"})
                    return render(request, 'forgot-email.html', {'var': "Error Sending Email, Try Again!"})
        else:
            return render(request, "forgot-email.html", {'var': 'Email Already Exists!'})
        return render(request, 'forgot-email.html')
    elif token:
        if data := t.isSignUpTokenValid(token=token):
            dataBase = db.Database()
            if data:
                update.email(username=data[0], newEmail=data[1], password=data[2])
                dataBase.deleteVerifyEmail(data[1])
                return render(request, 'login.html', {'var': 'Email Reset Successfull'})
        return render(request, "forgot-email.html", {'var': "Invalid or Expired Token!"})
    return render(request, 'forgot-email.html')


def forgotPasswordByEmail(request):
    token = request.GET.get('token')
    if (request.method == 'POST') and (not token):
        mail = SendEMail()
        dataBase = db.Database()
        email = request.POST.get('email')
        dbData = dataBase.getUserByEmail(email=email)
        dbEmail = dbData.email
        username = dbData.username
        message = "User Not Found!"
        if dbEmail:
            if dbEmail == email:
                dbuserId = dataBase.getUserByEmail(email=email).id
                if t.checkTokenExists(dbuserId):
                    dataBase.deleteTokenById(dbuserId)
                token = t.generateResetToken(dbuserId)
                subject = emailContent.subject['resetPassword']
                body = (emailContent.body['resetPassword'].format(username, token))
                if mail.send(recEmail=email, subject=subject, body=body):
                    return render(request, 'forgot-password-byEmail.html', {'var': "Verification Mail has Been Sent!"})
                message = "Error Sending Email, Try Again!"
        return render(request, 'forgot-password-byEmail.html', {'var': message})
    elif token:
        userId = t.isTokenValid(token=token)
        if userId:
            return render(request, 'reset-password.html', {'token': token, 'userId': userId})
        return render(request, 'forgot-password-byEmail.html', {'var': "Invalid or expired token!"})
    return render(request, 'forgot-password-byEmail.html')


def resetPassword(request):
    if request.method == 'POST':
        dataBase = db.Database()
        userId = request.POST.get('userId')
        token = request.POST.get('token')
        newPassword = request.POST.get('newPassword')
        confirmPassword = request.POST.get('confirmNewPassword')
        if newPassword != confirmPassword:
            return render(request, 'reset-password.html', {'var': "Passwords do not match", 'userId': userId, 'token': token})
        if dbPass := dataBase.getUserById(userId=userId).password:
            if newPassword == dbPass[0]:
                return render(request, 'reset-password.html', {'var': "Current Password Can't be your New Password!", 'userId': userId, 'token': token})
        if tUserId := t.isTokenValid(token=token):
            if int(tUserId) == int(userId):
                validPass = a.authPass(newPassword)
                if validPass != True:
                    return render(request, 'reset-password.html', {'var': validPass, 'userId': userId, 'token': token})
                # hashedPassword = a.hashPassword(newPassword)
                update.passById(userId=userId, newPassword=newPassword)
                update.deleteTokenById(userId=userId)
            return render(request, 'login.html', {'var': "Password has been successfully reset!"})
        else:
            return render(request, 'forgot-password-byEmail.html', {'var': "Invalid or expired token!"})
    return HttpResponse(status=400)


def updateUsername(request):
    loggedIn = request.session.get('loggedIn', False)
    user_id = request.session.get('userId', None)
    if ('loggedIn' in request.session and loggedIn) and user_id:
        if request.method == 'POST':
            newName = request.POST.get('newUsername')
            userId = request.POST.get('userId')
            if not ((search(r"[A-Z]", newName)) or (search(r"[a-z]", newName))):
                return redirect('/')
            if request.session['userId'] == int(userId):
                update.username(request.session['userId'], newName)
    return redirect('/')

        #### Verification Section ####

# def verifySignUp(request):
#     if request.method == 'POST':
#         dataBase = db.Database()
#         token = request.POST.get('token')
#         if data := t.isSignUpTokenValid(token=token):
#             a.signUp(data[0], data[1], data[2])
#             dataBase.deleteNotVerifiedUser(email=data[1])
#             return render(request, 'login.html', var="Sign Up Successfull!")
#         return render(request, 'sign-up.html', var="Invalid or expired token.")
#     return HttpResponse(status=400)