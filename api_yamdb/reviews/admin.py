from django.contrib import admin

from .models import Comment, Category, Genre, Review, Title, User


class ReviewsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'score',
        'author',
        'title'
    )
    search_fields = ('text', 'author__username')
    list_filter = ('score', 'title')


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'role',
        'bio',
        'confirmation_code'
    )
    search_fields = ('username', 'email')
    list_filter = ('role',)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'review_title'
    )

    def review_title(self, obj):
        return f'''
            Произведение: {Comment.objects.get(id=obj.id).review.title}.
            Автор обзора - {Comment.objects.get(id=obj.id).review.author}.
        '''

    review_title.short_description = 'Комментарий к обзору на произведение'

    search_fields = ('author__username', 'text')
    list_filter = ['author', 'review__title']


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'category',
        'get_genres'
    )

    def get_genres(self, obj):
        return [genre for genre in obj.genre.all()]
    get_genres.short_description = 'Жанры'
    search_fields = ('name',)
    list_filter = ('genre', 'category', 'year')


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
    search_fields = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
    search_fields = ('name',)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewsAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
