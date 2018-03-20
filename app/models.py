from __future__ import unicode_literals
from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User

############################################################
from vote.models import VoteModel

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    word = models.CharField(max_length=80)
    explanation = models.TextField()

    def __str__(self):
        return self.author.first_name

############################################

# Create your models here.
class Question(models.Model):
	name = models.TextField(max_length = 500)
	uid = models.CharField(max_length=500)
	qid=models.IntegerField(primary_key=True)
	boolValue = models.BooleanField(default=False)
	#category = models.CharField(auto_now_add=True)

class User(models.Model):
	name=models.CharField(max_length = 500)
	uid = models.CharField(max_length=500)
	password = models.CharField(max_length=500)

class Answer(VoteModel, models.Model):
	name = models.TextField(max_length = 500)
	uid = models.CharField(max_length = 500)
	quesid=models.IntegerField()
	aid=models.CharField(max_length = 500)
	voting = models.IntegerField()