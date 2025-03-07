from django.shortcuts import render
from django.views import generic

# Create your views here.
from .models import Task, Path, Learning, Guache

class PathListView(generic.ListView):
    model = Path
    context_object_name = 'path_list'

    paginate_by = 3

    #queryset = Path.objects.filter(name__icontains='linux')[:5]
    #template_name = 'paths/learning_paths_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(PathListView, self).get_context_data(**kwargs)
        #context = ['some_data'] = 'This is just some data'

        return context

class PathDetailView(generic.DetailView):
    model = Path

def index(request):
    num_paths = Path.objects.all().count()
    num_learning_paths = Learning.objects.all().count()

    num_learning_paths_active = Learning.objects.filter(status__exact='w').count()

    num_guaches = Guache.objects.count()

    # Visits counter
    visits = request.session.get('visits',0)
    visits += 1
    request.session['visits'] = visits

    context = {
        'num_paths': num_paths,
        'num_learning_paths': num_learning_paths,
        'num_learning_paths_active': num_learning_paths_active,
        'num_guaches': num_guaches,
        'visits': visits,
    }

    return render(request, 'index.html', context=context)


class GuacheListView(generic.ListView):
    model = Guache
    context_object_name = 'guache_list'

    #queryset = Path.objects.filter(name__icontains='linux')[:5]
    #template_name = 'paths/learning_paths_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(GuacheListView, self).get_context_data(**kwargs)
        #context = ['some_data'] = 'This is just some data'

        return context

class GuacheDetailView(generic.DetailView):
    model = Guache