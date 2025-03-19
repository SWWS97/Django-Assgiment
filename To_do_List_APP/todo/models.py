from django.contrib.auth.models import User
from django.db import models

from django.urls import reverse


class Todo(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # cd_views.py에서 사용하던 def get_success_url(self): 대신 models.py에 만들어 놓으면 cd_views.py에서 사용하던 model = Todo에서 model을 불러올때 알아서 get_absolute_url(self) 함수를 사용 한다
    # def get_absolute_url(self):
    #     return reverse('todo:detail', kwargs={'pk': self.pk})
