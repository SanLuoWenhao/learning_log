from django.shortcuts import render


# Create your views here.
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

# insert model.py class
from .models import Topic, Entry

# insert forms.py forms
from .forms import TopicForm
from .forms import EntryForm

def index(reqeust):
    """
    学习笔记的主页
    """
    return render(reqeust, 'learning_logs/index.html')
    # return HttpResponse('Nice!')


def topics(request):
    """
    显示所有的主题
    """
    topics = Topic.objects.order_by('date_added')

    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """
    显示每个主题的所有内容
    """
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')

    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def new_topic(request):

    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(resolve_url('topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request, topic_id):

    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topics'))

    context = {'form': form, 'topic': topic}
    return render(request, 'learning_logs/new_entry.html', context)


def edit_entry(request, entry_id):

    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != "POST":
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))

    context = {'topic': topic, 'form': form, 'entry': entry}
    return render(request, 'learning_logs/edit_entry.html', context)





