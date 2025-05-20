from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('paths/', views.PathListView.as_view(), name='paths'),
    path('path/<int:pk>', views.PathDetailView.as_view(), name='path-detail'),
    path('guaches/', views.GuacheListView.as_view(), name='guaches'),
    path('guaches/<int:pk>', views.GuacheDetailView.as_view(), name='guache-detail'),
    path('mylearnings/', views.LearningsByUserListView.as_view(), name='my-learnings'),
    path('learnings/', views.LearningsByStaffListView.as_view(), name='learnings'),
    path('learning/<int:pk>', views.LearningDetailView.as_view(), name='learning-detail'),
    path('learning/<int:pk>/renew/', views.renew_learning_master, name='renew-learning-master'),
]
