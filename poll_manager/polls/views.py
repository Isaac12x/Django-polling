from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader, RequestContext
from django.shortcuts import render
from models import Poll, Choice, Votes, PollForm, ChoiceForm

# Create your views here.
def index(request):
	return render_to_response('index.html', context_instance = RequestContext(request),)

def add_poll(request):
	# calls the PollForm we created and displays it on the page
	if request.method == 'POST':
		form = PollForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('../.')
	else:
		form = PollForm()
	return render_to_response('add_poll.html', {'form': form}, context_instance = RequestContext(request),)


def add_choice(request, poll_id):
	poll = Poll.objects.get(id=poll_id)
	if request.method == 'POST':
		form = ChoiceForm(request.POST)
		if form.is_valid():
			#uses false commit to save the poll as the current poll ID, sets initial vote to 0, and saves all choices the user
			#has put in the form
			add_poll = form.save(commit=False)
			add_poll.poll = poll
			add_poll.vote = 0
			add_poll.save()
			form.save()
		return HttpResponseRedirect('../.')
		else:
			form = ChoiceForm()
		return render_to_response('add_choices.html', {'form': form, 'poll_id': poll_id,}, context_instance=RequestContext(request,),)


def view_polls(request):
	poll_query = Poll.objects.all().order_by('date')
	return render_to_response('polls.html', {'poll_query': poll_query, })


def view_single_poll(request, poll_id):
	poll = Poll.objects.get(id=poll_id)
	choices = poll.choice_set.all().order_by('id')
	return render_to_response('poll_info.html', {'poll': poll, 'choices': choices,}, context_instance=RequestContext(request,),)


def add_vote(request, poll_id):
	poll = Poll.objects.get(id=poll_id)
	choice = Choice.objects.filter(poll=poll_id).order_by('id')
	if request.method == 'POST':
		vote = request.POST.get('choice')
		if vote:
			vote = Choice.objects.get(id=vote)
			# saves the poll id, user id, and choice to the votes table
			v = Votes(poll=poll, choiceVote = vote)
			v.save()
			# redirects the user to the results page after they submit their vote
			return HttpResponseRedirect('../.')
		return render_to_response('votes.html', {'choice': choice, 'poll': poll, 'vcount': vcount,}, context_instance=RequestContext(request))

def view_results(request, poll_id):
	# display the choices and number of votes they have - displaying the number of votes is done in the  view_results template
	poll = Poll.objects.get(id=poll_id)
	choices = poll.choice_set.all()
	return render_to_response('poll_info.html', vars())
