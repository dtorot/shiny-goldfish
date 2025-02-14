from django.db import models

# Create your models here.
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
import uuid

# The minimal unit of learning
class Task(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Knowledge task item...",
    )

    #Author of this Task
    creator = models.ForeignKey(
        'Guache',         
        on_delete=models.RESTRICT, 
        null=True,
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


# The user of the system: a warrior. Maybe act like an apprentice or a sensei
class Guache (models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)

    date_of_birth = models.DateField(null=True, blank=True)
    last_visit_date = models.DateField('last in', null=True, blank=True)

    karma=models.IntegerField()

    class Meta:
        ordering=['last_name','first_name']

    def get_absolute_url(self):
        return reverse ('guache-detail', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.last_name},{self.first_name}'


# A planned learning Path
# a Path contains one or more "Learning Tasks"
class Path (models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(
        'Guache', 
        related_name="author_paths",
        on_delete=models.RESTRICT, 
        null=True,
    )
    apprentice = models.ManyToManyField(
        Guache, 
        related_name="learning_paths",
        help_text="Add a new Apprentice to this Learning Path",
    )

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
    
    # ...get the related Learning Tasks to this Learning Path
    def display_tasks(self):
        return ', '.join(task.name for task in self.task.all()[:3])
    
    display_tasks.short_description ='Some Tasks included in this path...'
 

   
# The particular execution of a learning Path of a specific Guache
# A Guache can have one or more Learnings in execution (state defined in status)
class Learning(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this particular learning path",
    )

    name = models.CharField(max_length=500, null=True)

    apprentice = models.ForeignKey('Guache', on_delete=models.RESTRICT, null=True)
    
    path = models.ForeignKey(
        'Path',
        on_delete=models.RESTRICT,
        null=True,
    )

    last_visit = models.DateField(null=True, blank=True)

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

    birth = models.DateField(null=True,blank=True)

    class Meta:
        ordering = ['birth']

    def __str__(self):
        return f'{self.id} ({self.path.name})'
    
