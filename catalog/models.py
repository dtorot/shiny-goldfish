from django.db import models

# Create your models here.
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower


class Task(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Knowledge task item...",
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('task-detail', args=[str(self.id)])
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='task_name_case_insensitive_unique',
                violation_error_message="Task already exists (case insensitive match)"
            ),
        ]

class Path (models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)

    summary = models.TextField(
        max_length=1000,
        help_text= "A Brief description of the book",        
    )
    
    refcode = models.CharField(
        'RefCode',
        max_length=13,

    )

    task = models.ManyToManyField(
        Task, 
        help_text="Select tasks for this path",
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('path-detail', args=[str(self.id)])
    
