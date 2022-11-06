from django.http import Http404
from django.shortcuts import render,redirect     #HttpResponse
from django.contrib.auth.decorators import login_required
from learning_app.models import Topic,Entry
from .forms import TopicForm,EntryForm

# Create your views here.



def index(request):
    """"学习笔记主页"""
    return render(request,'learning_app/index.html')


@login_required   #限制访问，如果没有登录会去setting.login_url重定向，只对下面这一个函数生效
def topics(request):
    """显示主题页面"""
    topics=Topic.objects.filter(owner=request.user).order_by('date_added')
    context={'topics':topics}
    return render(request,'learning_app/topics.html',context)

@login_required
def topic(request,topic_id):
    """显示单个主题及其所有条目"""
    topic=Topic.objects.get(id=topic_id)
    #确认请求的主题属于当前用户
    if topic.owner!=request.user:
        raise Http404
    entries=topic.entry_set.order_by('-date_added')
    context={'topic':topic, 'entries':entries}
    return render(request,'learning_app/topic.html',context)

@login_required
def new_topic(request):
    """添加新主题"""
    if request.method=='GET':
        #未提交数据，创建新表单
        form=TopicForm()
    else:
        #post 提交的数据：处理数据
        form=TopicForm(data=request.POST)
        if form.is_valid():
            new_topic=form.save(commit=False)
            new_topic.owner=request.user
            new_topic.save()
            return redirect('learning_app:topics')
    #显示空表单或者指出表单无数据
    context={'form':form}
    return render(request,'learning_app/new_topic.html',context)

@login_required
def new_entry(request, topic_id):
    """在特定主题添加新条目"""
    topic=Topic.objects.get(id=topic_id)
    if request =='GET':
        #未提交数据，创建空表
        form=EntryForm()
    else:
        #post请求，对数据处理
        form=EntryForm(data=request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            new_entry.topic=topic
            new_entry.save()
            return redirect('learning_app:topic',topic_id=topic_id)
    #显示空表或指出数据无效
    context={'topic':topic,'form':form}
    return render(request,'learning_app/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
    """编辑现有条目"""
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic
    if request.method=='GET':
        #初次请求，使用当前目录填充表单
        form=EntryForm(instance=entry)
    else:
        #post请求，处理提交的数据
        form=EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_app:topic',topic_id=topic.id)
    context={'entry':entry,'topic':topic,'form':form}
    return render(request,'learning_app/edit_entry.html/',context)

