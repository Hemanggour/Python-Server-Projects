from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    goal = models.CharField(max_length=20, default='Goal')

    def __str__(self):
        return self.username


class Note(models.Model):
    notedescription = models.TextField()
    notes = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')

    def __str__(self):
        return self.notedescription


class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    userId = models.IntegerField(default=0)
    token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Token for {self.user.username}"


class VerifyEmail(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Verification for {self.username}"