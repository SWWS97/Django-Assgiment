from django.contrib import admin

from todo.models import Todo, Comment

admin.site.register(Comment)

class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['content', 'author']
    extra = 1

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'is_completed', 'start_date', 'end_date')
    list_filter = ('is_completed',)
    search_fields = ('title',)
    ordering = ('start_date',)
    fieldsets = (
        ('Todo Info', {'fields': ('title', 'description', 'is_completed', 'completed_image')}),
        ('Date Range', {'fields': ('start_date', 'end_date')}),
    )
    summernote_fields = ['description', ]
    inlines = [
        CommentInline
    ]
