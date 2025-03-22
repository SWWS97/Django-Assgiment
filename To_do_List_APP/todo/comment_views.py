from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from todo.models import Comment, Todo


class CommentCreateView(CreateView):
    model = Comment
    fields = ['message']
    pk_url_kwarg = 'todo_id'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user

        # URL에서 todo_id 가져와서 연결된 Todo 찾기
        todo_id = self.kwargs.get('todo_id')
        self.object.todo = get_object_or_404(Todo, id=todo_id)

        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        # Comment의 pk가 아니라, 연결된 Todo의 pk 사용
        return reverse_lazy('todo:info', kwargs={'todo_id': self.object.todo.pk})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['message']

    def get_object(self, queryset=None):
        self.object = super().get_object()

        if self.request.user != self.object.user and not self.request.user.is_superuser:
            raise Http404

        return self.object

    def get_success_url(self):
        return reverse_lazy('todo:info', kwargs={'todo_id': self.object.todo.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_object(self, queryset=None):
        self.object = super().get_object()

        if self.request.user != self.object.user and not self.request.user.is_superuser:
            raise Http404

        return self.object

    def get_success_url(self):
        return reverse_lazy('todo:info', kwargs={'todo_id': self.object.todo.pk})