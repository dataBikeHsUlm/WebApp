from django.shortcuts import render

# Create your views here.
from crow.models import Distance

#from django.views.generic import CreateView
#from .models import Person

#class PersonCreateView(CreateView):
  #  model = Distance
  #  fields = 'distance'

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Distance.objects.all().count()
    context = {
        'num_books': num_books,
    }

  # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
