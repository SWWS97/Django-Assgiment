from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.views.decorators.http import require_http_methods

from .form import TodoForm, TodoUpdateForm
from todo.models import Todo
from django.urls import reverse



@login_required
def todo_list(request):
    todos = Todo.objects.filter(user_id=request.user.id).order_by('-created_at')

    q = request.GET.get('q')
    if q:
        todos = todos.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )

    paginator = Paginator(todos, 10)
    page = request.GET.get('page')
    page_object = paginator.get_page(page)

    context = {
        'page_object' : page_object,
    }

    return render(request, 'todo_list.html', context)



@login_required
def todo_info(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    context = {
        'todo' : todo,
    }

    return render(request, 'todo_info.html', context)



@login_required()
def todo_create(request):

    form = TodoForm(request.POST or None)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()

        # return redirect(reverse('todo_info', kwargs={'pk': todo.pk}))
        return redirect('todo:info', todo_id=todo.id) # 직접 뷰 이름과 매개변수를 전달

    context = {
        'form' : form,
    }

    return render(request, 'todo_create.html', context)



@login_required
def todo_update(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)

    form = TodoUpdateForm(request.POST or None, instance=todo)  # 사용자가 입력한 값으로 폼을 채움, 아직 수정,저장 된건 아님
    if form.is_valid(): # 입력한 폼이 유효한지 검사
        form.save()     # 유효하면 기존 todo 객체를 업데이트 (DB에 저장)
        # return redirect(reverse('todo_info', kwargs={'pk': todo.pk}))
        return redirect('todo:info', todo_id=todo.pk) # 수정한 해당 상세 페이지(todo/pk/로 이동)

    context = {
        'form' : form,
    }

    # 위의 POST가 아닌 GET 요청일경우 업데이트 폼이 만들어진 'todo_update.html' 페이지로 이동
    return render(request, 'todo_update.html', context)



@login_required
@require_http_methods(['POST'])
def todo_delete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()

    # return redirect(reverse('todo_list'))
    return redirect('todo:list')





