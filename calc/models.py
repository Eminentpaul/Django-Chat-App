from django.db import models
from django_resized import ResizedImageField

# Create your models here.

class Accounts(models.Model):
    username = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    image = ResizedImageField(size=[690, 501], upload_to='pics')
    login_status = models.CharField(max_length=20, default='Offline')
    msg_status = models.CharField(max_length=20)

class Posts(models.Model):
    username = models.CharField(max_length=100)
    title = models.CharField(max_length=500)
    contents = models.TextField()
    image = models.ImageField(upload_to='pics')
    date_posted = models.DateTimeField()


class Chats(models.Model):
    sender_username = models.CharField(max_length=100)
    receiver_username = models.CharField(max_length=100)
    messages = models.TextField()
    msg_date = models.DateTimeField()
    msg_status = models.CharField(max_length=20, default='Unread')

