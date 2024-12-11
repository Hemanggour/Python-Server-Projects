from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import User, Chat

messages = []
messagesIds = []

def setSession(request, chatName, id):
    request.session['sessionId'] = id
    request.session['loggedIn'] = True


def getSession(request):
    id = request.session.get('sessionId')
    loggedIn = request.session.get('loggedIn')
    context = {
        'sessionId': id,
        'loggedIn': loggedIn,
    }
    return context


def deleteSession(request):
    try:
        del request.session['sessionId']
        del request.session['loggedIn']
        return HttpResponse('LoggedOut!!')
    except KeyError:
        return HttpResponse("Error")


def deleteChat(request):
    if request.method == 'POST':
        try :
            user_id = request.POST.get('sessionId')
            user = get_object_or_404(User, id=user_id)
            user.delete()
            return redirect('/chat/login')
        except Exception as e:
            print(f"Error in deleteChat: {e}")
    return HttpResponse("Invalid request method.", status=405)


def getUserid(chatName, password):
    try:
        user = User.objects.filter(chatName=chatName, password=password).first()
        if user:
            return user.id
        return None
    except User.DoesNotExist:
        return None


def getMessages(sessionId):
    user = User.objects.filter(id=sessionId).first()
    messagesObj = Chat.objects.filter(user_id=user.id)
    if messagesObj:
        return messagesObj
    return None


def delMessage(messageId):
    try:
        Chat.objects.filter(id=messageId).delete()
        return True
    except Exception as e:
        print(f"Error in delMessage: {e}")
        return False


def addMessage(id, message):
    user = User.objects.filter(id=id)
    if message and user:
        new_message = Chat(user=user[0], chats=message)
        new_message.save()
        return True
    return False


def chat(request):
    loggedIn = request.session.get('loggedIn', False)
    sessionId = request.session.get('sessionId', None)
    if (('loggedIn' in dict(request.session)) and request.session['loggedIn'] and sessionId):
    # if loggedIn and sessionId:
        if request.method == 'POST':
            if loggedIn:
                message = request.POST.get('userMessage')
                chatId = request.POST.get('sessionId')
                if message:
                    if message.count(" ") == len(message):
                        return redirect('/chat/')
                    else:
                        try:
                            if request.session['sessionId'] == int(chatId):
                                addMessage(id=int(chatId), message=message)
                        except Exception as e:
                            print(f"Error in chat POST: {e}")
                            return redirect('/chat/login')
                return redirect('/chat/')
            return redirect('/chat/login')
        elif loggedIn and sessionId:
            try:
                messages.clear()
                messagesIds.clear()
                messagesObj = getMessages(sessionId=sessionId)
                if messagesObj:
                    params = {
                        'loggedIn': loggedIn,
                        'messages': messagesObj,
                        'sessionId': sessionId,
                    }
                    return render(request, 'app/chat.html', params)
                params = {
                    'loggedIn': loggedIn,
                    'sessionId': sessionId,
                }
                return render(request, 'app/chat.html', params)
            except Exception as e:
                print(f"Error in chat get: {e}")
    return redirect('/chat/login')


def deleteMessage(request):
    try:
        if request.method == 'POST':
            loggedIn = request.session.get('loggedIn', False)
            sessionId = request.session.get('sessionId', None)
            if (('loggedIn' in dict(request.session)) and request.session['loggedIn'] and sessionId):
                if loggedIn:
                    messIdToDelete = request.POST.get('messIdToDelete')
                    delMessage(messageId=messIdToDelete)
        return redirect('/chat/')
    except Exception as e:
        print(f"Error in deleteMessage: {e}")
        return redirect('/chat/login')


def login(request):
    if request.method == 'POST':
        chatName = request.POST.get('chatName')
        password = request.POST.get('password')
        if id := getUserid(chatName, password=password):
            setSession(request, chatName=chatName, id=id)
            return redirect('/chat/')
        return redirect('/chat/sign-up')
    return render(request, 'app/login.html')


def signUp(request):
    if request.method == 'POST':
        chatName = request.POST.get('chatName')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        if not getUserid(chatName=chatName, password=password):
            user = User(chatName=chatName, password=password)
            user.save()
            return redirect('/chat/login')
    return render(request, 'app/signUp.html')

if __name__=='__main__':
    pass