from django.http import HttpResponse
from datamodel.models import ZipDist_2digits
from datamodel.models import Zipcode
#def index(request):
#	return HttpResponse("Geooocoocccoooooooooder")

def index(request):
    all_distances = ZipDist.objects.all()
    html = ''
    for distance in all_distances:
        url = '/distance/' + str(distance.id) + '/'
        html += '<a href ="' + url + '">' + str(distance.distance_fly) + '</a><br>'
    return HttpResponse(html)
