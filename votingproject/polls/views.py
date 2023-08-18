from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .forms import CreatePoll
from .models import Poll
from django.contrib import messages
def home(request):
    polls = Poll.objects.all().order_by('question_text')
    context = {
        'polls' : polls
    }
    return render(request, 'polls/home.html', context)

def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    if request.method == 'POST':

        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.op_one_count += 1
        elif selected_option == 'option2':
            poll.op_two_count += 1
        elif selected_option == 'option3':
            poll.op_three_count += 1
        elif selected_option == 'option4':
            poll.op_four_count += 1
        else:
            return HttpResponse(400, 'Invalid form')

        poll.save()

        return redirect('results', poll.id)

    context = {
        'poll' : poll
    }
    return render(request, 'polls/vote.html', context)

def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    poll_owner = User.objects.get(pk=poll.owner)
    context = {
        'poll' : poll,
        'poll_owner' : poll_owner
    }
    return render(request, 'polls/results.html', context)
def search_polls(request):
    if request.method == "POST":
        searched = request.POST['searched']
        polls = Poll.objects.filter(question_text__contains=searched)
        return render(request, 'polls/search_polls.html', {"searched":searched, "polls":polls})
    else:
        return render(request, 'polls/search_polls.html')
def update_polls (request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    if request.user.id == poll.owner:
        form = CreatePoll(request.POST or None, instance=poll)
        if form.is_valid():
            form.save()
            return redirect('home')
        context = {
            'form' : form,
            'poll' : poll
        }
        return render(request, 'polls/update_polls.html', context)
    else:
        messages.success(request,("Can not update this poll since you are not the owner !"))
        return redirect('home')
def create(request):
    if request.method == 'POST':
        form = CreatePoll(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.owner = request.user.id
            poll.save()
            return redirect('home')
    else:
        form = CreatePoll()
    context = {
        'form' : form
    }
    return render(request, 'polls/create.html', context)
def delete_polls (request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    if request.user.id == poll.owner:
        poll.delete()
        messages.success(request,("Poll Deleted !"))
        return redirect('home')
    else:
        messages.success(request,("Can not delete this poll since you are not the owner !"))
        return redirect('home')

def resultData (request, poll_id):
    question = Poll.objects.get(id=poll_id)
    votedata = [{question.op_one:question.op_one_count}, {question.op_two:question.op_two_count}, {question.op_three:question.op_three_count}, {question.op_four:question.op_four_count}]
    print(votedata)
    return JsonResponse(votedata, safe=False)
def my_polls(request):
    if request.user.is_authenticated:
        me = request.user.id
        polls = Poll.objects.filter(owner = me)
        return render(request, 'polls/my_poll.html', {"polls":polls})
    else:
        messages.success(request,("Please Log in to watch this page"))
        return redirect('home')


