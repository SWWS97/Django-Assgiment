from django.urls import path

from todo import cb_views

app_name = 'todo'

urlpatterns = [
 # CBV todo
    path('todo/', cb_views.TodoListView.as_view(), name='list'),
    path('todo/<int:todo_id>/', cb_views.TodoDetailView.as_view(), name='info'),
    path('todo/create/', cb_views.TodoCreateView.as_view(), name='create'),
    path('todo/<int:todo_id>/update/', cb_views.TodoUpdateView.as_view(), name='update'),
    path('todo/<int:todo_id>/delete/', cb_views.TodoDeleteView.as_view(), name='delete'),
]
