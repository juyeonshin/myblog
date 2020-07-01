from django.contrib import admin
from .models import Post

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