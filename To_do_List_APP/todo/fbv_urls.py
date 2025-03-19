from django.urls import path

from todo import views

app_name = 'fb'

urlpatterns=[
    # FBV todo
    path('todo/', views.todo_list, name='list'),
    path('todo/<int:todo_id>/', views.todo_info, name='info'),
    # crud(FBV)
    path('todo/create/', views.todo_create, name='create'),
    path('todo/<int:todo_id>/update/', views.todo_update, name='update'),
    path('todo/<int:todo_id>/delete/', views.todo_delete, name='delete'),
]
