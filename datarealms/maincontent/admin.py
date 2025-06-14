from django.contrib import admin, messages
from .models import Article, Category

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'cat', 'slug', 'content', 'tags']
    filter_horizontal = ['tags']
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('title',)
    ordering = ['-time_create', 'title']
    list_editable = ('is_published', )
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = ['cat__name', 'is_published']

    @admin.display(description="Краткое описание", ordering='content')
    def brief_info(self, article: Article):
        return f"Описание {len(article.content)} символов."

    @admin.action(description="Опубликовать выбранные статьи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Article.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description="Снять с публикации выбранные статьи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Article.Status.DRAFT)
        self.message_user(request, f"{count} статей сняты с публикации!", messages.WARNING)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')