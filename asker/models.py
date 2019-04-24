# Create your models here.
from __future__ import unicode_literals

from datetime import datetime

import requests
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

class User(AbstractUser):

    upload = models.ImageField(upload_to='uploads/%Y/%m/%d/')

class Tag(models.Model):
    title = models.CharField(max_length=120, verbose_name=u"Заголовок ярлыка")

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class QuestionManager(models.Manager):

    def new(self):
        return self.order_by('-created_at')

    def best(self):
        return self.order_by('-rating')

class Question(models.Model):

    objects = QuestionManager()

    author = models.ForeignKey(
        to=Profile, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=128)
    text = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    tags = models.ManyToManyField(Tag, blank=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.pk} {self.title}"
    class Meta:
        ordering = ['-created_at']

class Answers(models.Model):

    author = models.ForeignKey(
        to=Profile, on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    correct = models.BooleanField(default=False)
    like = models.ManyToManyField(User, blank=False)
    rating = models.IntegerField(default=0)
    questions = models.ForeignKey(
        to=Question, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.pk} {self.text}"
    class Meta:
        ordering = ['-rating']

#@receiver(post_save, sender=Question)
#def renewal(sender, instance, created, **kwargs):
#    if created:
#        requests.post("http://localhost:8006/create/message", data={"message": instance.id})