"""为应用程序users定义url"""

# from django import urls
# urls.path    urls.include
from django.urls import path,include
from users import views

app_name='users'
urlpatterns=[
    #包含默认程序的身份验证
    path('',include('django.contrib.auth.urls')),
    #注册页面
    path('register/',views.register,name='register')
]







