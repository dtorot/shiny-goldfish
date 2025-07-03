import datetime

from django.shortcuts import render, get_object_or_404
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.contrib.auth.decorators import login_required, permission_required

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from catalog.forms import RenewLearningForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Guache


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


class LearningsByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = Learning
    context_object_name = 'learning_list'
    template_name = 'catalog/learninginstance_list_apprentice_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            Learning.objects.filter(apprentice=self.request.user).filter(status__exact='d')
            #.filter(status__exact='d')
            #.order_by('due_back')
        )

class LearningsByStaffListView(PermissionRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = Learning
    context_object_name = 'staff_learning_list'
    template_name = 'catalog/learninginstance_list_staff_user.html'
    paginate_by = 10

    permission_required = (
    #    'can_mark_completed',
        'catalog.change_learning',
    #    'login_required',
    )

    def get_queryset(self):
        return (
            Learning.objects.all()
        )


class LearningDetailView(generic.DetailView):
    model = Learning

def renew_learning_master(request, pk):
    learning = get_object_or_404(Learning, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewLearningForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            learning.due_back = form.cleaned_data['renewal_date']
            learning.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('learnings'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewLearningForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'learning': learning,
    }

    return render(request, 'catalog/learning_renew_master.html', context)

class GuacheCreate(PermissionRequiredMixin, CreateView):
    model = Guache
    fields = ['first_name', 'last_name', 'date_of_birth', 'karma', 'last_visit_date']
    initial = {'last_visit_date': '11/11/2023'}
    permission_required = 'catalog.add_guache'

class GuacheUpdate(PermissionRequiredMixin, UpdateView):
    model = Guache
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    permission_required = 'catalog.change_guache'

class GuacheDelete(PermissionRequiredMixin, DeleteView):
    model = Guache
    success_url = reverse_lazy('guaches')
    permission_required = 'catalog.delete_guache'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("guache-delete", kwargs={"pk": self.object.pk})
            )
        
class PathCreate(PermissionRequiredMixin, CreateView):
    model = Path
    fields = ['name', 'author', 'summary', 'refcode', 'task']
    permission_required = 'catalog.add_path'

class PathUpdate(PermissionRequiredMixin, UpdateView):
    model = Path
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    permission_required = 'catalog.change_path'

class PathDelete(PermissionRequiredMixin, DeleteView):
    model = Path
    success_url = reverse_lazy('paths')
    permission_required = 'catalog.delete_path'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("path-delete", kwargs={"pk": self.object.pk})
            )
