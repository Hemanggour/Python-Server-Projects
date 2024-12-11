from django.db import models

class User(models.Model):
    chatName = models.CharField(max_length=50)
    password = models.CharField(max_length=255)

class Chat(models.Model):
    chats = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)