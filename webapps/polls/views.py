from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.views import generic

from django.utils import timezone

from .models import Question
# Create your views here.
def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #output = ', '.join([p.question_text for p in latest_question_list])
    #return HttpResponse(output)
    
    #template = loader.get_template('polls/index.html')
    #context = RequestContext(request, {'latest_question_list':latest_question_list,})
    #return HttpResponse(template.render(context))
    context = {'latest_question_list':latest_question_list}
    return render(request, 'polls/index.html', context)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        #return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    
def detail(request, question_id):
    #return HttpResponse("You're looking at question %s." % question_id)
    #try:
    #    question = Question.objects.get(pk=question_id)
    #except Question.DoesNotExist:
    #    raise Http404('Question does not exist.')
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html',{'question':question})
    
def results(request, question_id):
    #response = "You're looking at the results of question %s."
    #return HttpResponse(response % question_id)
    question = get_object_or_404(Question,pk=question_id)
    return render(request, 'polls/results.html', {'question':question})

def vote(request, question_id):
    #return HttpResponse("You're voting on question %s." % question_id)
    p = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',{
            'question':p,
            'error_message':"You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))