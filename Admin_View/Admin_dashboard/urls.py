from django.urls import path
from . import views
urlpatterns = [

    path('', views.query, name=''),
    path('sidebar/', views.query, name='sidebar'),
    path('home/', views.home, name='home'),
    path('letterform/', views.home, name='letterform'),
    path('home/', views.home, name='home'),
    path('allpackages/', views.all_packages, name='allpackages'),
    path('pendingpackages/', views.pendingpackages, name='pendingpackages'),
    path('collectedpackages/', views.collectedpackages, name='collectedpackages'),
    path('notification/', views.notification, name='notification'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('members',views.members,name='members')
    # path('home.html/', views.home, name='home')



]