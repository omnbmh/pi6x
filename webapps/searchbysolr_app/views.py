from django.http import HttpResponse
from django.template import loader


# Create your views here.
def index(req):
    template = loader.get_template('searchbysolr/index.html')
    context = {}
    return HttpResponse(template.render(context, req))
    
def search(req):
    key = ''
    # request solr result
    template = loader.get_template('searchbysolr/index.html')
    context = {}
    return HttpResponse(template.render(context, req))