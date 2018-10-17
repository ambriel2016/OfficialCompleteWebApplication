from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('urlsinput', views.urlsinput, name='urlsinput'),
    path('output', views.output, name='output'),
    path('dashboard', views.dashboard, name='dashboard'),

]
