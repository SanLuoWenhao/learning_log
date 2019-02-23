from django.shortcuts import render

# Create your views here.
from django.http import HttpRequest
from django.http import HttpResponse
from learning_logs.models import Topic

def index(reqeust):
    """
    学习笔记的主页
    """
    return render(reqeust, 'learning_logs/index.html')
    # return HttpResponse('Nice!')

def topics(request):
    """
    显示所有的主题
    :param request:
    :return:
    """
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)