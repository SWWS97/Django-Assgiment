"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import Http404
from django.shortcuts import render, redirect
from fake_db import user_db

_db = user_db

# 홈 화면
def home(request):
    return render(request, 'home.html')

# 유저 리스트
def user_list(request):
    names = [{'id': key, 'name': value['이름']} for key, value in _db.items()]    # .items로 키와값을 두가지 다 들고온다.

    return render(request, 'user_list.html', {'data': names})

# 유저 상세 정보
def user_info(request, id):
    if id > len(_db):
        raise Http404('유저를 찾을수 없습니다.')
    info = _db[id]

    return render(request, 'user_info.html', {'data' : info})



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('users/', user_list, name='user_list'),
    path('users/<int:id>/', user_info, name='user_info')
]
