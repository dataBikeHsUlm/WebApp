from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
#	path('', views.PersonCreateView.as_view(), name='index'),
        path('', views.index, name='index'),
	path(r'distance',TemplateView.as_view(template_name='distance/index.html')),
]
