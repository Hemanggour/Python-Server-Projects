from django.shortcuts import render, redirect
from django.http import Http404
import secrets

chats = {}
tokens = set()

def generateToken():
    return secrets.token_hex(32)

def home(request):
    return render(request, 'pvtApp/home.html')

def chat(request):
    token = request.GET.get('token')
    if request.method == 'GET' and token:
        if token in tokens:
            params = {
                'messages': chats.get(token, []),
                'token': token,
            }
            return render(request, 'pvtApp/chat.html', params)
        else:
            # raise Http404("Chat not found.")
            return redirect('/privateChat')
    elif request.method == 'POST':
        token = request.POST.get('token')
        if token in tokens:
            message = request.POST.get('message')
            if message and message.strip():
                chats[token].append(message)
            return redirect(f"/privateChat/chat?token={token}")
    return redirect('/privateChat')

def create(request):
    if request.method == 'GET':
        token = generateToken()
        tokens.add(token)
        chats[token] = []
        url = f'/privateChat/chat?token={token}'
        return redirect(url)

def deleteChat(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        if token in tokens:
            chats.pop(token, None)
            tokens.remove(token)
        return redirect('/privateChat')