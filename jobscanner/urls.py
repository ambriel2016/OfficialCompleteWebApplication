from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('urlsinput', views.urlsinput, name='urlsinput'),
    path('output', views.output, name='output'),

]
