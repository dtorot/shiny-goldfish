from django.db import models

# Create your models here.
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
import uuid


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
    #author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)

    summary = models.TextField(
        max_length=1000,
        help_text= "A Brief description of the Path",        
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
    

class Learning(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this particular learning path",
    )

    path = models.ForeignKey(
        'Path',
        on_delete=models.RESTRICT,
        null=True,
    )

    begin = models.DateField(null=True, blank=True)

    PATH_STATUS = (
        ('w','Walking'),
        ('m','Maintenance'),
        ('d','In debt'),
        ('l','Lost'),
        ('c','Completed path'),
    )

    status = models.CharField(
        max_length=1,
        choices=PATH_STATUS,
        blank=True,
        default='w',
        help_text="Status of the Learning Path",
    )

    class Meta:
        ordering = ['begin']

    def __str__(self):
        return f'{self.id} ({self.path.name})'
    
