from django.contrib import admin
from .models import Post,Comment

# Register your models here.
#admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'view_count',
        'created_at',
    )
    search_fields =(
        'title',
        'id',
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    listdisplay={
        'id',
        'content',
    }