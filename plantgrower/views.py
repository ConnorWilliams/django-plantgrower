from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}

    return render(request, 'plantgrower/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'plantgrower/detail.html', {'question': question})


def results(request, question_id):
    return HttpResponse("You're looking at the results of question %s." %
                        question_id
                        )


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
