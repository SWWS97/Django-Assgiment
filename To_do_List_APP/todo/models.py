from io import BytesIO

from django.contrib.auth.models import User
from django.db import models

from django.urls import reverse
from PIL import Image
from pathlib import Path


class Todo(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed_image = models.ImageField('이미지', null=True, blank=True, upload_to='blog/%Y/%m/%d')
    thumbnail = models.ImageField('썸네일', null=True, blank=True, default='blog/%Y/%m/%d/thumbnail')

    def __str__(self):
        return self.title

    # cd_views.py에서 사용하던 def get_success_url(self): 대신 models.py에 만들어 놓으면 cd_views.py에서 사용하던 model = Todo에서 model을 불러올때 알아서 get_absolute_url(self) 함수를 사용 한다
    # def get_absolute_url(self):
    #     return reverse('todo:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.completed_image:  # 이미지가 없을 땐 그대로 세이브하고
            return super().save(*args, **kwargs)

        # 이미지가 있을 땐 썸네일 이미지를 만들어서 저장
        image = Image.open(self.completed_image)
        image.thumbnail((300, 300)) # thumbnail이라는 함수로 사이즈를 넣는다

        completed_image_path = Path(self.completed_image.name)

        thumbnail_name = completed_image_path.stem  # /blog/2025/3/21/이미지파일.png => 이미지파일(이미지이름)
        thumbnail_extension = completed_image_path.suffix.lower()   # /blog/2025/3/21/이미지파일.png => .png
        thumbnail_filename = f'{thumbnail_name}_thumb{thumbnail_extension}' # database_thumb.png

        # 확장자에 따라 처리해주는 알고리즘
        if thumbnail_extension in ['.jpg', '.jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension == '.gif':
            file_type = 'GIF'
        elif thumbnail_extension == '.png':
            file_type = 'PNG'
        else:
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO()  # BytesIO라는 인메모리에 저장
        image.save(temp_thumb, file_type)
        temp_thumb.seek(0)

        # 장고에 있는 썸네일 필드에 이름과 인메모리 객체를 넣고 save=False로 바로 DB엔 저장 하지않고
        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)
        temp_thumb.close()  # 인메모리의 메모리를 비워주고
        return super().save(*args, **kwargs)  # 실제로 원래 일어나야 했던 장고 세이브를 한다


class Comment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.todo.title} 댓글'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ('-created_at', '-id')
