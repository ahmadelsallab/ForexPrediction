from django.shortcuts import render
from django.template import RequestContext, loader
from django.views import generic

# Create your views here.
from django.http import HttpResponse
from app.models import NewsHeadline
#from DatasetBuilder.DatasetBuilder import DatasetBuilder
def main(request):
    
            
    # Render the response
    #--------------------   
            
    # Load the main page template
    template = loader.get_template('app/main.html')
    
    # Fill the query list
    headlines_list = NewsHeadline.objects.order_by('text')[:1000]
    
    # Render with the query
    context = RequestContext(request, {'headlines_list' : headlines_list})
   
    return HttpResponse(template.render(context))

