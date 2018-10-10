from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('verbackup', views.verbackup, name='verbackup'),
    path('backupDetails/<str:servidor>/<str:ip>/<int:porta>/', views.backupDetails, name='backupDetails'),
    path('verErrorlog', views.verErrorlog, name='verErrorlog'),
    path('JobsRunning', views.JobsRunning, name='JobsRunning'),    
    path('verBloqueio', views.verBloqueio, name='verBloqueio'),
    path('DuplicateIndex', views.DuplicateIndex, name='DuplicateIndex'),
]