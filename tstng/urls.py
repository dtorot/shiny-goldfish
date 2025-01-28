from django.urls import path
from . import views

urlpatterns = [
    path('unicorns/', views.UnicornListView.as_view(), name='unicorns'),
]
