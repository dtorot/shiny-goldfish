from django.shortcuts import render

# Create your views here.
from .models import Task, Path, Learning, Guache

def index(request):
    num_paths = Task.objects.all().count()
    num_learning_paths = Learning.objects.all().count()

    num_learning_paths_active = Learning.objects.filter(status__exact='w').count()

    num_guaches = Guache.objects.count()

    context = {
        'num_paths': num_paths,
        'num_learning_paths': num_learning_paths,
        'num_learning_paths_active': num_learning_paths_active,
        'num_guaches': num_guaches,
    }

    return render(request, 'index.html', context=context)
