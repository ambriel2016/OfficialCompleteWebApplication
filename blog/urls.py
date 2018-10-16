from django.urls import path
from . import views

urlpatterns = [
	path('', views.allblogs, name='allblogs'),
	# look for in int after blog and call it id
	path('<int:blog_id>', views.detail, name='detail'),
]
