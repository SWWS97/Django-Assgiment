from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request, Http404, HttpResponseRedirect

from todo.models import Todo


class TodoListView(LoginRequiredMixin,ListView):
    queryset = Todo.objects.all()
    template_name = 'todo_list.html'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_superuser:
            q = self.request.GET.get('q')

            if q:
                queryset = queryset.filter(
                    Q(title__icontains=q) |
                    Q(description__icontains=q)
                )
            return queryset

        q = self.request.GET.get('q')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )

        return queryset.filter(user=self.request.user)


class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = 'todo_info.html'
    pk_url_kwarg = 'todo_id'

    def get_object(self, queryset=None):
        self.object = super().get_object()

        if self.request.user != self.object.user and not self.request.user.is_superuser:
            raise Http404

        return self.object

    def get_context_dat(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {'todo': self.object.__dict__}

        return context


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = 'todo_create.html'
    fields = ('title', 'description')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self): # "FBV"에서 reverse 부분
        return reverse_lazy('todo:info', kwargs={'todo_id': self.object.pk})


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    template_name = 'todo_update.html'
    fields = ['title', 'description','is_completed']
    pk_url_kwarg = 'todo_id'

    def get_object(self, queryset=None):
        self.object = super().get_object()

        if self.request.user != self.object.user and not self.request.user.is_superuser:
            raise Http404

        return self.object

    def get_success_url(self): # "FBV"에서 reverse 부분
        return reverse_lazy('todo:info', kwargs={'todo_id': self.object.pk})


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    pk_url_kwarg = 'todo_id'

    def get_object(self, queryset=None):
        self.object = super().get_object()

        if self.request.user != self.object.user and not self.request.user.is_superuser:
            raise Http404

        return self.object

    def get_success_url(self):  # "FBV"에서 reverse 부분
        return reverse_lazy('todo:list')



