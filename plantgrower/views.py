from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from .models import Grow
from django.views import generic
from django.utils import timezone
from .forms import GrowForm




def new_grow(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GrowForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GrowForm()

    return render(request, 'plantgrower/index.html', {'form': form})


class Details(generic.DetailView):
    model = Grow
    template_name = 'plantgrower/detail.html'

    def get_queryset(self):
            """
            Excludes any questions that aren't published yet.
            """
            return Grow.objects.all()
#
#
# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'plantgrower/results.html'
#
#
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
