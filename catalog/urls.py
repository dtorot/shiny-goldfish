from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('paths/', views.PathListView.as_view(), name='paths'),
    path('path/<int:pk>', views.PathDetailView.as_view(), name='path-detail'),
    path('path/create/', views.PathCreate.as_view(), name='path-create'),
    path('path/<int:pk>/update/', views.PathUpdate.as_view(), name='path-update'),
    path('path/<int:pk>/delete/', views.PathDelete.as_view(), name='path-delete'),
    path('guaches/', views.GuacheListView.as_view(), name='guaches'),
    path('guaches/<int:pk>', views.GuacheDetailView.as_view(), name='guache-detail'),
    path('guache/create/', views.GuacheCreate.as_view(), name='guache-create'),
    path('guache/<int:pk>/update/', views.GuacheUpdate.as_view(), name='guache-update'),
    path('guaches/<int:pk>/delete/', views.GuacheDelete.as_view(), name='guache-delete'),
    path('mylearnings/', views.LearningsByUserListView.as_view(), name='my-learnings'),
    path('learnings/', views.LearningsByStaffListView.as_view(), name='learnings'),
    path('learning/<int:pk>', views.LearningDetailView.as_view(), name='learning-detail'),
    path('learning/<int:pk>/renew/', views.renew_learning_master, name='learninginstance_list_staff_user'),    
]
