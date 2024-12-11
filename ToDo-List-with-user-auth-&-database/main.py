from flask import Flask, render_template, request, redirect, session
from authentication import Authenticate, Update, Token
from database import db
from re import search
from sendEmail import SendEMail
import emailContent
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'ifYouAreBadThenIAmYourDad'
tasks = []

app.permanent_session_lifetime = timedelta(days=7)

a = Authenticate()
update = Update()
t = Token()
        #### Home Section ####

@app.route('/', methods=['GET', 'POST'])
def index():
    dataBase = db.Database()
    loggedIn = session.get('loggedIn', False)
    user_id = session.get('userId', None)
    if ('loggedIn' in session and session['loggedIn']) and (session.permanent):
        print(loggedIn, request.method)
        if request.method == 'POST':
            if loggedIn:
                task = request.form.get('task')
                userId = request.form.get('userId')
                if task:
                    if task.count(" ") == len(task):
                        return redirect('/')
                    else:
                        try:
                            if session['userId'] == int(userId):
                                dataBase.addTask((session['userId']), task_description=task)
                        except:
                            return redirect('/login')
                return redirect('/')
            return redirect('/login')
        elif loggedIn and user_id:
            try:
                tasks.clear()
                tasksIds = []
                if dataBase.getTasks(userId=user_id):
                    for task in dataBase.getTasks(userId=user_id):
                        tasks.append(task[0])
                    for taskId in dataBase.getTasksIds(userId=user_id):
                        tasksIds.append(taskId[0])
                username = dataBase.getUserById(userId=user_id)
                return render_template('home.html', length=len(tasks), tasks=tasks, tasksIds=tasksIds, username=username[0], userId = session['userId'] , loggedIn = loggedIn)
            except Exception as e:
                print(f"Error: {e}")
                return redirect('/login')
        else:
            return render_template('home.html', loggedIn=loggedIn)
    return redirect('/login')

@app.route('/delete-task', methods=['POST'])
def delete_task():
    dataBase = db.Database()
    try:
        if session['loggedIn'] == True:
            userId = session['userId']
            task_to_delete = request.form.get('task_to_delete')
            taskId = request.form.get('taskId_to_delete')
            print(task_to_delete)
            if task_to_delete in [task[0] for task in dataBase.getTasks(userId=userId)]:
                dataBase.deleteTask(userId=userId, taskId=taskId, task=task_to_delete)
        return redirect('/')
    except:
        return redirect('/login')

        #### Authentication Section ####

