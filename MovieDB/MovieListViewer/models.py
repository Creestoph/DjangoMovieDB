from django.db import models

class Movie(models.Model):
    name = models.CharField(max_length=1024, blank=False, null=False)
    directory = models.CharField(max_length=1024, blank=False, null=False)
