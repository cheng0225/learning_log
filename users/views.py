from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def register(request):
    """注册用户"""
    if request.method=='GET':
        #显示空表单
        form=UserCreationForm()
    else:
        #POST处理提交的数据
        form=UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user=form.save()
            #让用户自动登录，然后重定向到主页
            login(request,new_user)
            return redirect('learning_app:index')
    #显示空表单或者数据无效
    context={'form':form}
    return render(request,'registration/register.html',context)