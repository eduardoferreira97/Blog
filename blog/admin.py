
from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at', 'is_published']
    list_display_links = 'title', 'created_at', 'id', 'author'
    search_fields = 'id', 'title', 'text', 'slug', 'created_at', 'author'
    list_filter = 'title', 'author', 'is_published', 'slug', 'created_at'
    list_per_page = 15
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('title',)
    }

# admin.site.register(Post)
