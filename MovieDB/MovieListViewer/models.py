from django.contrib.auth.models import User
from django.db import models

class Movie(models.Model):
    name = models.CharField(max_length=1024, blank=False, null=False)
    directory = models.CharField(max_length=1024, blank=False, null=False)

class Request(models.Model):
    user = models.ForeignKey(User, editable=False)
    name = models.CharField(max_length=1024, blank=False, null=False)
    year = models.CharField(max_length=4, blank=True, null=True)