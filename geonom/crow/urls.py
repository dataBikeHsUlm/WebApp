from django.urls import path
from . import views

urlpatterns = [
#	path('', views.PersonCreateView.as_view(), name='index'),
        path('', views.index, name='index'),
]
