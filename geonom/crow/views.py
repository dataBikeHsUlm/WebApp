from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from crow.forms import CrowForm
from django.views.generic import TemplateView
from datamodel.models import ZipDist
from datamodel.models import ZipDist_2digits
from datamodel.models import Zipcode
from django.template import RequestContext, Template


#from django.urls import path
#from . import views

class Distance(TemplateView):
    template_name='distance/index.html'
   
    def get(self,request):
        form = CrowForm()
        
        return render(request, self.template_name,{'form':form})

    def post(self,request):
        form = CrowForm(request.POST)
        distance_dict = {}
        if form.is_valid():
            from_zip = form.cleaned_data['from_zip']
            from_iso = form.cleaned_data['from_iso']
            to_zip = form.cleaned_data['to_zip']
            to_iso = form.cleaned_data['to_iso']
            d = ZipDist.distance_between_postcodes(from_zip, from_iso, to_zip, to_iso) 
            distance = str(d) 
            distance_dict = {'d': distance}

        return render (request, self.template_name, distance_dict)


