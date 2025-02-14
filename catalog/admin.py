from django.contrib import admin
from .models import Task, Path, Learning, Guache

# Register your models here.
admin.site.register(Task)
#admin.site.register(Path)
#admin.site.register(Learning)
#admin.site.register(Guache)
#admin.site.register(Guache, GuacheAdmin)

@admin.register(Guache)
class GuacheAdmin(admin.ModelAdmin):
    list_display=('last_name', 'first_name', 'karma')
    fields = [
        'first_name',
        'last_name',
        (
            'date_of_birth',
            'last_visit_date'
        )
    ]

@admin.register(Learning)
class LearningAdmin(admin.ModelAdmin):
    list_display = ('id', 'apprentice','birth')
    list_filter = ('status','birth')

    fieldsets = (
        (
            None, {
                'fields':('name', 'path', 'id', 'apprentice')
            }
        ),
        (
            'Learning Status', {
                'fields': ('status',('birth','last_visit'))
            }
        ),
    )

class LearningInline(admin.TabularInline):
    model = (Learning)
    extra = 0

@admin.register(Path)
class PathAdmin(admin.ModelAdmin):
    list_display=('name', 'author', 'display_tasks')

    inlines=[LearningInline]


