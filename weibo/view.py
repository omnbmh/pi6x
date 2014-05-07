from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import template
import datetime
from django.template.loader import get_template

def error(request):
    return HttpResponse("Ohh, error ~~~")

def ctime(req,num):
    try:
        num = int(num)
        num = str(num)
    except ValueError:
        raise Http404
    txt = 'url is [http://127.0.0.1:8080/time/%s/]' % num
    return HttpResponse(txt)
    
def hello(req):
    return HttpResponse("<h1>Hello World!</h1>")

def signin(req):
    t = get_template('signin.html')
    c = template.Context({})
    return HttpResponse(t.render(c))
    
def signout(req):
    req.session.clear()
    req.session.flush()
    return HttpResponseRedirect('signin')
    
def home(req):
    t = get_template('index.html')
    if 'user' in req.session:
        c = template.Context({'is_login':'true', 'nick':req.session['user']['nick'], 'name':req.session['user']['name']})
        html = t.render(c)
        return HttpResponse(html)
    return HttpResponseRedirect('signin')
def send(req, id):
    pass
    
    
def current_datetime(req):
    now = datetime.datetime.now()
    #fp = open('C:/omnbmh-wy/_my_project/Python/django/site/firstsite/templates/mytemplate.html')
    #t = template.Template(fp.read())
    t = get_template('mytemplate.html')
    #fp.close()
    html = t.render(template.Context({'current_date':now}))
    return HttpResponse(html)

def hours_add(request,offset):
    try:
        offset=int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset,dt)
    return HttpResponse(html)

def person(request):
    t = template.Template('My name is {{ name }}')
    c = template.Context({'name':'Fred'})
    return HttpResponse(t.render(c))