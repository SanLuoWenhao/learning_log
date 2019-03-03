from django.shortcuts import render

# Create your views here.
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
# insert model.py class
from .models import Topic, Entry
# insert forms.py forms
from .forms import TopicForm
from .forms import EntryForm
# insert django.contrib
from django.contrib.auth.decorators import login_required


def index(reqeust):
    """
    学习笔记的主页
    """
    return render(reqeust, 'learning_logs/index.html')
    # return HttpResponse('Nice!')

@login_required
def topics(request):
    """
    显示所有的主题
    """
    # topics = Topic.objects.order_by('date_added')
    #只向用户显示属于自己的主题
    topics = Topic.objects.filter(ower=request.user).order_by('date_added')

    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """
    显示每个主题的所有内容
    """
    topic = Topic.objects.get(id=topic_id)

    # 确认请求的主题属于当前用户
    if topic.ower != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')

    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):

    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.ower = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):

    topic = Topic.objects.get(id=topic_id)

    # 确认请求的主题属于当前用户
    if topic.ower != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

    context = {'form': form, 'topic': topic}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):

    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    # 确认请求的主题属于当前用户
    if topic.ower != request.user:
        raise Http404

    if request.method != "POST":
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

    context = {'topic': topic, 'form': form, 'entry': entry}
    return render(request, 'learning_logs/edit_entry.html', context)





