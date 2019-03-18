from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from crow.forms import CrowForm
from django.views.generic import TemplateView
from datamodel.models import ZipDist
from datamodel.models import ZipDist_2digits
from datamodel.models import Zipcode
from django.template import RequestContext, Template
from NominatimLibrary import Locator


#from django.urls import path
#from . import views

class Distance(TemplateView):
    template_name='distance/index.html'
   
    def get(self,request):
        form = CrowForm()
        
        return render(request, self.template_name,{'form':form})

    def post(self,request):
        locator = Locator()
        form = CrowForm(request.POST)
        distance_dict = {}
        if form.is_valid():
            from_zip = form.cleaned_data['from_zip']
            from_iso = form.cleaned_data['from_iso']
            to_zip = form.cleaned_data['to_zip']
            to_iso = form.cleaned_data['to_iso']
            d_route = ZipDist.distance_between_postcodes(from_zip, from_iso, to_zip, to_iso)

            from_zipcode_obj = Zipcode.objects.get(country_iso=from_iso, zip_code=from_zip)
            from_coords = (from_zipcode_obj.lat, from_zipcode_obj.lon)
            to_zipcode_obj = Zipcode.objects.get(country_iso=to_iso, zip_code=to_zip)
            to_coords = (to_zipcode_obj.lat, to_zipcode_obj.lon)
            d_crow = locator.distance_crow_addrs(from_coords, to_coords)

            distance_dict = {'distance_route': str(d_route), 'distance_crow': str(d_crow)}

        return render (request, self.template_name, distance_dict)


