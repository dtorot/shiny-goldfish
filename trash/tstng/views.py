from django.shortcuts import render
from django.views import generic
# Create your views here.

from .models import Unicorn

def index(request):

    num_unicorns = Unicorn.objects.all().count()

    context = {
        'num_unicorns': num_unicorns,
    }

    return render (request, 'index.html', context=context)

class UnicornListView(generic.ListView):
    model = Unicorn

    context_object_name = 'unicorn_list'

    template_name = 'tstng/unicorn_list.html'