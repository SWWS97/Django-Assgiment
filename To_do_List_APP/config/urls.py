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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from todo.views import todo_list, todo_info, todo_create, todo_update, todo_delete
from member.views import signup

urlpatterns = [
    path('admin/', admin.site.urls),

   # include
    path('', include('todo.urls')),
    path('fb/', include('todo.fbv_urls')),

    # login
    path('accounts/', include('django.contrib.auth.urls')),   # django 내장기능
    path('accounts/signup/', signup, name='signup'),
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:  # media(동적) 연결
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
