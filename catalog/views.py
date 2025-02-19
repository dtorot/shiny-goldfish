from django.shortcuts import render
from django.views import generic

# Create your views here.
from .models import Task, Path, Learning, Guache

class PathListView(generic.ListView):
    model = Task
    context_object_name = 'path_list'

    #queryset = Path.objects.filter(name__icontains='linux')[:5]
    #template_name = 'paths/learning_paths_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(PathListView, self).get_context_data(**kwargs)
        #context = ['some_data'] = 'This is just some data'

        return context



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
