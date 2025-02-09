from django.contrib import admin
from .models import Task, Path, Learning, Guache

# Register your models here.
admin.site.register(Task)
admin.site.register(Path)
admin.site.register(Learning)
admin.site.register(Guache)
