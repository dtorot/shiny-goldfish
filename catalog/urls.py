from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('paths/', views.PathListView.as_view(), name='paths'),
    path('path/<int:pk>', views.PathDetailView.as_view(), name='path-detail'),
    path('guaches/', views.GuacheListView.as_view(), name='guaches'),
    path('guaches/<int:pk>', views.GuacheDetailView.as_view(), name='guache-detail'),
]
