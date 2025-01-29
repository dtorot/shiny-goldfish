from django.db import models

# Create your models here.
from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of fields

class Unicorn(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return self.name
    