@app.route('/login', methods=['GET', 'POST'])
def login():
    dataBase = db.Database()
    if 'loggedIn' in session and session['loggedIn']:
        return render_template('logout.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        data = a.authLogin(email=email, password=password)
        if data:
            if data == 'Incorrect Password!!':
                return render_template('login.html', var=data)
            elif data == 'User Not Found!':
                return render_template('sign-up.html', var=data)
        else:
            session.permanent = True
            session['loggedIn'] = True
            session['userId'] = dataBase.getUserId(email=email)[0]
            return redirect('/')
    else:
        return render_template('login.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    if 'loggedIn' in session and session['loggedIn']:
        return render_template('logout.html')
    token = request.args.get('token')
    if (request.method == 'POST') and (not token):
        dataBase = db.Database()
        mail = SendEMail()
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        conPassword = request.form.get('confirmPassword')
        if conPassword != password:
            return render_template('sign-up.html', var="Password Doesn't Match!!")
        validPass = a.authPass(password)
        if validPass != True:
            return render_template('sign-up.html', var=validPass)
        if a.authSignUp(username=username, email=email, password=password):
            return render_template('sign-up.html', var="User Already Exists!")
        if t.checkUserInNotVerified(email=email):
            dataBase.deleteNotVerifiedUser(email=email)
        token = t.generateSignUpToken(username=username, email=email, password=password)
        subject = emailContent.subject['emailSignUpVerification']
        body = (emailContent.body['emailSignUpVerification'].format(username, token))
        print(subject, "\n",body)
        if mail.send(recEmail=email, subject=subject, body=body):
            return render_template('sign-up.html', var="Verification Mail has Been Sent!")
        return render_template('sign-up.html', var="Error Sending Email, Try Again!")
    elif token:
        dataBase = db.Database()
        if data := t.isSignUpTokenValid(token=token):
            a.signUp(data[0], data[1], data[2])
            dataBase.deleteNotVerifiedUser(email=data[1])
            return render_template('login.html', var="Sign Up Successfull!")
        return render_template('sign-up.html', var="Invalid or expired token.")
            # return render_template('verify-sign-up.html', token=token)
    return render_template('sign-up.html')

@app.route('/logout')
def logout():
    try:
        session.clear()
        session.permanent = False
        return redirect('/')
    except:
        return redirect('/login')

        #### Forgot Section ####

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgotPassword():
    if request.method == 'POST':
        email = request.form.get('email')
        oldPassword = request.form.get('oldPassword')
        newPassword = request.form.get('newPassword')
        conNewPassword = request.form.get('confirmNewPassword')
        notVerified = a.authLogin(email=email, password=oldPassword)
        if notVerified:
            if notVerified == 'Incorrect Password!!':
                return render_template('forgot-password.html', var=notVerified)
            elif notVerified == 'User Not Found!':
                return render_template('sign-up.html', var=notVerified)
        else:
            if conNewPassword != newPassword:
                return render_template('forgot-password.html', var="Password Doesn't Match!!")
            if newPassword == oldPassword:
                return render_template('forgot-password.html', var="Current Password Can't Be Your New Password!")
            validPass = a.authPass(newPassword)
            if validPass != True:
                return render_template('forgot-password.html', var=validPass)
            else:
                update.password(email=email, oldPassword=oldPassword, newPassword=newPassword)
                return render_template('login.html', var="Password Reset Successfull!")
    return render_template('forgot-password.html')

@app.route('/forgot-email', methods=['GET', 'POST'])
def forgotEmail():
    token = request.args.get('token')
    if (request.method == 'POST') and (not token):
        dataBase = db.Database()
        mail = SendEMail()
        username = request.form.get('username')
        password = request.form.get('password')
        newEmail = request.form.get('newEmail')
        notVerified = a.authLogin(email=newEmail, password=password)
        if notVerified:
            if notVerified == 'Incorrect Password!!':
                return render_template('forgot-email.html', var="Email Already Exists!")
            elif notVerified == 'User Not Found!':
                if a.authUser(username=username, password=password) == "Invalid Username or Password!":
                    return render_template('forgot-email.html', var="Invalid Username or Password!")
                else:
                    if t.checkUserInNotVerified(email=newEmail):
                        dataBase.deleteNotVerifiedUser(email=newEmail)
                    token = t.generateSignUpToken(username=username, email=newEmail, password=password)
                    subject = emailContent.subject["newEmailVerification"]
                    body = (emailContent.body["newEmailVerification"].format(username, token))
                    print(subject, "\n", body)
                    if mail.send(newEmail, subject=subject, body=body):
                        return render_template('forgot-email.html', var="Verification Mail has Been Sent To New Email!")
                    return render_template('forgot-email.html', var="Error Sending Email, Try Again!")
        else:
            return render_template("forgot-email.html", var='Email Already Exists!')
        return render_template('forgot-email.html')
    elif token:
        if data := t.isSignUpTokenValid(token=token):
            dataBase = db.Database()
            if data:
                update.email(username=data[0], newEmail=data[1], password=data[2])
                dataBase.deleteNotVerifiedUser(data[1])
                return render_template('login.html', var='Email Reset Successfull')
        return render_template("forgot-email.html", var="Invalid or Expired Token!")
    return render_template('forgot-email.html')

@app.route('/forgot-password-byEmail', methods=['GET', 'POST'])
def forgotPasswordByEmail():
    token = request.args.get('token')
    if (request.method == 'POST') and (not token):
        mail = SendEMail()
        dataBase = db.Database()
        email = request.form.get('email')
        dbEmail = dataBase.getEmail(email=email)
        username = dataBase.getUserByEmail(email=email)
        message = "User Not Found!"
        if dbEmail:
            if dbEmail[0] == email:
                dbuserId = dataBase.getUserId(email=email)[0]
                if t.checkTokenExists(dbuserId):
                    dataBase.deleteTokenById(dbuserId)
                token = t.generateResetToken(dbuserId)
                subject = emailContent.subject['resetPassword']
                body = (emailContent.body['resetPassword'].format(username[0], token))
                print(subject, "\n",body)
                if mail.send(recEmail=email, subject=subject, body=body):
                    return render_template('forgot-password-byEmail.html', var="Verification Mail has Been Sent!")
                message = "Error Sending Email, Try Again!"
        return render_template('forgot-password-byEmail.html', var=message)
    elif token:
        userId = t.isTokenValid(token=token)
        print(f"UserId: {userId}")
        if userId:
            return render_template('reset-password.html', token=token, userId=userId)
        return render_template('forgot-password-byEmail.html', var="Invalid or expired token!")
    return render_template('forgot-password-byEmail.html')

@app.route('/reset-password', methods=['POST'])
def resetPassword():
    dataBase = db.Database()
    userId = request.form.get('userId')
    token = request.form.get('token')
    newPassword = request.form.get('newPassword')
    confirmPassword = request.form.get('confirmNewPassword')
    if newPassword != confirmPassword:
        return render_template('reset-password.html', var="Passwords do not match", userId=userId, token=token)
    if dbPass := dataBase.getPassById(userId=userId):
        if newPassword == dbPass[0]:
            return render_template('reset-password.html', var="Current Password Can't be your New Password!", userId=userId, token=token)
    if tUserId := t.isTokenValid(token=token):
        if int(tUserId) == int(userId):
            validPass = a.authPass(newPassword)
            if validPass != True:
                return render_template('reset-password.html', var=validPass, userId=userId, token=token)
            # hashedPassword = a.hashPassword(newPassword)
            update.passById(userId=userId, newPassword=newPassword)
            update.deleteTokenById(userId=userId)
        return render_template('login.html', var="Password has been successfully reset!")
    else:
        return render_template('forgot-password-byEmail.html', var="Invalid or expired token!")

@app.route('/update-username', methods=['GET', 'POST'])
def updateUsername():
    if 'loggedIn' in session and session['loggedIn']:
        if request.method == 'POST':
            newName = request.form.get('newUsername')
            userId = request.form.get('userId')
            if not ((search(r"[A-Z]", newName)) or (search(r"[a-z]", newName))):
                return redirect('/')
            print(userId, newName, session['userId'])
            if session['userId'] == int(userId):
                print(userId, newName, session['userId'])
                update.username(session['userId'], newName)
    return redirect('/')

        #### Verification Section ####

# @app.route('/verify-sign-up', methods=['POST'])
# def verifySignUp():
#     dataBase = db.Database()
#     token = request.form.get('token')
#     if data := t.isSignUpTokenValid(token=token):
#         a.signUp(data[0], data[1], data[2])
#         dataBase.deleteNotVerifiedUser(email=data[1])
#         return render_template('login.html', var="Sign Up Successfull!")
#     return render_template('sign-up.html', var="Invalid or expired token.")


if __name__ == '__main__':
    PORT = 5000
    app.run(debug=True, port=PORT, threaded=True)