from django.contrib import admin
from .models import Category, Article, ArticleRating, Bookmark

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_approved', 'is_draft', 'created_at')
    list_filter = ('is_approved', 'category', 'created_at')
    search_fields = ('title', 'content')
    actions = ['make_approved']

    def make_approved(self, request, queryset):
        queryset.update(is_approved=True)
    make_approved.short_description = "Approve selected articles for publication"

admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleRating)
admin.site.register(Bookmark)