import logging

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Grow
from .forms import GrowForm

logger = logging.getLogger(__name__)


def index(request):
    if Grow.objects.filter(status='1'):
        logger.info("Active grow found")
        return current_grow(request)
    else:
        logger.info("No active grows")
        return new_grow(request)


def new_grow(request):
    if request.method == 'POST':
        logger.info("Received POST")
        form = GrowForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/plantgrower/')
    else:
        logger.info("No POST")
        if not Grow.objects.filter(status='1'):
            form = GrowForm()
        else:
            logger.info("Showing active grow")
            return HttpResponseRedirect('/plantgrower/')

    return render(request, 'plantgrower/newgrow.html', {'form': form})


def current_grow(request):
    grow = Grow.objects.filter(status='1')[0]
    return render(request, 'plantgrower/currentgrow.html', {'grow': grow})


def edit_grow(request, grow_id):
    logger.info("Editing")
    grow = get_object_or_404(Grow, pk=grow_id)
    if request.method == 'POST':
        logger.info("Received POST")
        form = GrowForm(request.POST, instance=grow)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/plantgrower/')
    else:
        logger.info("No POST")
        form = GrowForm(instance=grow)

    return render(
        request, 'plantgrower/editgrow.html', {'form': form, 'grow': grow}
    )


def all_grows(request):
    grows = Grow.objects.all()
    output = '</br>'.join([str(grow) for grow in grows])
    return HttpResponse(output)

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'plantgrower/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse(
#             'plantgrower:results',
#             args=(question.id,)
#         ))
