from django.contrib import admin
from .models import Task, Path, Learning, Guache

# Register your models here.
admin.site.register(Task)
#admin.site.register(Path)
#admin.site.register(Learning)
#admin.site.register(Guache)

class GuacheAdmin(admin.ModelAdmin):
    list_display=('last_name', 'first_name', 'karma')

admin.site.register(Guache, GuacheAdmin)


@admin.register(Path)
class PathAdmin(admin.ModelAdmin):
    list_display=('name', 'author', 'display_tasks')

@admin.register(Learning)
class LearningAdmin(admin.ModelAdmin):
    pass